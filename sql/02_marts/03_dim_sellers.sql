-- grain: 1 row per seller; key: seller_id
CREATE OR REPLACE TABLE dim_sellers AS
WITH cat_spend AS (
    SELECT seller_id, category, SUM(price) AS spend
    FROM fct_order_items
    WHERE in_window AND is_valid_status AND category <> 'unknown'
    GROUP BY 1, 2),
main_cat AS (
    SELECT seller_id, ARG_MAX(category, spend) AS main_category
    FROM cat_spend GROUP BY 1),
activity AS (
    SELECT seller_id,
           MIN(purchased_at) AS first_order_at,
           MAX(purchased_at) AS last_order_at
    FROM fct_seller_orders GROUP BY 1)
SELECT s.seller_id, s.seller_state, s.seller_city,
       COALESCE(m.main_category, 'unknown') AS main_category,
       a.first_order_at, a.last_order_at
FROM stg_sellers s
LEFT JOIN main_cat m USING (seller_id)
LEFT JOIN activity a USING (seller_id);