-- grain: 1 row per order item; key: order_id + order_item_id
CREATE OR REPLACE TABLE fct_order_items AS
WITH sellers_per_order AS (
    SELECT order_id, COUNT(DISTINCT seller_id) AS n_sellers
    FROM stg_order_items GROUP BY order_id)
SELECT
    i.order_id, i.order_item_id, i.seller_id, i.product_id,
    p.category, p.weight_g, p.volume_cm3,
    s.seller_state, c.customer_state,
    o.order_status, o.purchased_at, o.approved_at, o.delivered_carrier_at,
    o.delivered_customer_at, o.estimated_delivery_at, i.shipping_limit_at,
    i.price, i.freight_value, r.review_score,
    o.is_failed,
    NOT o.is_failed                                                    AS is_valid_status,
    spo.n_sellers = 1                                                  AS is_single_seller,
    o.purchased_at >= DATE '2017-01-01'
      AND o.purchased_at < DATE '2018-09-01'                           AS in_window,
    o.dq_carrier_before_approval, o.dq_customer_before_carrier,
    -- seller SLA: dispatch vs seller shipping limit (does not use approval date)
    CASE WHEN o.delivered_carrier_at IS NULL THEN NULL
         WHEN o.delivered_carrier_at <= i.shipping_limit_at THEN 1 ELSE 0 END AS dispatch_on_time,
    -- end-to-end: compared by date because the estimate is always 00:00
    CASE WHEN o.delivered_customer_at IS NULL OR o.dq_customer_before_carrier THEN NULL
         WHEN CAST(o.delivered_customer_at AS DATE) <= CAST(o.estimated_delivery_at AS DATE)
         THEN 1 ELSE 0 END                                             AS customer_on_time,
    CASE WHEN o.approved_at IS NULL OR o.dq_carrier_before_approval THEN NULL
         ELSE DATE_DIFF('minute', o.approved_at, o.delivered_carrier_at) / 1440.0
    END                                                                AS dispatch_lead_days,
    CAST(i.freight_value AS DOUBLE) / NULLIF(CAST(i.price AS DOUBLE), 0) AS freight_ratio,
    6371 * 2 * ASIN(SQRT(
        POWER(SIN(RADIANS(gc.lat - gs.lat) / 2), 2)
      + COS(RADIANS(gs.lat)) * COS(RADIANS(gc.lat))
      * POWER(SIN(RADIANS(gc.lng - gs.lng) / 2), 2)))                  AS distance_km
FROM stg_order_items i
JOIN stg_orders o            USING (order_id)
JOIN sellers_per_order spo   USING (order_id)
LEFT JOIN stg_products p     USING (product_id)
LEFT JOIN stg_sellers s      USING (seller_id)
LEFT JOIN stg_customers c    ON c.customer_id = o.customer_id
LEFT JOIN stg_geolocation gs ON gs.zip_prefix = s.zip_prefix
LEFT JOIN stg_geolocation gc ON gc.zip_prefix = c.zip_prefix
LEFT JOIN stg_reviews r      USING (order_id);