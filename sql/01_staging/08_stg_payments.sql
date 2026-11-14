-- grain: 1 row per order; key: order_id
CREATE OR REPLACE VIEW stg_payments AS
SELECT order_id,
       SUM(TRY_CAST(payment_value AS DECIMAL(12,2)))                       AS payment_total,
       MAX(TRY_CAST(payment_installments AS INTEGER))                      AS max_installments,
       ARG_MAX(payment_type, TRY_CAST(payment_value AS DECIMAL(12,2)))     AS main_payment_type,
       COUNT(*)                                                            AS n_payments
FROM raw.payments
GROUP BY order_id;