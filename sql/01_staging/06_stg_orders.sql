-- grain: 1 row per order; key: order_id
CREATE OR REPLACE VIEW stg_orders AS
WITH t AS (
    SELECT order_id, customer_id, order_status,
           TRY_CAST(order_purchase_timestamp      AS TIMESTAMP) AS purchased_at,
           TRY_CAST(order_approved_at             AS TIMESTAMP) AS approved_at,
           TRY_CAST(order_delivered_carrier_date  AS TIMESTAMP) AS delivered_carrier_at,
           TRY_CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_at,
           TRY_CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_at
    FROM raw.orders)
SELECT
    t.*,
    order_status IN ('canceled', 'unavailable')                               AS is_failed,
    approved_at IS NULL                                                       AS dq_missing_approval,
    COALESCE(order_status = 'delivered' AND delivered_customer_at IS NULL, false) AS dq_missing_delivery_date,
    COALESCE(order_status = 'delivered' AND delivered_carrier_at IS NULL, false)  AS dq_missing_carrier_date,
    COALESCE(delivered_carrier_at < approved_at, false)                       AS dq_carrier_before_approval,
    COALESCE(delivered_customer_at < delivered_carrier_at, false)             AS dq_customer_before_carrier
FROM t;