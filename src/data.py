"""Read-only access to the DuckDB marts, from any folder (notebooks included)."""
from pathlib import Path

import duckdb

DB = Path(__file__).resolve().parents[1] / "data" / "olist.duckdb"


def q(sql):
    """Run a query and return a pandas DataFrame. Opens and closes the connection
    each time, so the pipeline can rebuild the database while a notebook is open."""
    with duckdb.connect(str(DB), read_only=True) as con:
        return con.sql(sql).df()
