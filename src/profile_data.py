# src/profile_data.py
"""Data quality diagnostics for the raw layer. Writes docs/data_quality.md."""
from datetime import date
from pathlib import Path

import duckdb

con = duckdb.connect("data/olist.duckdb", read_only=True)


def one(sql):
    return con.sql(sql).fetchall()[0][0]


def md_table(sql):
    rel = con.sql(sql)
    cols, data = rel.columns, rel.fetchall()
    lines = ["| " + " | ".join(cols) + " |", "|" + " --- |" * len(cols)]
    for r in data:
        lines.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(lines)


def ts(col):
    return f"TRY_CAST({col} AS TIMESTAMP)"


ORDER_TS = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
            "order_delivered_customer_date", "order_estimated_delivery_date"]
IN_BR = ("TRY_CAST(geolocation_lat AS DOUBLE) BETWEEN -34 AND 5.5 "
         "AND TRY_CAST(geolocation_lng AS DOUBLE) BETWEEN -74 AND -34")
MULTI = ("SELECT order_id FROM raw.order_items GROUP BY order_id "
         "HAVING COUNT(DISTINCT seller_id) > 1")

N_ORDERS = "SELECT COUNT(*) FROM raw.orders"
N_ITEMS = "SELECT COUNT(*) FROM raw.order_items"
N_REVIEWS = "SELECT COUNT(*) FROM raw.reviews"

CHECKS = [
    # (group, check, numerator SQL, denominator SQL)
    ("Keys", "duplicate order_id in orders",
     "SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM raw.orders", N_ORDERS),
    ("Keys", "duplicate order_id + order_item_id",
     "SELECT COUNT(*) - COUNT(DISTINCT order_id || '-' || order_item_id) FROM raw.order_items", N_ITEMS),
    ("Keys", "duplicate seller_id",
     "SELECT COUNT(*) - COUNT(DISTINCT seller_id) FROM raw.sellers", "SELECT COUNT(*) FROM raw.sellers"),
    ("Keys", "duplicate product_id",
     "SELECT COUNT(*) - COUNT(DISTINCT product_id) FROM raw.products", "SELECT COUNT(*) FROM raw.products"),
    ("Keys", "duplicate customer_id",
     "SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM raw.customers", "SELECT COUNT(*) FROM raw.customers"),

    ("Orphans", "items without order",
     "SELECT COUNT(*) FROM raw.order_items ANTI JOIN raw.orders USING (order_id)", N_ITEMS),
    ("Orphans", "items with unknown seller",
     "SELECT COUNT(*) FROM raw.order_items ANTI JOIN raw.sellers USING (seller_id)", N_ITEMS),
    ("Orphans", "items with unknown product",
     "SELECT COUNT(*) FROM raw.order_items ANTI JOIN raw.products USING (product_id)", N_ITEMS),
    ("Orphans", "reviews without order",
     "SELECT COUNT(*) FROM raw.reviews ANTI JOIN raw.orders USING (order_id)", N_REVIEWS),
    ("Orphans", "orders without any item",
     "SELECT COUNT(*) FROM raw.orders ANTI JOIN raw.order_items USING (order_id)", N_ORDERS),

    ("Reviews", "repeated review_id",
     "SELECT COUNT(*) - COUNT(DISTINCT review_id) FROM raw.reviews", N_REVIEWS),
    ("Reviews", "orders with more than one review",
     "SELECT COUNT(*) FROM (SELECT order_id FROM raw.reviews GROUP BY order_id HAVING COUNT(*) > 1)",
     "SELECT COUNT(DISTINCT order_id) FROM raw.reviews"),
    ("Reviews", "score missing or outside 1-5",
     "SELECT COUNT(*) FROM raw.reviews WHERE TRY_CAST(review_score AS INTEGER) IS NULL "
     "OR TRY_CAST(review_score AS INTEGER) NOT BETWEEN 1 AND 5", N_REVIEWS),

    ("Products", "products without category",
     "SELECT COUNT(*) FROM raw.products WHERE product_category_name IS NULL",
     "SELECT COUNT(*) FROM raw.products"),
    ("Products", "categories without English translation",
     "SELECT COUNT(DISTINCT product_category_name) FROM raw.products "
     "ANTI JOIN raw.category_translation USING (product_category_name) "
     "WHERE product_category_name IS NOT NULL",
     "SELECT COUNT(DISTINCT product_category_name) FROM raw.products"),
    ("Products", "items whose product has no category",
     "SELECT COUNT(*) FROM raw.order_items JOIN raw.products USING (product_id) "
     "WHERE product_category_name IS NULL", N_ITEMS),

    ("Multi-seller", "orders with more than one seller",
     f"SELECT COUNT(*) FROM ({MULTI})", "SELECT COUNT(DISTINCT order_id) FROM raw.order_items"),
    ("Multi-seller", "items in multi-seller orders",
     f"SELECT COUNT(*) FROM raw.order_items WHERE order_id IN ({MULTI})", N_ITEMS),

    ("Dates", "timestamps that fail to parse (5 columns)",
     "SELECT " + " + ".join(
         f"SUM(CASE WHEN {c} IS NOT NULL AND {ts(c)} IS NULL THEN 1 ELSE 0 END)" for c in ORDER_TS)
     + " FROM raw.orders", "SELECT COUNT(*) * 5 FROM raw.orders"),
    ("Dates", "approval date missing",
     "SELECT COUNT(*) FROM raw.orders WHERE order_approved_at IS NULL", N_ORDERS),
    ("Dates", "delivered without customer delivery date",
     "SELECT COUNT(*) FROM raw.orders WHERE order_status = 'delivered' "
     "AND order_delivered_customer_date IS NULL",
     "SELECT COUNT(*) FROM raw.orders WHERE order_status = 'delivered'"),
    ("Dates", "delivered without carrier date",
     "SELECT COUNT(*) FROM raw.orders WHERE order_status = 'delivered' "
     "AND order_delivered_carrier_date IS NULL",
     "SELECT COUNT(*) FROM raw.orders WHERE order_status = 'delivered'"),
    ("Dates", "carrier date before approval",
     f"SELECT COUNT(*) FROM raw.orders WHERE {ts('order_delivered_carrier_date')} < {ts('order_approved_at')}",
     "SELECT COUNT(*) FROM raw.orders WHERE order_delivered_carrier_date IS NOT NULL "
     "AND order_approved_at IS NOT NULL"),
    ("Dates", "customer delivery before carrier date",
     f"SELECT COUNT(*) FROM raw.orders WHERE {ts('order_delivered_customer_date')} "
     f"< {ts('order_delivered_carrier_date')}",
     "SELECT COUNT(*) FROM raw.orders WHERE order_delivered_customer_date IS NOT NULL "
     "AND order_delivered_carrier_date IS NOT NULL"),
    ("Dates", "approval before purchase",
     f"SELECT COUNT(*) FROM raw.orders WHERE {ts('order_approved_at')} < {ts('order_purchase_timestamp')}",
     "SELECT COUNT(*) FROM raw.orders WHERE order_approved_at IS NOT NULL"),

    ("Geolocation", "zip prefixes with more than one coordinate",
     "SELECT COUNT(*) FROM (SELECT geolocation_zip_code_prefix FROM raw.geolocation GROUP BY 1 "
     "HAVING COUNT(DISTINCT geolocation_lat || ',' || geolocation_lng) > 1)",
     "SELECT COUNT(DISTINCT geolocation_zip_code_prefix) FROM raw.geolocation"),
    ("Geolocation", "points outside Brazil",
     f"SELECT COUNT(*) FROM raw.geolocation WHERE NOT ({IN_BR})", "SELECT COUNT(*) FROM raw.geolocation"),
    ("Geolocation", "sellers whose zip prefix has no coordinate",
     "SELECT COUNT(*) FROM raw.sellers WHERE LPAD(seller_zip_code_prefix, 5, '0') NOT IN "
     "(SELECT LPAD(geolocation_zip_code_prefix, 5, '0') FROM raw.geolocation)",
     "SELECT COUNT(*) FROM raw.sellers"),
    ("Geolocation", "customers whose zip prefix has no coordinate",
     "SELECT COUNT(*) FROM raw.customers WHERE LPAD(customer_zip_code_prefix, 5, '0') NOT IN "
     "(SELECT LPAD(geolocation_zip_code_prefix, 5, '0') FROM raw.geolocation)",
     "SELECT COUNT(*) FROM raw.customers"),

    ("Values", "items with price missing, zero or negative",
     "SELECT COUNT(*) FROM raw.order_items WHERE TRY_CAST(price AS DOUBLE) IS NULL "
     "OR TRY_CAST(price AS DOUBLE) <= 0", N_ITEMS),
    ("Values", "items with freight missing or negative",
     "SELECT COUNT(*) FROM raw.order_items WHERE TRY_CAST(freight_value AS DOUBLE) IS NULL "
     "OR TRY_CAST(freight_value AS DOUBLE) < 0", N_ITEMS),
]

TABLES = ["orders", "order_items", "payments", "reviews", "customers",
          "sellers", "products", "geolocation", "category_translation"]

report = [
    "# Data quality report", "",
    f"Generated by `python -m src.profile_data` on {date.today().isoformat()} from the raw layer.",
    "Every cleaning rule in staging and marts must point to a row of this report.", "",
    "## Measured anomalies", "",
    "| Group | Check | Affected | Base | % | Decision |",
    "| --- | --- | ---: | ---: | ---: | --- |",
]

print(f"{'group':<14}{'check':<46}{'affected':>10}{'%':>9}")
for group, check, num_sql, den_sql in CHECKS:
    n, d = one(num_sql), one(den_sql)
    pct = 100 * n / d if d else 0
    print(f"{group:<14}{check:<46}{n:>10,}{pct:>8.2f}%")
    report.append(f"| {group} | {check} | {n:,} | {d:,} | {pct:.2f}% |  |")

report += ["", "## Order status", "", md_table(
    "SELECT order_status AS status, COUNT(*) AS orders, "
    "ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct "
    "FROM raw.orders GROUP BY 1 ORDER BY 2 DESC")]

report += ["", "## Orders per month", "", md_table(
    f"SELECT strftime({ts('order_purchase_timestamp')}, '%Y-%m') AS month, COUNT(*) AS orders "
    "FROM raw.orders GROUP BY 1 ORDER BY 1")]

report += ["", "**Decision:** analysis window Jan 2017 to Aug 2018 (20 months). "
           "Excluded Sep-Dec 2016 and Sep-Oct 2018: 349 orders (0.35%), volume too low "
           "for stable monthly rates. Persistence split at 2018-01-01 (balanced by order volume)."]

null_sql = " UNION ALL ".join(
    f"SELECT '{t}' AS table_name, column_name, null_percentage FROM (SUMMARIZE raw.{t}) "
    f"WHERE TRY_CAST(REPLACE(CAST(null_percentage AS VARCHAR), '%', '') AS DOUBLE) > 0"
    for t in TABLES)
report += ["", "## Columns with nulls", "", md_table(null_sql)]

Path("docs").mkdir(exist_ok=True)
Path("docs/data_quality.md").write_text("\n".join(report) + "\n", encoding="utf-8")
con.close()
print("\nReport written to docs/data_quality.md")