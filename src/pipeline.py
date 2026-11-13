# src/pipeline.py
import duckdb
from pathlib import Path

DB = "data/olist.duckdb"
LAYERS = ["sql/00_raw", "sql/01_staging", "sql/02_marts"]

def run():
    con = duckdb.connect(DB)
    for layer in LAYERS:
        for f in sorted(Path(layer).glob("*.sql")):
            print(f"-> {f}")
            con.execute(f.read_text(encoding="utf-8"))
    con.close()

if __name__ == "__main__":
    run()