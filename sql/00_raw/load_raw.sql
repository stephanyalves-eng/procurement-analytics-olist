-- sql/00_raw/load_raw.sql
-- camada raw: cópia fiel dos CSVs, tudo como texto
CREATE SCHEMA IF NOT EXISTS raw;

CREATE OR REPLACE TABLE raw.orders AS
SELECT * FROM read_csv('data/raw/olist_orders_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.order_items AS
SELECT * FROM read_csv('data/raw/olist_order_items_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.payments AS
SELECT * FROM read_csv('data/raw/olist_order_payments_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.reviews AS
SELECT * FROM read_csv('data/raw/olist_order_reviews_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.customers AS
SELECT * FROM read_csv('data/raw/olist_customers_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.sellers AS
SELECT * FROM read_csv('data/raw/olist_sellers_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.products AS
SELECT * FROM read_csv('data/raw/olist_products_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.geolocation AS
SELECT * FROM read_csv('data/raw/olist_geolocation_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE raw.category_translation AS
SELECT * FROM read_csv('data/raw/product_category_name_translation.csv', header = true, all_varchar = true);