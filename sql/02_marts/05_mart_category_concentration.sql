-- grain: 1 row per category (whole window, 'unknown' excluded); key: category
CREATE OR REPLACE TABLE mart_category_concentration AS
WITH s AS (
    SELECT category, seller_id, CAST(SUM(price) AS DOUBLE) AS spend
    FROM fct_order_items
    WHERE in_window AND is_valid_status AND category <> 'unknown'
    GROUP BY 1, 2),
sh AS (
    SELECT *, 100.0 * spend / SUM(spend) OVER (PARTITION BY category) AS share_pct
    FROM s)
SELECT
    category,
    SUM(spend)                    AS spend_brl,
    COUNT(*)                      AS n_sellers,
    MAX(share_pct)                AS top1_share_pct,
    SUM(share_pct * share_pct)    AS hhi,
    MAX(share_pct) > 50           AS single_source_risk,
    CASE WHEN SUM(share_pct * share_pct) > 2500 THEN 'high'
         WHEN SUM(share_pct * share_pct) > 1500 THEN 'moderate'
         ELSE 'low' END           AS concentration_level
FROM sh
GROUP BY category;