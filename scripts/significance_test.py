"""
Statistical significance testing for two-proportion A/B tests.
"""

from statsmodels.stats.proportion import (
    proportions_ztest,
    confint_proportions_2indep,
)


def two_proportion_test(
    treatment_successes,
    treatment_total,
    control_successes,
    control_total,
    alpha=0.05,
):
    """
    Perform a two-sided two-proportion z-test.

    Returns:
    - treatment rate
    - control rate
    - observed difference
    - relative lift
    - z-statistic
    - p-value
    - confidence interval
    - statistical decision
    """

    treatment_rate = treatment_successes / treatment_total
    control_rate = control_successes / control_total

    # Absolute difference between treatment and control
    observed_difference = treatment_rate - control_rate

    # Relative lift compared with the control
    relative_lift = observed_difference / control_rate

    count = [
        treatment_successes,
        control_successes,
    ]

    nobs = [
        treatment_total,
        control_total,
    ]

    # Two-proportion z-test
    z_statistic, p_value = proportions_ztest(
        count=count,
        nobs=nobs,
        alternative="two-sided",
    )

    # Confidence interval for the difference
    ci_low, ci_high = confint_proportions_2indep(
        count1=treatment_successes,
        nobs1=treatment_total,
        count2=control_successes,
        nobs2=control_total,
        compare="diff",
        method="wald",
        alpha=alpha,
    )

    statistically_significant = p_value < alpha

    return {
        "treatment_rate": treatment_rate,
        "control_rate": control_rate,
        "observed_difference": observed_difference,
        "relative_lift": relative_lift,
        "z_statistic": z_statistic,
        "p_value": p_value,
        "alpha": alpha,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "statistically_significant": statistically_significant,
        "decision": (
            "Reject H0"
            if statistically_significant
            else "Fail to reject H0"
        ),
    }