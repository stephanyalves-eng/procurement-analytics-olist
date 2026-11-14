# tests/test_marts.py
import duckdb
import pytest


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect("data/olist.duckdb", read_only=True)
    yield c
    c.close()


def val(con, sql):
    return con.sql(sql).fetchall()[0][0]


WINDOW_SPEND = "SELECT SUM(price) FROM fct_order_items WHERE in_window AND is_valid_status"


def test_fact_keeps_every_item(con):
    assert val(con, "SELECT COUNT(*) FROM fct_order_items") == \
        val(con, "SELECT COUNT(*) FROM stg_order_items")


@pytest.mark.parametrize("table, key", [
    ("fct_order_items", "order_id || '-' || order_item_id"),
    ("fct_seller_orders", "seller_id || '-' || order_id"),
    ("dim_sellers", "seller_id"),
    ("mart_seller_monthly", "seller_id || '-' || CAST(month AS VARCHAR)"),
    ("mart_category_concentration", "category"),
    ("mart_seller_scorecard_base", "seller_id"),
])
def test_unique_grain(con, table, key):
    assert val(con, f"SELECT COUNT(*) - COUNT(DISTINCT {key}) FROM {table}") == 0


@pytest.mark.parametrize("sql", [
    "SELECT SUM(spend_brl) FROM fct_seller_orders WHERE in_window AND is_valid_status",
    "SELECT SUM(spend_brl) FROM mart_seller_scorecard_base",
    "SELECT SUM(spend_brl) FROM mart_seller_monthly",
])
def test_spend_reconciles(con, sql):
    assert val(con, sql) == val(con, WINDOW_SPEND)


def test_category_spend_plus_unknown_reconciles(con):
    known = val(con, "SELECT SUM(spend_brl) FROM mart_category_concentration")
    unknown = val(con, "SELECT CAST(SUM(price) AS DOUBLE) FROM fct_order_items "
                       "WHERE in_window AND is_valid_status AND category = 'unknown'")
    total = float(val(con, WINDOW_SPEND))
    assert abs(known + unknown - total) < 0.01


@pytest.mark.parametrize("col", [
    "dispatch_on_time_rate", "customer_on_time_rate", "cancel_rate", "pct_negative_reviews",
])
def test_rates_between_0_and_1(con, col):
    assert val(con, f"SELECT COUNT(*) FROM mart_seller_scorecard_base "
                    f"WHERE {col} < 0 OR {col} > 1") == 0


def test_lead_time_not_negative(con):
    assert val(con, "SELECT COUNT(*) FROM fct_order_items WHERE dispatch_lead_days < 0") == 0


def test_hhi_range(con):
    assert val(con, "SELECT COUNT(*) FROM mart_category_concentration "
                    "WHERE hhi <= 0 OR hhi > 10000.001") == 0


def test_exports_exist():
    from pathlib import Path
    for f in ["scorecard_base.parquet", "seller_monthly.csv", "category_concentration.csv"]:
        assert Path("data/processed", f).stat().st_size > 0