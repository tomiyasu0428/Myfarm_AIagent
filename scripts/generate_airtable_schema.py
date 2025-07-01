"""generate_airtable_schema.py
Airtable Metadata API を利用して、指定された Base 内のすべてのテーブルと
フィールド情報を取得し、docs/Airtable_Schema_Summary.md を自動生成するスクリプト。

メタデータ API は Personal Access Token (PAT) でのみ利用できます。
`.env` に下記の環境変数を追加してください。

AIRTABLE_API_KEY   = pat... (scope: schema.bases:read)
AIRTABLE_BASE_ID   = app...

使い方:
    python scripts/generate_airtable_schema.py
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
OUTPUT_PATH = Path("docs/Airtable_Schema_Summary.md")

if not API_KEY or not BASE_ID:
    sys.exit("AIRTABLE_API_KEY または AIRTABLE_BASE_ID が .env に設定されていません。")

METADATA_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

resp = requests.get(METADATA_URL, headers=HEADERS, timeout=30)
if resp.status_code != 200:
    sys.exit(f"Metadata API からスキーマを取得できませんでした: {resp.status_code} {resp.text}")

data = resp.json()

lines = [
    "# Airtable Database Schema Summary",
    "",
    f"_Last updated: {datetime.utcnow().isoformat()}Z_",
    "",
    "---",
    "",
]

for table in data.get("tables", []):
    t_name = table["name"]
    t_id = table["id"]
    lines.append(f"## Table: {t_name} (ID: {t_id})\n")
    lines.append("### Fields:")
    for field in table.get("fields", []):
        fname = field["name"]
        ftype = field["type"]
        lines.append(f"- **{fname}**: {ftype}")
    lines.append("\n---\n")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"Schema summary written to {OUTPUT_PATH}")
