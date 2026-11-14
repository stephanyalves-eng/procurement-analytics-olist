-- grain: 1 row per seller x month (analysis window only); key: seller_id + month
CREATE OR REPLACE TABLE mart_seller_monthly AS
SELECT
    seller_id,
    DATE_TRUNC('month', purchased_at)                                   AS month,
    COUNT(*) FILTER (WHERE is_valid_status)                             AS n_orders,
    SUM(spend_brl) FILTER (WHERE is_valid_status)                       AS spend_brl,
    SUM(freight_brl) FILTER (WHERE is_valid_status)                     AS freight_brl,
    AVG(dispatch_on_time) FILTER (WHERE is_single_seller)               AS dispatch_on_time_rate,
    COUNT(dispatch_on_time) FILTER (WHERE is_single_seller)             AS n_dispatch_obs,
    AVG(customer_on_time) FILTER (WHERE is_single_seller)               AS customer_on_time_rate,
    AVG(review_score) FILTER (WHERE is_single_seller)                   AS review_mean,
    COUNT(review_score) FILTER (WHERE is_single_seller)                 AS review_n,
    AVG(CASE WHEN is_failed THEN 1.0 ELSE 0 END)                        AS cancel_rate
FROM fct_seller_orders
WHERE in_window
GROUP BY 1, 2;