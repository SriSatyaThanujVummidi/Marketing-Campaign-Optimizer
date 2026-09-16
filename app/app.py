"""
CampaignIQ — Marketing Experimentation Dashboard

Run from the project root:
    streamlit run app/app.py
"""

from pathlib import Path
import sys
import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "marketing_campaign_optimizer.db"
SCRIPTS_PATH = PROJECT_ROOT / "scripts"

if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

from significance_test import two_proportion_test
from power_calculator import calculate_sample_size
from verdict_engine import generate_verdict


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CampaignIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HTML / MARKDOWN RENDERER
# =========================================================

def render_block(body, *args, **kwargs):
    """Render custom HTML with Streamlit's native HTML renderer."""
    if isinstance(body, str) and any(
        marker in body
        for marker in (
            "<div", "<style", "<span", "<h1", "<h2",
            "<h3", "<p>", "<hr", "<section"
        )
    ):
        st.html(body)
    else:
        st.markdown(body, *args, **kwargs)


# =========================================================
# PREMIUM UI CSS
# =========================================================

render_block(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
    font-weight: 600;
}

/* Brand */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #818cf8, #4f46e5);
    color: white;
    font-size: 21px;
}

.brand-name {
    font-size: 19px;
    font-weight: 800;
    color: white;
}

.brand-sub {
    font-size: 11px;
    color: #9ca3af;
}

/* Hero */
.hero {
    padding: 8px 0 26px 0;
}

.eyebrow {
    color: #6366f1;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 8px;
}

.hero h1 {
    font-size: 34px;
    line-height: 1.15;
    letter-spacing: -0.04em;
    margin: 0;
    color: #111827;
    font-weight: 800;
}

.hero p {
    max-width: 760px;
    color: #6b7280;
    font-size: 14px;
    line-height: 1.7;
    margin-top: 12px;
}

/* Section */
.section-title {
    color: #111827;
    font-size: 19px;
    font-weight: 800;
    margin-top: 10px;
}

.section-sub {
    color: #6b7280;
    font-size: 12px;
    line-height: 1.6;
    margin: 5px 0 15px;
}

/* KPI cards */
.kpi-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 18px 20px;
    min-height: 112px;
    box-shadow: 0 4px 18px rgba(15,23,42,.035);
}

.kpi-label {
    color: #9ca3af;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .09em;
}

.kpi-value {
    color: #111827;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

.kpi-help {
    color: #9ca3af;
    font-size: 11px;
    margin-top: 4px;
}

.lift-positive {
    color: #059669 !important;
}

.lift-negative {
    color: #dc2626 !important;
}

/* Verdict */
.verdict-card {
    border-radius: 18px;
    padding: 21px 23px;
    margin: 18px 0 20px;
    border: 1px solid #e5e7eb;
    background: white;
}

.verdict-neutral {
    border-left: 5px solid #f59e0b;
}

.verdict-positive {
    border-left: 5px solid #10b981;
}

.verdict-negative {
    border-left: 5px solid #ef4444;
}

.verdict-icon {
    font-size: 23px;
    font-weight: 800;
}

.verdict-title {
    color: #111827;
    font-size: 17px;
    font-weight: 800;
    margin-top: 4px;
}

.verdict-text {
    color: #6b7280;
    font-size: 12px;
    margin-top: 6px;
}

/* Evidence */
.evidence-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 15px;
    padding: 17px;
    min-height: 105px;
}

.evidence-label {
    color: #9ca3af;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
}

.evidence-value {
    color: #111827;
    font-size: 18px;
    font-weight: 800;
    margin-top: 8px;
}

.evidence-help {
    color: #9ca3af;
    font-size: 11px;
    margin-top: 4px;
}

/* Interpretation */
.interpretation-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px 24px;
    margin: 18px 0 28px;
    box-shadow: 0 4px 18px rgba(15,23,42,.035);
}

.interpretation-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 14px;
}

.interpretation-eyebrow {
    color: #6366f1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .1em;
    margin-bottom: 7px;
}

.interpretation-title {
    color: #111827;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.4;
}

.interpretation-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: #eef2ff;
    color: #4f46e5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    font-weight: 800;
    flex-shrink: 0;
}

.interpretation-body {
    color: #6b7280;
    font-size: 13px;
    line-height: 1.75;
    border-top: 1px solid #f0f1f5;
    padding-top: 15px;
}

.interpretation-body strong {
    color: #374151;
}

/* Planner */
.planner {
    background: #111827;
    border-radius: 18px;
    padding: 22px;
    color: white;
    min-height: 160px;
}

.planner-title {
    font-size: 17px;
    font-weight: 800;
}

.planner-sub {
    color: #9ca3af;
    font-size: 11px;
    margin: 5px 0 22px;
}

.result-label {
    color: #9ca3af;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .08em;
}

.result-number {
    color: white;
    font-size: 25px;
    font-weight: 800;
    margin-top: 4px;
}

/* Upload */
[data-testid="stFileUploader"] {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px;
}
</style>
""",
)


# =========================================================
# DATABASE
# =========================================================

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


conn = get_connection()


# =========================================================
# HELPERS
# =========================================================

def safe_pct(value):
    return f"{value:.2%}"


def single_proportion_ci(conversions, n, confidence=0.95):
    from scipy.stats import norm

    if n <= 0:
        return 0.0, 0.0

    p = conversions / n
    z = norm.ppf(1 - (1 - confidence) / 2)
    se = (p * (1 - p) / n) ** 0.5

    return (
        max(0.0, p - z * se),
        min(1.0, p + z * se),
    )


def get_verdict_class(result):
    if result["statistically_significant"]:
        if result["absolute_difference"] > 0:
            return (
                "verdict-positive",
                "✓",
                "Statistically Significant Positive Effect",
            )
        return (
            "verdict-negative",
            "×",
            "Statistically Significant Negative Effect",
        )

    return (
        "verdict-neutral",
        "!",
        "No Statistically Significant Difference Detected",
    )


def validate_uploaded_csv(df, group_col, conversion_col):
    """Validate an uploaded experiment before calculating statistics."""
    errors = []

    if df.empty:
        errors.append("The uploaded CSV is empty.")

    if group_col not in df.columns:
        errors.append(f"Missing group column: {group_col}")

    if conversion_col not in df.columns:
        errors.append(f"Missing conversion column: {conversion_col}")

    if errors:
        return errors

    if df[group_col].isna().any():
        errors.append("The group column contains missing values.")

    if df[conversion_col].isna().any():
        errors.append("The conversion column contains missing values.")

    groups = df[group_col].dropna().unique().tolist()

    if len(groups) != 2:
        errors.append(
            f"The group column must contain exactly 2 groups; found {len(groups)}."
        )

    converted = pd.to_numeric(df[conversion_col], errors="coerce")

    if converted.isna().any():
        errors.append(
            "The conversion column must contain only binary numeric values: 0 or 1."
        )
    elif not converted.isin([0, 1]).all():
        errors.append(
            "The conversion column must contain only 0 and 1."
        )

    return errors


def calculate_uploaded_result(
    df,
    group_col,
    conversion_col,
    control_value,
    treatment_value,
):
    """Run the project's statistical engine on an uploaded experiment."""
    clean = df[[group_col, conversion_col]].copy()
    clean[conversion_col] = pd.to_numeric(
        clean[conversion_col], errors="coerce"
    )

    control = clean[clean[group_col] == control_value][conversion_col]
    treatment = clean[clean[group_col] == treatment_value][conversion_col]

    control_n = int(len(control))
    treatment_n = int(len(treatment))
    control_conversions = int(control.sum())
    treatment_conversions = int(treatment.sum())

    if control_n == 0 or treatment_n == 0:
        raise ValueError(
            "Both control and treatment groups must contain at least one participant."
        )

    # Use positional arguments here so this app remains compatible
    # with the project's existing significance_test.py function signature.
    stats = two_proportion_test(
        control_conversions,
        control_n,
        treatment_conversions,
        treatment_n,
        0.05,
    )

    baseline_rate = stats["control_rate"]

    power = calculate_sample_size(
        baseline_rate=baseline_rate,
        relative_mde=0.20,
        alpha=0.05,
        power=0.80,
    )

    required_sample = int(power["sample_size_per_group"])
    actual_sample = min(control_n, treatment_n)

    verdict = generate_verdict(
        p_value=stats["p_value"],
        alpha=stats["alpha"],
        treatment_rate=stats["treatment_rate"],
        control_rate=stats["control_rate"],
        ci_low=stats["ci_low"],
        ci_high=stats["ci_high"],
        sample_size=actual_sample,
        required_sample_size=required_sample,
    )

    result = {
        **stats,
        "sample_size": actual_sample,
        "required_sample_size": required_sample,
        "statistically_significant": verdict["statistically_significant"],
        "decision": verdict["result"],
    }

    return result, control_n, treatment_n


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    render_block(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-name">CampaignIQ</div>
                <div class="brand-sub">Experimentation Analytics</div>
            </div>
        </div>
        """
    )

    render_block("### DATA SOURCE")

    source = st.radio(
        "Source",
        ["Existing campaign", "Upload CSV"],
        label_visibility="collapsed",
    )


# =========================================================
# HERO
# =========================================================

render_block(
    """
    <div class="hero">
        <div class="eyebrow">Marketing experimentation</div>
        <h1>Understand what your experiment is telling you.</h1>
        <p>
            Measure conversion lift, statistical significance,
            confidence intervals, and sample requirements in one place.
        </p>
    </div>
    """
)


# =========================================================
# DATABASE OVERVIEW
# =========================================================

campaign_count = conn.execute(
    "SELECT COUNT(DISTINCT campaign_id) FROM campaigns"
).fetchone()[0]

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

underpowered_count = conn.execute(
    """
    SELECT COUNT(*)
    FROM experiment_results
    WHERE sample_size < required_sample_size
    """
).fetchone()[0]

k1, k2, k3, k4 = st.columns(4)

with k1:
    render_block(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">CAMPAIGNS</div>
            <div class="kpi-value">{campaign_count}</div>
            <div class="kpi-help">Available experiments</div>
        </div>
        """
    )

with k2:
    render_block(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">EXPERIMENT RESULTS</div>
            <div class="kpi-value">{result_count}</div>
            <div class="kpi-help">Statistical analyses</div>
        </div>
        """
    )

with k3:
    render_block(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">SIGNIFICANT RESULTS</div>
            <div class="kpi-value">{significant_count}</div>
            <div class="kpi-help">Based on α = 0.05</div>
        </div>
        """
    )

with k4:
    render_block(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">UNDERPOWERED</div>
            <div class="kpi-value">{underpowered_count}</div>
            <div class="kpi-help">Below required sample</div>
        </div>
        """
    )


# =========================================================
# SELECT / UPLOAD EXPERIMENT
# =========================================================

result = None
context_label = ""
channel = ""
source_status = ""
control_n = 0
treatment_n = 0

if source == "Existing campaign":

    campaigns_df = pd.read_sql_query(
        """
        SELECT DISTINCT campaign_id, campaign_name, channel
        FROM campaigns
        ORDER BY campaign_id
        """,
        conn,
    )

    campaign_options = campaigns_df.apply(
        lambda row: f"{row['campaign_id']} — {row['campaign_name']}",
        axis=1,
    ).tolist()

    selected_campaign = st.selectbox(
        "Select a campaign",
        campaign_options,
    )

    selected_campaign_id = int(
        selected_campaign.split(" — ")[0]
    )

    selected_campaign_info = campaigns_df[
        campaigns_df["campaign_id"] == selected_campaign_id
    ].iloc[0]

    channel = selected_campaign_info["channel"]
    context_label = selected_campaign
    source_status = "Database connected"

    result_df = pd.read_sql_query(
        """
        SELECT
            control_rate,
            treatment_rate,
            absolute_difference,
            relative_lift,
            p_value,
            alpha,
            ci_low,
            ci_high,
            sample_size,
            required_sample_size,
            statistically_significant,
            decision
        FROM experiment_results
        WHERE campaign_id = ?
        """,
        conn,
        params=(selected_campaign_id,),
    )

    if result_df.empty:
        st.error("No experiment result found for this campaign.")
        st.stop()

    result = result_df.iloc[0].to_dict()

    control_n = int(result["sample_size"])
    treatment_n = int(result["sample_size"])

else:

    render_block(
        """
        <div class="section-title">Run your own A/B test</div>
        <div class="section-sub">
            Upload a CSV containing a group/variant column and a binary
            conversion/outcome column. CampaignIQ will validate it and
            run the project's statistical testing engine.
        </div>
        """
    )

    uploaded_file = st.file_uploader(
        "Upload experiment CSV",
        type=["csv"],
    )

    if uploaded_file is not None:

        try:
            uploaded_df = pd.read_csv(uploaded_file)

            st.success(
                f"{len(uploaded_df):,} rows loaded"
            )

            if uploaded_df.empty:
                st.error("The uploaded CSV contains no rows.")
                st.stop()

            columns = uploaded_df.columns.tolist()

            group_candidates = [
                c for c in columns
                if c.lower() in {
                    "test_group",
                    "test group",
                    "group",
                    "variant",
                    "treatment",
                    "arm",
                }
            ]

            conversion_candidates = [
                c for c in columns
                if c.lower() in {
                    "converted",
                    "conversion",
                    "converted_flag",
                    "conversion_flag",
                    "outcome",
                }
            ]

            detected_group = (
                group_candidates[0]
                if group_candidates
                else columns[0]
            )

            detected_conversion = (
                conversion_candidates[0]
                if conversion_candidates
                else (
                    columns[1]
                    if len(columns) > 1
                    else columns[0]
                )
            )

            col1, col2 = st.columns(2)

            with col1:
                group_col = st.selectbox(
                    "Group / variant",
                    columns,
                    index=columns.index(detected_group),
                )

            with col2:
                conv_col = st.selectbox(
                    "Conversion / outcome",
                    columns,
                    index=columns.index(detected_conversion),
                )

            validation_errors = validate_uploaded_csv(
                uploaded_df,
                group_col,
                conv_col,
            )

            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                unique_groups = (
                    uploaded_df[group_col]
                    .dropna()
                    .unique()
                    .tolist()
                )

                unique_groups = sorted(
                    unique_groups,
                    key=str,
                )

                default_control = next(
                    (
                        value
                        for value in unique_groups
                        if str(value).strip().lower()
                        in {
                            "control",
                            "a",
                            "holdout",
                            "control group",
                        }
                    ),
                    unique_groups[0],
                )

                control_value = st.selectbox(
                    "Control group",
                    unique_groups,
                    index=unique_groups.index(default_control),
                )

                treatment_options = [
                    value
                    for value in unique_groups
                    if value != control_value
                ]

                treatment_value = treatment_options[0]

                st.caption(
                    f"Treatment group: **{treatment_value}**"
                )

                result, control_n, treatment_n = calculate_uploaded_result(
                    uploaded_df,
                    group_col,
                    conv_col,
                    control_value,
                    treatment_value,
                )

                context_label = (
                    f"Uploaded experiment · "
                    f"{control_value} vs {treatment_value}"
                )
                channel = "Uploaded CSV"
                source_status = "CSV validated"

                render_block(
                    f"""
                    <div class="section-sub">
                        <strong>{control_n:,}</strong> control participants ·
                        <strong>{treatment_n:,}</strong> treatment participants
                    </div>
                    """
                )

                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True,
                )

        except Exception as exc:
            st.error(f"Could not process CSV: {exc}")


# =========================================================
# MAIN EXPERIMENT RESULT
# =========================================================

if result is not None:

    render_block(
        f"""
        <div class="section-title">CURRENT EXPERIMENT</div>
        <div class="section-sub">
            {context_label}
            {" · Channel: " + str(channel) if channel else ""}
            &nbsp;&nbsp; ✓ {source_status}
        </div>
        """
    )

    verdict_class, verdict_icon, verdict_title = get_verdict_class(result)

    render_block(
        f"""
        <div class="verdict-card {verdict_class}">
            <div class="verdict-icon">{verdict_icon}</div>
            <div class="verdict-title">{verdict_title}</div>
            <div class="verdict-text">
                {"The observed difference is statistically significant at α = "
                + f"{result['alpha']:.2f}."
                if result["statistically_significant"]
                else
                "No statistically significant difference was detected at "
                + f"α = {result['alpha']:.2f}."}
            </div>
        </div>
        """
    )

    lift_class = (
        "lift-positive"
        if result["relative_lift"] >= 0
        else "lift-negative"
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">CONTROL CONVERSION</div>
                <div class="kpi-value">{safe_pct(result['control_rate'])}</div>
                <div class="kpi-help">Control group</div>
            </div>
            """
        )

    with k2:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">TREATMENT CONVERSION</div>
                <div class="kpi-value">{safe_pct(result['treatment_rate'])}</div>
                <div class="kpi-help">Treatment group</div>
            </div>
            """
        )

    with k3:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">RELATIVE LIFT</div>
                <div class="kpi-value {lift_class}">
                    {result['relative_lift']:+.1%}
                </div>
                <div class="kpi-help">Treatment vs control</div>
            </div>
            """
        )

    with k4:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">P-VALUE</div>
                <div class="kpi-value">{result['p_value']:.4f}</div>
                <div class="kpi-help">α = {result['alpha']:.2f}</div>
            </div>
            """
        )

    # -----------------------------------------------------
    # Chart + evidence
    # -----------------------------------------------------

    chart_col, info_col = st.columns([2.2, 1])

    with chart_col:

        render_block(
            """
            <div class="section-title">Conversion performance</div>
            <div class="section-sub">
                Control vs treatment conversion rates with 95% confidence intervals.
            </div>
            """
        )

        control_conversions = round(
            result["control_rate"] * control_n
        )
        treatment_conversions = round(
            result["treatment_rate"] * treatment_n
        )

        control_lo, control_hi = single_proportion_ci(
            control_conversions,
            control_n,
        )

        treatment_lo, treatment_hi = single_proportion_ci(
            treatment_conversions,
            treatment_n,
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Control", "Treatment"],
                y=[
                    result["control_rate"],
                    result["treatment_rate"],
                ],
                text=[
                    safe_pct(result["control_rate"]),
                    safe_pct(result["treatment_rate"]),
                ],
                textposition="outside",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=[
                        control_hi - result["control_rate"],
                        treatment_hi - result["treatment_rate"],
                    ],
                    arrayminus=[
                        result["control_rate"] - control_lo,
                        result["treatment_rate"] - treatment_lo,
                    ],
                ),
            )
        )

        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis=dict(
                tickformat=".1%",
                title="Conversion rate",
                gridcolor="#eef0f4",
            ),
            xaxis=dict(title=""),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    with info_col:

        render_block(
            """
            <div class="section-title">Experiment evidence</div>
            <div class="section-sub">Key statistical signals.</div>
            """
        )

        render_block(
            f"""
            <div class="evidence-card">
                <div class="evidence-label">ABSOLUTE DIFFERENCE</div>
                <div class="evidence-value">
                    {result['absolute_difference']:+.2%}
                </div>
                <div class="evidence-help">Treatment − control</div>
            </div>
            """
        )

        st.write("")

        render_block(
            f"""
            <div class="evidence-card">
                <div class="evidence-label">95% CONFIDENCE INTERVAL</div>
                <div class="evidence-value">
                    {result['ci_low'] * 100:.2f} pp to
                    {result['ci_high'] * 100:.2f} pp
                </div>
                <div class="evidence-help">Absolute difference</div>
            </div>
            """
        )

        st.write("")

        sample_status = (
            "✓ Adequate"
            if result["sample_size"] >= result["required_sample_size"]
            else "⚠ Underpowered"
        )

        render_block(
            f"""
            <div class="evidence-card">
                <div class="evidence-label">SAMPLE ADEQUACY</div>
                <div class="evidence-value">{sample_status}</div>
                <div class="evidence-help">Actual vs required sample</div>
            </div>
            """
        )

    # -----------------------------------------------------
    # Power analysis
    # -----------------------------------------------------

    render_block(
        """
        <div class="section-title">Power & sample-size analysis</div>
        <div class="section-sub">
            Check whether the experiment has enough participants to detect
            the configured effect.
        </div>
        """
    )

    actual_sample = int(result["sample_size"])
    required_sample = int(result["required_sample_size"])

    p1, p2, p3 = st.columns(3)

    with p1:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">ACTUAL / GROUP</div>
                <div class="kpi-value">{actual_sample:,}</div>
                <div class="kpi-help">Participants currently available</div>
            </div>
            """
        )

    with p2:
        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">REQUIRED / GROUP</div>
                <div class="kpi-value">{required_sample:,}</div>
                <div class="kpi-help">Required for 80% power</div>
            </div>
            """
        )

    with p3:
        status = (
            "✓ Adequate"
            if actual_sample >= required_sample
            else "⚠ Underpowered"
        )

        render_block(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">SAMPLE STATUS</div>
                <div class="kpi-value">{status}</div>
                <div class="kpi-help">Actual vs required sample</div>
            </div>
            """
        )

    if actual_sample < required_sample:
        st.warning(
            "The available sample is below the calculated requirement for "
            "80% power and a 20% relative MDE. A non-significant result "
            "should therefore be interpreted cautiously."
        )

    # -----------------------------------------------------
    # Interpretation
    # -----------------------------------------------------

    lift = result["relative_lift"] * 100
    p_value = result["p_value"]
    alpha = result["alpha"]
    ci_low_pp = result["ci_low"] * 100
    ci_high_pp = result["ci_high"] * 100

    if result["statistically_significant"]:
        if lift > 0:
            interpretation_title = (
                "Treatment shows a statistically significant improvement"
            )
            interpretation_text = (
                f"The treatment conversion rate was "
                f"<strong>{lift:.2f}% higher</strong> than the control. "
                f"The observed difference is statistically significant at "
                f"<strong>α = {alpha:.2f}</strong> with "
                f"<strong>p = {p_value:.6f}</strong>."
            )
        else:
            interpretation_title = (
                "Treatment shows a statistically significant decline"
            )
            interpretation_text = (
                f"The treatment conversion rate was "
                f"<strong>{abs(lift):.2f}% lower</strong> than the control. "
                f"The observed difference is statistically significant at "
                f"<strong>α = {alpha:.2f}</strong> with "
                f"<strong>p = {p_value:.6f}</strong>."
            )
    else:
        interpretation_title = (
            "The experiment did not detect a statistically significant difference"
        )
        interpretation_text = (
            f"The treatment showed an observed relative lift of "
            f"<strong>{lift:.2f}%</strong>, but the difference was "
            f"<strong>not statistically significant</strong> at "
            f"α = {alpha:.2f}. The p-value was "
            f"<strong>{p_value:.6f}</strong>."
        )

    render_block(
        f"""
        <div class="interpretation-card">
            <div class="interpretation-header">
                <div>
                    <div class="interpretation-eyebrow">
                        RESULT INTERPRETATION
                    </div>
                    <div class="interpretation-title">
                        {interpretation_title}
                    </div>
                </div>
                <div class="interpretation-icon">↘</div>
            </div>

            <div class="interpretation-body">
                {interpretation_text}
                <br><br>
                The 95% confidence interval for the absolute difference
                ranges from <strong>{ci_low_pp:.2f} pp</strong> to
                <strong>{ci_high_pp:.2f} pp</strong>.
                <br><br>
                This does <strong>not prove that the two groups are identical</strong>.
            </div>
        </div>
        """
    )


# =========================================================
# EXPERIMENT PLANNER
# =========================================================

render_block("<hr>")

render_block(
    """
    <div class="section-title">🔮 Experiment planner</div>
    <div class="section-sub">
        Estimate how many samples each group needs before you launch
        or extend an experiment.
    </div>
    """
)

planner_left, planner_right = st.columns([1.25, 1])

with planner_left:

    p1, p2 = st.columns(2)

    with p1:
        baseline_rate = st.slider(
            "Baseline conversion",
            min_value=0.01,
            max_value=0.30,
            value=0.05,
            step=0.01,
            format="%.2f",
        )

    with p2:
        mde_relative = st.slider(
            "Minimum detectable lift",
            min_value=0.02,
            max_value=0.50,
            value=0.10,
            step=0.01,
            format="%.2f",
        )

    target_rate = baseline_rate * (1 + mde_relative)

    try:
        calc_result = calculate_sample_size(
            baseline_rate=baseline_rate,
            relative_mde=mde_relative,
            alpha=0.05,
            power=0.80,
        )

        required_n = calc_result["sample_size_per_group"]

        render_block(
            f"""
            <div class="planner">
                <div class="planner-title">Launch requirements</div>
                <div class="planner-sub">
                    80% statistical power · α = 0.05
                </div>

                <div style="display:flex;gap:55px;align-items:end;">

                    <div>
                        <div class="result-label">CONTROL</div>
                        <div class="result-number">{baseline_rate:.1%}</div>
                    </div>

                    <div>
                        <div class="result-label">TARGET TEST</div>
                        <div class="result-number">{target_rate:.1%}</div>
                    </div>

                    <div>
                        <div class="result-label">REQUIRED / GROUP</div>
                        <div class="result-number">{required_n:,}</div>
                    </div>

                </div>
            </div>
            """
        )

    except Exception as exc:
        st.error(f"Unable to calculate sample size: {exc}")

with planner_right:
    render_block(
        """
        <div class="kpi-card" style="min-height:220px;">
            <div class="kpi-label">WHAT THIS MEANS</div>

            <div style="
                font-size:17px;
                font-weight:800;
                color:#111827;
                margin:10px 0;
            ">
                Plan your experiment around the effect you actually care about.
            </div>

            <div style="
                font-size:13px;
                color:#6b7280;
                line-height:1.7;
            ">
                Set the current control conversion rate and the smallest
                relative improvement worth detecting. The calculator estimates
                the sample required per group using the project's power calculation.
            </div>
        </div>
        """
    )


# =========================================================
# FOOTER
# =========================================================

render_block(
    """
    <div style="
        text-align:center;
        margin-top:35px;
        color:#9ca3af;
        font-size:11px;
    ">
        CampaignIQ · Marketing Experimentation Analytics
    </div>
    """
)
