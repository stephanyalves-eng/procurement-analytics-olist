# src/check_raw.py
import duckdb

EXPECTED = {
    "orders": 99441, "order_items": 112650, "payments": 103886,
    "reviews": 99224, "customers": 99441, "sellers": 3095,
    "products": 32951, "geolocation": 1000163, "category_translation": 71,
}

con = duckdb.connect("data/olist.duckdb", read_only=True)
print(f"{'tabela':<22}{'linhas':>12}{'esperado':>12}  status")
for table, exp in EXPECTED.items():
    n = con.sql(f"SELECT COUNT(*) FROM raw.{table}").fetchall()[0][0]
    status = "ok" if n == exp else "DIVERGE"
    print(f"{table:<22}{n:>12,}{exp:>12,}  {status}")
con.close()