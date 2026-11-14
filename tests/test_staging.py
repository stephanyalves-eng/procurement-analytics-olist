# tests/test_staging.py
import duckdb
import pytest


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect("data/olist.duckdb", read_only=True)
    yield c
    c.close()


def val(con, sql):
    return con.sql(sql).fetchall()[0][0]


@pytest.mark.parametrize("view, raw_table", [
    ("stg_orders", "orders"), ("stg_order_items", "order_items"),
    ("stg_products", "products"), ("stg_sellers", "sellers"), ("stg_customers", "customers"),
])
def test_one_to_one_row_counts(con, view, raw_table):
    assert val(con, f"SELECT COUNT(*) FROM {view}") == val(con, f"SELECT COUNT(*) FROM raw.{raw_table}")


@pytest.mark.parametrize("view, key", [
    ("stg_orders", "order_id"), ("stg_products", "product_id"), ("stg_sellers", "seller_id"),
    ("stg_customers", "customer_id"), ("stg_reviews", "order_id"), ("stg_payments", "order_id"),
    ("stg_geolocation", "zip_prefix"), ("stg_category_translation", "category_pt"),
    ("stg_order_items", "order_id || '-' || order_item_id"),
])
def test_unique_keys(con, view, key):
    assert val(con, f"SELECT COUNT(*) - COUNT(DISTINCT {key}) FROM {view}") == 0


def test_one_review_per_reviewed_order(con):
    assert val(con, "SELECT COUNT(*) FROM stg_reviews") == \
        val(con, "SELECT COUNT(DISTINCT order_id) FROM raw.reviews")


def test_every_product_has_category_label(con):
    assert val(con, "SELECT COUNT(*) FROM stg_products WHERE category IS NULL") == 0


def test_all_categories_translated(con):
    assert val(con, "SELECT COUNT(*) FROM stg_products "
                    "WHERE category = 'unknown' AND NOT dq_missing_category") == 0


def test_values_and_scores_valid(con):
    assert val(con, "SELECT COUNT(*) FROM stg_order_items WHERE price <= 0 OR freight_value < 0") == 0
    assert val(con, "SELECT COUNT(*) FROM stg_reviews WHERE review_score NOT BETWEEN 1 AND 5") == 0


def test_dq_flags_never_null(con):
    assert val(con, "SELECT COUNT(*) FROM stg_orders WHERE dq_carrier_before_approval IS NULL "
                    "OR dq_customer_before_carrier IS NULL OR dq_missing_delivery_date IS NULL") == 0


def test_flags_match_profile(con):
    # same counts measured in docs/data_quality.md
    assert val(con, "SELECT COUNT(*) FROM stg_orders WHERE dq_carrier_before_approval") == 1359
    assert val(con, "SELECT COUNT(*) FROM stg_products WHERE dq_missing_category") == 610