-- grain: 1 row per seller (analysis window); key: seller_id
-- raw metrics only; percentiles and score are computed in Python (step 6)
CREATE OR REPLACE TABLE mart_seller_scorecard_base AS
SELECT
    seller_id,
    COUNT(*) FILTER (WHERE is_valid_status)                                  AS n_orders,
    SUM(spend_brl) FILTER (WHERE is_valid_status)                            AS spend_brl,
    SUM(freight_brl) FILTER (WHERE is_valid_status)                          AS freight_brl,
    CAST(SUM(freight_brl) FILTER (WHERE is_valid_status) AS DOUBLE)
      / NULLIF(CAST(SUM(spend_brl) FILTER (WHERE is_valid_status) AS DOUBLE), 0) AS freight_ratio,
    AVG(dispatch_on_time) FILTER (WHERE is_single_seller)                    AS dispatch_on_time_rate,
    COUNT(dispatch_on_time) FILTER (WHERE is_single_seller)                  AS n_dispatch_obs,
    QUANTILE_CONT(dispatch_lead_days, 0.9) FILTER (WHERE is_single_seller)   AS dispatch_lead_p90_days,
    AVG(customer_on_time) FILTER (WHERE is_single_seller)                    AS customer_on_time_rate,
    AVG(review_score) FILTER (WHERE is_single_seller)                        AS review_mean,
    COUNT(review_score) FILTER (WHERE is_single_seller)                      AS review_n,
    AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0 END)
      FILTER (WHERE is_single_seller AND review_score IS NOT NULL)           AS pct_negative_reviews,
    AVG(CASE WHEN is_failed THEN 1.0 ELSE 0 END)                             AS cancel_rate,
    AVG(distance_km)                                                         AS avg_distance_km
FROM fct_seller_orders
WHERE in_window
GROUP BY seller_id;