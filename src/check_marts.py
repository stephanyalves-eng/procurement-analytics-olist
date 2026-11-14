# src/check_marts.py
"""Business sanity check of the marts. Run after the pipeline."""
import duckdb

con = duckdb.connect("data/olist.duckdb", read_only=True)
W = "FROM fct_seller_orders WHERE in_window"
S = "FROM mart_seller_scorecard_base"
C = "FROM mart_category_concentration"

CHECKS = [
    ("Sellers with orders in window", f"SELECT COUNT(*) {S} WHERE n_orders > 0", "int"),
    ("Eligible sellers (30+ orders)", f"SELECT COUNT(*) {S} WHERE n_orders >= 30", "int"),
    ("Spend covered by eligible sellers",
     f"SELECT CAST(SUM(spend_brl) FILTER (WHERE n_orders >= 30) AS DOUBLE) "
     f"/ CAST(SUM(spend_brl) AS DOUBLE) {S}", "pct"),
    ("Total spend in window (BRL)", f"SELECT CAST(SUM(spend_brl) AS DOUBLE) {S}", "money"),
    ("Sellers that make 80% of spend",
     "SELECT MIN(rn) FROM (SELECT ROW_NUMBER() OVER (ORDER BY spend_brl DESC) AS rn, "
     "CAST(SUM(spend_brl) OVER (ORDER BY spend_brl DESC ROWS UNBOUNDED PRECEDING) AS DOUBLE) "
     f"/ CAST(SUM(spend_brl) OVER () AS DOUBLE) AS cum {S} WHERE spend_brl > 0) WHERE cum >= 0.8",
     "int"),
    ("Dispatch on time (single-seller orders)",
     f"SELECT AVG(dispatch_on_time) {W} AND is_single_seller", "pct"),
    ("Customer on time (single-seller orders)",
     f"SELECT AVG(customer_on_time) {W} AND is_single_seller", "pct"),
    ("Average review score", f"SELECT AVG(review_score) {W} AND is_single_seller", "num"),
    ("Cancel rate (orders)", f"SELECT AVG(CASE WHEN is_failed THEN 1.0 ELSE 0 END) {W}", "pct"),
    ("Categories analysed", f"SELECT COUNT(*) {C}", "int"),
    ("Categories with high concentration", f"SELECT COUNT(*) {C} WHERE concentration_level = 'high'", "int"),
    ("Categories with single-source risk", f"SELECT COUNT(*) {C} WHERE single_source_risk", "int"),
]

FMT = {"int": "{:,.0f}", "pct": "{:.1%}", "num": "{:.2f}", "money": "{:,.0f}"}

for label, sql, kind in CHECKS:
    value = con.sql(sql).fetchall()[0][0]
    shown = "n/a" if value is None else FMT[kind].format(float(value))
    print(f"{label:<45}{shown:>15}")
con.close()