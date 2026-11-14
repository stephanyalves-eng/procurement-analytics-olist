-- grain: 1 row per order item; key: order_id + order_item_id
CREATE OR REPLACE VIEW stg_order_items AS
SELECT order_id,
       TRY_CAST(order_item_id AS INTEGER)          AS order_item_id,
       product_id,
       seller_id,
       TRY_CAST(shipping_limit_date AS TIMESTAMP)  AS shipping_limit_at,
       TRY_CAST(price         AS DECIMAL(12,2))    AS price,
       TRY_CAST(freight_value AS DECIMAL(12,2))    AS freight_value
FROM raw.order_items;