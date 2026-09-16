"""
Load processed experiment datasets into the SQLite database.
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "db" / "marketing_campaign_optimizer.db"


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

marketing_path = PROCESSED_DIR / "marketing_ab_processed.csv"
cookie_cats_path = PROCESSED_DIR / "cookie_cats_processed.csv"
simulated_campaigns_path = (
    PROCESSED_DIR / "simulated_campaigns.csv"
)

marketing_df = pd.read_csv(marketing_path)
cookie_cats_df = pd.read_csv(cookie_cats_path)
simulated_campaigns_df = pd.read_csv(
    simulated_campaigns_path
)


# ============================================================
# CONVERT BOOLEAN COLUMNS TO SQLITE INTEGER VALUES
# ============================================================

marketing_df["converted"] = (
    marketing_df["converted"].astype(int)
)

cookie_cats_df["retention_1"] = (
    cookie_cats_df["retention_1"].astype(int)
)

cookie_cats_df["retention_7"] = (
    cookie_cats_df["retention_7"].astype(int)
)

simulated_campaigns_df["converted"] = (
    simulated_campaigns_df["converted"].astype(int)
)


# ============================================================
# LOAD INTO SQLITE
# ============================================================

conn = sqlite3.connect(DB_PATH)

# Original validated datasets
marketing_df.to_sql(
    "marketing_ab",
    conn,
    if_exists="replace",
    index=False,
)

cookie_cats_df.to_sql(
    "cookie_cats",
    conn,
    if_exists="replace",
    index=False,
)

# Simulated 40-campaign dataset
simulated_campaigns_df.to_sql(
    "campaigns",
    conn,
    if_exists="replace",
    index=False,
)

conn.close()


# ============================================================
# VALIDATION
# ============================================================

conn = sqlite3.connect(DB_PATH)

marketing_count = conn.execute(
    "SELECT COUNT(*) FROM marketing_ab"
).fetchone()[0]

cookie_cats_count = conn.execute(
    "SELECT COUNT(*) FROM cookie_cats"
).fetchone()[0]

campaign_count = conn.execute(
    "SELECT COUNT(*) FROM campaigns"
).fetchone()[0]

campaigns = conn.execute(
    "SELECT COUNT(DISTINCT campaign_id) FROM campaigns"
).fetchone()[0]

conn.close()


# ============================================================
# FINAL STATUS
# ============================================================

print("=== DATABASE LOAD COMPLETE ===")
print(f"Marketing A/B rows: {marketing_count:,}")
print(f"Cookie Cats rows: {cookie_cats_count:,}")
print(f"Simulated campaign rows: {campaign_count:,}")
print(f"Simulated campaigns: {campaigns}")
print(f"Database: {DB_PATH}")