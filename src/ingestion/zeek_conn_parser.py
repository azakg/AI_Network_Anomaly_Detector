from typing import List, Dict


def parse_zeek_conn_log(file_path: str) -> List[Dict]:
    records = []
    headers = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#fields"):
                headers = line.split("\t")[1:]
                continue

            if line.startswith("#"):
                continue

            if not headers:
                continue

            values = line.split("\t")
            if len(values) != len(headers):
                continue

            record = dict(zip(headers, values))
            records.append(record)

    return records
