"""
Generate statistical experiment results for all simulated campaigns.

Pipeline:
SQLite campaigns
    -> significance test
    -> sample-size calculation
    -> verdict engine
    -> SQLite experiment_results
"""

import sqlite3
from pathlib import Path

import pandas as pd

from significance_test import two_proportion_test
from power_calculator import calculate_sample_size
from verdict_engine import generate_verdict


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "db" / "marketing_campaign_optimizer.db"


# ============================================================
# LOAD CAMPAIGN SUMMARY
# ============================================================

def load_campaign_summary(conn):
    """
    Aggregate user-level campaign data into
    control/treatment success counts.
    """

    query = """
        SELECT
            campaign_id,
            test_group,
            COUNT(*) AS sample_size,
            SUM(converted) AS conversions
        FROM campaigns
        GROUP BY campaign_id, test_group
        ORDER BY campaign_id, test_group
    """

    return pd.read_sql_query(query, conn)


# ============================================================
# GENERATE EXPERIMENT RESULTS
# ============================================================

def generate_results(campaign_summary):
    """
    Run statistical analysis for every campaign.
    """

    results = []

    for campaign_id in campaign_summary["campaign_id"].unique():

        campaign = campaign_summary[
            campaign_summary["campaign_id"] == campaign_id
        ]

        control = campaign[
            campaign["test_group"] == "control"
        ].iloc[0]

        treatment = campaign[
            campaign["test_group"] == "treatment"
        ].iloc[0]

        control_total = int(control["sample_size"])
        control_successes = int(control["conversions"])

        treatment_total = int(treatment["sample_size"])
        treatment_successes = int(treatment["conversions"])

        # ----------------------------------------------------
        # Statistical significance
        # ----------------------------------------------------

        test_result = two_proportion_test(
            treatment_successes=treatment_successes,
            treatment_total=treatment_total,
            control_successes=control_successes,
            control_total=control_total,
            alpha=0.05,
        )

        # ----------------------------------------------------
        # Required sample size
        # ----------------------------------------------------

        required_sample = calculate_sample_size(
            baseline_rate=test_result["control_rate"],
            relative_mde=0.20,
            alpha=0.05,
            power=0.80,
        )

        required_sample_size = required_sample[
            "sample_size_per_group"
        ]

        # ----------------------------------------------------
        # Verdict
        # ----------------------------------------------------

        verdict = generate_verdict(
            p_value=test_result["p_value"],
            alpha=test_result["alpha"],
            treatment_rate=test_result["treatment_rate"],
            control_rate=test_result["control_rate"],
            ci_low=test_result["ci_low"],
            ci_high=test_result["ci_high"],
            sample_size=min(
                control_total,
                treatment_total,
            ),
            required_sample_size=required_sample_size,
        )

        results.append({
            "campaign_id": int(campaign_id),
            "metric_name": "conversion_rate",
            "control_rate": test_result["control_rate"],
            "treatment_rate": test_result["treatment_rate"],
            "absolute_difference": test_result[
                "observed_difference"
            ],
            "relative_lift": test_result["relative_lift"],
            "p_value": test_result["p_value"],
            "alpha": test_result["alpha"],
            "ci_low": test_result["ci_low"],
            "ci_high": test_result["ci_high"],
            "sample_size": min(
                control_total,
                treatment_total,
            ),
            "required_sample_size": required_sample_size,
            "statistically_significant": int(
                verdict["statistically_significant"]
            ),
            "decision": verdict["result"],
        })

    return pd.DataFrame(results)


# ============================================================
# SAVE RESULTS TO SQLITE
# ============================================================

def save_results(results_df, conn):
    """
    Replace the existing experiment results
    with the latest calculated results.
    """

    conn.execute("DELETE FROM experiment_results")

    results_df.to_sql(
        "experiment_results",
        conn,
        if_exists="append",
        index=False,
    )

    conn.commit()


# ============================================================
# MAIN
# ============================================================

def main():

    conn = sqlite3.connect(DB_PATH)

    campaign_summary = load_campaign_summary(conn)

    results_df = generate_results(
        campaign_summary
    )

    save_results(
        results_df,
        conn
    )

    result_count = conn.execute(
        "SELECT COUNT(*) FROM experiment_results"
    ).fetchone()[0]

    significant_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM experiment_results
        WHERE statistically_significant = 1
        """
    ).fetchone()[0]

    conn.close()

    print("=== EXPERIMENT RESULTS GENERATED ===")
    print(f"Campaigns analyzed: {len(results_df)}")
    print(f"Results stored: {result_count}")
    print(f"Statistically significant: {significant_count}")
    print(f"Database: {DB_PATH}")


if __name__ == "__main__":
    main()