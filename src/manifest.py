# src/manifest.py
import csv, hashlib, datetime
from pathlib import Path

RAW = Path("data/raw")
rows = []
for f in sorted(RAW.glob("*.csv")):
    data = f.read_bytes()
    rows.append({
        "file": f.name,
        "rows": data.count(b"\n") - 1,   # aproximado; a contagem oficial é a do DuckDB na Etapa 2
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "downloaded_at": datetime.date.today().isoformat(),
    })
with open("data/manifest.csv", "w", newline="") as out:
    w = csv.DictWriter(out, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} arquivos registrados")
