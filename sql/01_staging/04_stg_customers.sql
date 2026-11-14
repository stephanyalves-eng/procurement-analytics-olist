-- grain: 1 row per customer_id (one per order); key: customer_id
CREATE OR REPLACE VIEW stg_customers AS
SELECT customer_id,
       customer_unique_id,
       LPAD(customer_zip_code_prefix, 5, '0') AS zip_prefix,
       LOWER(TRIM(customer_city))             AS customer_city,
       UPPER(TRIM(customer_state))            AS customer_state
FROM raw.customers;