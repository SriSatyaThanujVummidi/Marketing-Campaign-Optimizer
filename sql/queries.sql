-- ============================================================
-- MARKETING CAMPAIGN OPTIMIZER
-- ANALYTICAL SQL QUERIES
-- ============================================================


-- ============================================================
-- 1. MARKETING A/B GROUP SUMMARY
-- ============================================================

SELECT
    test_group,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(
        AVG(converted) * 100,
        4
    ) AS conversion_rate_pct
FROM marketing_ab
GROUP BY test_group
ORDER BY test_group;


-- ============================================================
-- 2. MARKETING A/B EXPOSURE SUMMARY
-- ============================================================

SELECT
    test_group,
    COUNT(*) AS users,
    ROUND(AVG(total_ads), 2) AS avg_ads,
    MIN(total_ads) AS min_ads,
    MAX(total_ads) AS max_ads
FROM marketing_ab
GROUP BY test_group
ORDER BY test_group;


-- ============================================================
-- 3. MARKETING CONVERSION BY DAY
-- ============================================================

SELECT
    most_ads_day,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(
        AVG(converted) * 100,
        4
    ) AS conversion_rate_pct
FROM marketing_ab
GROUP BY most_ads_day
ORDER BY conversion_rate_pct DESC;


-- ============================================================
-- 4. MARKETING CONVERSION BY HOUR
-- ============================================================

SELECT
    most_ads_hour,
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(
        AVG(converted) * 100,
        4
    ) AS conversion_rate_pct
FROM marketing_ab
GROUP BY most_ads_hour
ORDER BY most_ads_hour;


-- ============================================================
-- 5. COOKIE CATS RETENTION SUMMARY
-- ============================================================

SELECT
    version,
    COUNT(*) AS users,
    ROUND(
        AVG(retention_1) * 100,
        4
    ) AS retention_day1_pct,
    ROUND(
        AVG(retention_7) * 100,
        4
    ) AS retention_day7_pct
FROM cookie_cats
GROUP BY version
ORDER BY version;


-- ============================================================
-- 6. COOKIE CATS GAME-ROUND SUMMARY
-- ============================================================

SELECT
    version,
    COUNT(*) AS users,
    ROUND(AVG(sum_gamerounds), 2) AS avg_game_rounds,
    MIN(sum_gamerounds) AS min_game_rounds,
    MAX(sum_gamerounds) AS max_game_rounds
FROM cookie_cats
GROUP BY version
ORDER BY version;


-- ============================================================
-- 7. MARKETING OVERALL METRICS
-- ============================================================

SELECT
    COUNT(*) AS total_users,
    SUM(converted) AS total_conversions,
    ROUND(
        AVG(converted) * 100,
        4
    ) AS overall_conversion_rate_pct,
    ROUND(AVG(total_ads), 2) AS avg_ads_per_user
FROM marketing_ab;


-- ============================================================
-- 8. COOKIE CATS OVERALL METRICS
-- ============================================================

SELECT
    COUNT(*) AS total_users,
    ROUND(
        AVG(retention_1) * 100,
        4
    ) AS overall_day1_retention_pct,
    ROUND(
        AVG(retention_7) * 100,
        4
    ) AS overall_day7_retention_pct,
    ROUND(
        AVG(sum_gamerounds),
        2
    ) AS avg_game_rounds
FROM cookie_cats;