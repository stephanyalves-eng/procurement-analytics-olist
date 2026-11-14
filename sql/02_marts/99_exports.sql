COPY (
    SELECT b.*, d.main_category, d.seller_state
    FROM mart_seller_scorecard_base b JOIN dim_sellers d USING (seller_id)
) TO 'data/processed/scorecard_base.parquet' (FORMAT PARQUET);
COPY mart_seller_monthly         TO 'data/processed/seller_monthly.csv'         (HEADER, DELIMITER ',');
COPY mart_category_concentration TO 'data/processed/category_concentration.csv' (HEADER, DELIMITER ',');