"""
Campaign simulator for the Marketing Campaign Optimizer.

Generates user-level A/B testing data for 40 simulated
marketing campaigns across multiple marketing channels.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


CAMPAIGN_DEFINITIONS = [
    # Email campaigns
    {
        "campaign_id": 1,
        "campaign_name": "Summer Email Campaign",
        "channel": "Email",
        "control_rate": 0.020,
        "treatment_rate": 0.025,
    },
    {
        "campaign_id": 2,
        "campaign_name": "Product Launch Email",
        "channel": "Email",
        "control_rate": 0.018,
        "treatment_rate": 0.022,
    },
    {
        "campaign_id": 3,
        "campaign_name": "Weekend Email Offer",
        "channel": "Email",
        "control_rate": 0.025,
        "treatment_rate": 0.030,
    },
    {
        "campaign_id": 4,
        "campaign_name": "Customer Reactivation Email",
        "channel": "Email",
        "control_rate": 0.015,
        "treatment_rate": 0.019,
    },
    {
        "campaign_id": 5,
        "campaign_name": "Newsletter CTA Test",
        "channel": "Email",
        "control_rate": 0.030,
        "treatment_rate": 0.034,
    },

    # Social campaigns
    {
        "campaign_id": 6,
        "campaign_name": "Instagram Product Campaign",
        "channel": "Social Media",
        "control_rate": 0.022,
        "treatment_rate": 0.027,
    },
    {
        "campaign_id": 7,
        "campaign_name": "Facebook Retargeting",
        "channel": "Social Media",
        "control_rate": 0.028,
        "treatment_rate": 0.032,
    },
    {
        "campaign_id": 8,
        "campaign_name": "LinkedIn Lead Campaign",
        "channel": "Social Media",
        "control_rate": 0.012,
        "treatment_rate": 0.016,
    },
    {
        "campaign_id": 9,
        "campaign_name": "Social Video Campaign",
        "channel": "Social Media",
        "control_rate": 0.020,
        "treatment_rate": 0.018,
    },
    {
        "campaign_id": 10,
        "campaign_name": "Influencer Promotion",
        "channel": "Social Media",
        "control_rate": 0.026,
        "treatment_rate": 0.031,
    },

    # Search campaigns
    {
        "campaign_id": 11,
        "campaign_name": "Google Search Campaign",
        "channel": "Search",
        "control_rate": 0.035,
        "treatment_rate": 0.040,
    },
    {
        "campaign_id": 12,
        "campaign_name": "Branded Search Test",
        "channel": "Search",
        "control_rate": 0.040,
        "treatment_rate": 0.044,
    },
    {
        "campaign_id": 13,
        "campaign_name": "Non-Branded Search",
        "channel": "Search",
        "control_rate": 0.018,
        "treatment_rate": 0.023,
    },
    {
        "campaign_id": 14,
        "campaign_name": "Search Landing Page Test",
        "channel": "Search",
        "control_rate": 0.025,
        "treatment_rate": 0.029,
    },
    {
        "campaign_id": 15,
        "campaign_name": "High Intent Keyword Test",
        "channel": "Search",
        "control_rate": 0.045,
        "treatment_rate": 0.049,
    },

    # Display campaigns
    {
        "campaign_id": 16,
        "campaign_name": "Display Banner Test",
        "channel": "Display",
        "control_rate": 0.010,
        "treatment_rate": 0.013,
    },
    {
        "campaign_id": 17,
        "campaign_name": "Retargeting Banner",
        "channel": "Display",
        "control_rate": 0.016,
        "treatment_rate": 0.020,
    },
    {
        "campaign_id": 18,
        "campaign_name": "Homepage Display Campaign",
        "channel": "Display",
        "control_rate": 0.012,
        "treatment_rate": 0.011,
    },
    {
        "campaign_id": 19,
        "campaign_name": "Mobile Display Campaign",
        "channel": "Display",
        "control_rate": 0.009,
        "treatment_rate": 0.012,
    },
    {
        "campaign_id": 20,
        "campaign_name": "Programmatic Display Test",
        "channel": "Display",
        "control_rate": 0.014,
        "treatment_rate": 0.018,
    },

    # Push notification campaigns
    {
        "campaign_id": 21,
        "campaign_name": "App Push Promotion",
        "channel": "Push Notification",
        "control_rate": 0.030,
        "treatment_rate": 0.036,
    },
    {
        "campaign_id": 22,
        "campaign_name": "Flash Sale Push",
        "channel": "Push Notification",
        "control_rate": 0.035,
        "treatment_rate": 0.042,
    },
    {
        "campaign_id": 23,
        "campaign_name": "Cart Reminder Push",
        "channel": "Push Notification",
        "control_rate": 0.040,
        "treatment_rate": 0.045,
    },
    {
        "campaign_id": 24,
        "campaign_name": "New Feature Push",
        "channel": "Push Notification",
        "control_rate": 0.020,
        "treatment_rate": 0.024,
    },
    {
        "campaign_id": 25,
        "campaign_name": "Reactivation Push",
        "channel": "Push Notification",
        "control_rate": 0.018,
        "treatment_rate": 0.021,
    },

    # SMS campaigns
    {
        "campaign_id": 26,
        "campaign_name": "SMS Discount Campaign",
        "channel": "SMS",
        "control_rate": 0.025,
        "treatment_rate": 0.030,
    },
    {
        "campaign_id": 27,
        "campaign_name": "SMS Flash Sale",
        "channel": "SMS",
        "control_rate": 0.030,
        "treatment_rate": 0.036,
    },
    {
        "campaign_id": 28,
        "campaign_name": "SMS Cart Reminder",
        "channel": "SMS",
        "control_rate": 0.022,
        "treatment_rate": 0.026,
    },
    {
        "campaign_id": 29,
        "campaign_name": "SMS Loyalty Campaign",
        "channel": "SMS",
        "control_rate": 0.035,
        "treatment_rate": 0.039,
    },
    {
        "campaign_id": 30,
        "campaign_name": "SMS Win Back Campaign",
        "channel": "SMS",
        "control_rate": 0.016,
        "treatment_rate": 0.020,
    },

    # In-app campaigns
    {
        "campaign_id": 31,
        "campaign_name": "In-App Banner Test",
        "channel": "In-App",
        "control_rate": 0.040,
        "treatment_rate": 0.045,
    },
    {
        "campaign_id": 32,
        "campaign_name": "In-App Recommendation",
        "channel": "In-App",
        "control_rate": 0.035,
        "treatment_rate": 0.041,
    },
    {
        "campaign_id": 33,
        "campaign_name": "In-App Checkout Test",
        "channel": "In-App",
        "control_rate": 0.050,
        "treatment_rate": 0.055,
    },
    {
        "campaign_id": 34,
        "campaign_name": "In-App Offer Test",
        "channel": "In-App",
        "control_rate": 0.028,
        "treatment_rate": 0.032,
    },
    {
        "campaign_id": 35,
        "campaign_name": "In-App Onboarding Test",
        "channel": "In-App",
        "control_rate": 0.022,
        "treatment_rate": 0.027,
    },

    # Other campaigns
    {
        "campaign_id": 36,
        "campaign_name": "Homepage CTA Test",
        "channel": "Website",
        "control_rate": 0.030,
        "treatment_rate": 0.034,
    },
    {
        "campaign_id": 37,
        "campaign_name": "Pricing Page Test",
        "channel": "Website",
        "control_rate": 0.025,
        "treatment_rate": 0.021,
    },
    {
        "campaign_id": 38,
        "campaign_name": "Checkout Flow Test",
        "channel": "Website",
        "control_rate": 0.045,
        "treatment_rate": 0.052,
    },
    {
        "campaign_id": 39,
        "campaign_name": "Referral Campaign",
        "channel": "Referral",
        "control_rate": 0.020,
        "treatment_rate": 0.026,
    },
    {
        "campaign_id": 40,
        "campaign_name": "Loyalty Campaign",
        "channel": "Loyalty",
        "control_rate": 0.038,
        "treatment_rate": 0.043,
    },
]


def simulate_campaign(
    campaign_id,
    campaign_name,
    channel,
    sample_size,
    control_rate,
    treatment_rate,
    random_seed=42,
):
    """
    Generate user-level A/B testing data for one campaign.
    """

    rng = np.random.default_rng(random_seed)

    control_size = sample_size // 2
    treatment_size = sample_size - control_size

    control = pd.DataFrame({
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "channel": channel,
        "user_id": np.arange(1, control_size + 1),
        "test_group": "control",
        "converted": rng.binomial(1, control_rate, control_size),
    })

    treatment = pd.DataFrame({
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "channel": channel,
        "user_id": np.arange(
            control_size + 1,
            sample_size + 1
        ),
        "test_group": "treatment",
        "converted": rng.binomial(1, treatment_rate, treatment_size),
    })

    campaign_data = pd.concat(
        [control, treatment],
        ignore_index=True
    )

    return campaign_data

def generate_all_campaigns(
    sample_size_per_campaign=10000,
    random_seed=42,
):
    """
    Generate user-level A/B testing data for all 40 campaigns.

    Each simulated user receives a globally unique user_id.
    """

    all_campaigns = []

    user_id_offset = 0

    for campaign in CAMPAIGN_DEFINITIONS:

        campaign_data = simulate_campaign(
            campaign_id=campaign["campaign_id"],
            campaign_name=campaign["campaign_name"],
            channel=campaign["channel"],
            sample_size=sample_size_per_campaign,
            control_rate=campaign["control_rate"],
            treatment_rate=campaign["treatment_rate"],
            random_seed=random_seed + campaign["campaign_id"],
        )

        # Make user IDs globally unique across all campaigns.
        campaign_data["user_id"] += user_id_offset

        user_id_offset += sample_size_per_campaign

        all_campaigns.append(campaign_data)

    return pd.concat(
        all_campaigns,
        ignore_index=True
    )

def main():
    """
    Generate all simulated campaigns and save them
    to the processed data directory.
    """

    campaigns = generate_all_campaigns(
        sample_size_per_campaign=10000,
        random_seed=42,
    )

    output_path = PROCESSED_DIR / "simulated_campaigns.csv"

    campaigns.to_csv(
        output_path,
        index=False
    )

    print("=== CAMPAIGN SIMULATION COMPLETE ===")
    print(f"Campaigns: {campaigns['campaign_id'].nunique()}")
    print(f"Rows: {len(campaigns):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()