-- ============================================================
-- MARKETING CAMPAIGN OPTIMIZER
-- DATABASE SCHEMA
-- ============================================================

PRAGMA foreign_keys = ON;


-- ============================================================
-- MARKETING A/B TEST DATA
-- ============================================================

CREATE TABLE IF NOT EXISTS marketing_ab (
    user_id INTEGER PRIMARY KEY,
    test_group TEXT NOT NULL,
    converted INTEGER NOT NULL,
    total_ads INTEGER NOT NULL,
    most_ads_day TEXT NOT NULL,
    most_ads_hour INTEGER NOT NULL,

    CHECK (test_group IN ('ad', 'psa')),
    CHECK (converted IN (0, 1)),
    CHECK (total_ads >= 0),
    CHECK (most_ads_hour BETWEEN 0 AND 23)
);


-- ============================================================
-- COOKIE CATS EXPERIMENT DATA
-- ============================================================

CREATE TABLE IF NOT EXISTS cookie_cats (
    userid INTEGER PRIMARY KEY,
    version TEXT NOT NULL,
    sum_gamerounds INTEGER NOT NULL,
    retention_1 INTEGER NOT NULL,
    retention_7 INTEGER NOT NULL,

    CHECK (version IN ('gate_30', 'gate_40')),
    CHECK (sum_gamerounds >= 0),
    CHECK (retention_1 IN (0, 1)),
    CHECK (retention_7 IN (0, 1))
);


-- ============================================================
-- CAMPAIGN METADATA
-- ============================================================

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL UNIQUE,
    sector TEXT,
    channel TEXT,
    experiment_type TEXT NOT NULL,
    control_name TEXT NOT NULL,
    treatment_name TEXT NOT NULL,
    primary_metric TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- EXPERIMENT RESULTS
-- ============================================================

CREATE TABLE IF NOT EXISTS experiment_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    metric_name TEXT NOT NULL,
    control_rate REAL NOT NULL,
    treatment_rate REAL NOT NULL,
    absolute_difference REAL NOT NULL,
    relative_lift REAL NOT NULL,
    p_value REAL NOT NULL,
    alpha REAL NOT NULL,
    ci_low REAL NOT NULL,
    ci_high REAL NOT NULL,
    sample_size INTEGER NOT NULL,
    required_sample_size INTEGER NOT NULL,
    statistically_significant INTEGER NOT NULL,
    decision TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id)
        REFERENCES campaigns(campaign_id),

    CHECK (alpha > 0 AND alpha < 1),
    CHECK (sample_size >= 0),
    CHECK (required_sample_size >= 0),
    CHECK (statistically_significant IN (0, 1))
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_marketing_test_group
    ON marketing_ab(test_group);

CREATE INDEX IF NOT EXISTS idx_cookie_version
    ON cookie_cats(version);

CREATE INDEX IF NOT EXISTS idx_campaign_channel
    ON campaigns(channel);

CREATE INDEX IF NOT EXISTS idx_campaign_sector
    ON campaigns(sector);

CREATE INDEX IF NOT EXISTS idx_results_campaign
    ON experiment_results(campaign_id);