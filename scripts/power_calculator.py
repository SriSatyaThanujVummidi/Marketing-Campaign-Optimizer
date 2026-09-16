"""
Power and sample-size calculations for two-proportion A/B tests.
"""

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def calculate_sample_size(
    baseline_rate,
    relative_mde,
    alpha=0.05,
    power=0.80,
):
    """
    Calculate the required sample size per group
    for a two-sided two-proportion A/B test.
    """

    # Calculate treatment rate implied by the relative MDE
    target_rate = baseline_rate * (1 + relative_mde)

    # Convert proportions to Cohen's h
    effect_size = proportion_effectsize(
        baseline_rate,
        target_rate
    )

    # Calculate sample size
    analysis = NormalIndPower()

    sample_size_per_group = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=1.0,
        alternative="two-sided"
    )

    return {
        "baseline_rate": baseline_rate,
        "target_rate": target_rate,
        "relative_mde": relative_mde,
        "alpha": alpha,
        "power": power,
        "sample_size_per_group": round(sample_size_per_group),
        "total_sample_size": round(sample_size_per_group * 2),
    }

if __name__ == "__main__":
    result = calculate_sample_size(
        baseline_rate=0.01785411,
        relative_mde=0.20,
        alpha=0.05,
        power=0.80,
    )

    print("=== POWER CALCULATOR ===")

    for key, value in result.items():
        print(f"{key}: {value}")