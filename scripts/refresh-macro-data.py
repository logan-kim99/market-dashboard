"""Refresh public FRED observations for the deployed Finance Lab. No API keys required."""
import concurrent.futures
import csv
import datetime as dt
import io
import json
from pathlib import Path
import sys
import urllib.request

IDS = ['DGS10', 'FEDFUNDS', 'UNRATE', 'CPIAUCSL', 'T10Y3M', 'BAMLH0A0HYM2', 'T10YIE', 'DFII10']
HISTORY = {'T10Y3M', 'T10YIE', 'DFII10'}

def fetch_series(series_id):
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd=2005-01-01'
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (FinanceLab data refresh)'})
    with urllib.request.urlopen(request, timeout=45) as response:
        text = response.read().decode('utf-8-sig')
    records = list(csv.reader(io.StringIO(text)))
    if not records or records[0][0] not in ('DATE', 'observation_date'):
        raise ValueError(f'{series_id}: invalid provider response')
    rows = []
    for date, value in records[1:]:
        if value not in ('', '.'):
            rows.append([date, float(value)])
    if len(rows) < 20:
        raise ValueError(f'{series_id}: insufficient observations')
    if series_id in HISTORY:
        # Preserve the final known observation of every month plus latest daily changes.
        by_month = {row[0][:7]: row for row in rows}
        kept = {row[0]: row for row in by_month.values()}
        kept.update({row[0]: row for row in rows[-3:]})
        rows = [kept[date] for date in sorted(kept)]
    else:
        rows = rows[-16:] if series_id == 'CPIAUCSL' else rows[-3:]
    return series_id, rows

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        series = dict(pool.map(fetch_series, IDS))
    snapshot = {'schema': 1, 'fetchedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'source': 'https://fred.stlouisfed.org/', 'series': series}
    destination = Path(sys.argv[1] if len(sys.argv) > 1 else 'data/fred-series.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(snapshot, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    print(f'Refreshed {len(series)} FRED series.')

if __name__ == '__main__':
    main()

