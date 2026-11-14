-- grain: 1 row per seller x order; key: seller_id + order_id
-- rates are computed per order, so large orders do not weigh more
CREATE OR REPLACE TABLE fct_seller_orders AS
SELECT
    seller_id, order_id,
    ANY_VALUE(purchased_at)        AS purchased_at,
    ANY_VALUE(in_window)           AS in_window,
    ANY_VALUE(is_failed)           AS is_failed,
    ANY_VALUE(is_valid_status)     AS is_valid_status,
    ANY_VALUE(is_single_seller)    AS is_single_seller,
    COUNT(*)                       AS n_items,
    SUM(price)                     AS spend_brl,
    SUM(freight_value)             AS freight_brl,
    MIN(dispatch_on_time)          AS dispatch_on_time,   -- 1 only if every item met its limit
    ANY_VALUE(customer_on_time)    AS customer_on_time,
    ANY_VALUE(dispatch_lead_days)  AS dispatch_lead_days,
    ANY_VALUE(review_score)        AS review_score,
    ANY_VALUE(distance_km)         AS distance_km
FROM fct_order_items
GROUP BY seller_id, order_id;