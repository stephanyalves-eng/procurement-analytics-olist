-- grain: 1 row per product; key: product_id
CREATE OR REPLACE VIEW stg_products AS
SELECT
    p.product_id,
    p.product_category_name                       AS category_pt,
    COALESCE(t.category, 'unknown')               AS category,
    TRY_CAST(p.product_weight_g   AS DOUBLE)      AS weight_g,
    TRY_CAST(p.product_length_cm  AS DOUBLE)
      * TRY_CAST(p.product_height_cm AS DOUBLE)
      * TRY_CAST(p.product_width_cm  AS DOUBLE)   AS volume_cm3,
    TRY_CAST(p.product_photos_qty AS INTEGER)     AS photos_qty,
    TRY_CAST(p.product_name_lenght        AS INTEGER) AS name_length,
    TRY_CAST(p.product_description_lenght AS INTEGER) AS description_length,
    p.product_category_name IS NULL               AS dq_missing_category
FROM raw.products p
LEFT JOIN stg_category_translation t ON t.category_pt = p.product_category_name;