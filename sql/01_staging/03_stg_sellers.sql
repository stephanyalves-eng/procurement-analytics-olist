-- grain: 1 row per seller; key: seller_id
CREATE OR REPLACE VIEW stg_sellers AS
SELECT seller_id,
       LPAD(seller_zip_code_prefix, 5, '0') AS zip_prefix,
       LOWER(TRIM(seller_city))             AS seller_city,
       UPPER(TRIM(seller_state))            AS seller_state
FROM raw.sellers;