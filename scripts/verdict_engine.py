"""
Experiment verdict engine.

Converts statistical test results into a clear,
plain-English experiment decision.
"""


def generate_verdict(
    p_value,
    alpha,
    treatment_rate,
    control_rate,
    ci_low,
    ci_high,
    sample_size,
    required_sample_size,
):
    """
    Generate an experiment verdict using:
    - statistical significance
    - observed effect direction
    - confidence interval
    - sample-size adequacy
    """

    observed_difference = treatment_rate - control_rate

    sample_size_adequate = sample_size >= required_sample_size
    statistically_significant = p_value < alpha

    # Determine statistical result
    if statistically_significant:
        if observed_difference > 0:
            result = "Statistically significant positive effect"
            interpretation = (
                "The treatment shows a statistically significant "
                "higher rate than the control."
            )

        elif observed_difference < 0:
            result = "Statistically significant negative effect"
            interpretation = (
                "The treatment shows a statistically significant "
                "lower rate than the control."
            )

        else:
            result = "Statistically significant difference"
            interpretation = (
                "The treatment and control differ significantly, "
                "but the observed difference is approximately zero."
            )

    else:
        result = "No statistically significant difference detected"
        interpretation = (
            "The observed difference is not statistically significant "
            "at the selected significance level. This does not prove "
            "that the treatment and control are identical."
        )

    # Sample-size interpretation
    if sample_size_adequate:
        sample_size_message = (
            "The available sample meets or exceeds the "
            "calculated required sample size."
        )
    else:
        sample_size_message = (
            "The available sample is below the calculated "
            "required sample size."
        )

    return {
        "result": result,
        "interpretation": interpretation,
        "sample_size_message": sample_size_message,
        "p_value": p_value,
        "alpha": alpha,
        "statistically_significant": statistically_significant,
        "observed_difference": observed_difference,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "sample_size": sample_size,
        "required_sample_size": required_sample_size,
        "sample_size_adequate": sample_size_adequate,
    }


if __name__ == "__main__":
    result = generate_verdict(
        p_value=0.0744096553,
        alpha=0.05,
        treatment_rate=0.442283,
        control_rate=0.448188,
        ci_low=-0.012392,
        ci_high=0.000582,
        sample_size=44700,
        required_sample_size=44700,
    )

    print("=== VERDICT ENGINE ===")

    for key, value in result.items():
        print(f"{key}: {value}")