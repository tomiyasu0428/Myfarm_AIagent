import os
import requests
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from datetime import date
from airtable import Airtable

try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except ModuleNotFoundError:  # pragma: no cover – optional dependency
    # dotenv is optional; skip loading .env if the library isn't available.
    pass

# ---------------------------------------------------------------------------
# Shared config helpers
# ---------------------------------------------------------------------------

_AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY") or os.getenv("AIRTABLE_PAT")
_AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not _AIRTABLE_API_KEY:
    raise EnvironmentError("AIRTABLE_API_KEY is not set. Add it to your environment or .env file.")
if not _AIRTABLE_BASE_ID:
    raise EnvironmentError("AIRTABLE_BASE_ID is not set. Add it to your environment or .env file.")


_HEADERS = {
    "Authorization": f"Bearer {_AIRTABLE_API_KEY}",
    "Content-Type": "application/json",
}


class AirtableError(RuntimeError):
    """Raised for any non-2xx response from the Airtable API."""


# ---------------------------------------------------------------------------
# Internal request helpers
# ---------------------------------------------------------------------------


def _request_json(method: str, url: str, **kwargs) -> Dict[str, Any]:
    """Wrapper around requests.request that raises on errors and returns JSON."""

    resp = requests.request(method, url, headers=_HEADERS, timeout=30, **kwargs)
    if not resp.ok:
        raise AirtableError(f"Airtable API error {resp.status_code}: {resp.text}")
    return resp.json()


# ---------------------------------------------------------------------------
# RECORD-LEVEL OPERATIONS
# ---------------------------------------------------------------------------


def airtable_get_records(
    table_name: str,
    view: Optional[str] = None,
    filter_formula: Optional[str] = None,
    max_records: Optional[int] = None,
) -> Dict[str, Any]:
    """Fetches records from an Airtable table.

    Args:
        table_name: The name of the table to query.
        view: Optional view name to use for ordering/filtering.
        filter_formula: Optional Airtable formula string for filtering.
        max_records: Optional maximum number of records to return.

    Returns:
        A dict containing a list of records under the key ``records``.
    """

    params = {}
    if view:
        params["view"] = view
    if filter_formula:
        params["filterByFormula"] = filter_formula
    if max_records is not None:
        params["maxRecords"] = str(max_records)

    query = urlencode(params)
    url = f"https://api.airtable.com/v0/{_AIRTABLE_BASE_ID}/{table_name}?{query}"
    data = _request_json("GET", url)
    return {"status": "success", "records": data.get("records", [])}


def airtable_create_record(table_name: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a single record in the specified table.

    Args:
        table_name: Target table.
        fields: Dict of field name -> value.
    """
    url = f"https://api.airtable.com/v0/{_AIRTABLE_BASE_ID}/{table_name}"
    payload = {"fields": fields}
    data = _request_json("POST", url, json=payload)
    return {"status": "success", "record": data}


def airtable_update_record(
    table_name: str,
    record_id: str,
    fields: Dict[str, Any],
) -> Dict[str, Any]:
    """Updates a record.

    Args:
        table_name: Target table
        record_id: The Airtable record ID (rec...)
        fields: Partial set of fields to update.
    """
    url = f"https://api.airtable.com/v0/{_AIRTABLE_BASE_ID}/{table_name}/{record_id}"
    payload = {"fields": fields}
    data = _request_json("PATCH", url, json=payload)
    return {"status": "success", "record": data}


def airtable_delete_record(table_name: str, record_id: str) -> Dict[str, Any]:
    """Deletes a record from a table."""
    url = f"https://api.airtable.com/v0/{_AIRTABLE_BASE_ID}/{table_name}/{record_id}"
    _request_json("DELETE", url)
    return {"status": "success", "deleted_record_id": record_id}


# ---------------------------------------------------------------------------
# TABLE-LEVEL (SCHEMA) OPERATIONS – Metadata API (PAT required)
# ---------------------------------------------------------------------------

_META_BASE = f"https://api.airtable.com/v0/meta/bases/{_AIRTABLE_BASE_ID}/tables"


def airtable_create_table(
    table_name: str,
    fields: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Creates a new table in the current base.

    Args:
        table_name: Name of the new table.
        fields: List of field definitions, e.g.::

            [
                {"name": "Name", "type": "singleLineText"},
                {"name": "Quantity", "type": "number", "options": {"precision": 0}},
            ]

    Returns:
        Dict with the created table metadata.
    """
    payload = {
        "name": table_name,
        "fields": fields,
    }
    data = _request_json("POST", _META_BASE, json=payload)
    return {"status": "success", "table": data}


def airtable_update_table(
    table_id: str,
    new_name: Optional[str] = None,
    fields: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Updates an existing table's name and/or fields.

    Args:
        table_id: The internal Airtable table ID (tbl...).
        new_name: New table name.
        fields: List of updated field definitions.
    """
    if not new_name and not fields:
        raise ValueError("Provide at least new_name or fields to update.")
    payload: Dict[str, Any] = {}
    if new_name:
        payload["name"] = new_name
    if fields is not None:
        payload["fields"] = fields

    url = f"{_META_BASE}/{table_id}"
    data = _request_json("PATCH", url, json=payload)
    return {"status": "success", "table": data}


def airtable_delete_table(table_id: str) -> Dict[str, Any]:
    """Deletes (permanently) a table from the base."""
    url = f"{_META_BASE}/{table_id}"
    _request_json("DELETE", url)
    return {"status": "success", "deleted_table_id": table_id}


def airtable_list_tables() -> Dict[str, Any]:
    """Lists all tables in the base with their schema."""
    data = _request_json("GET", _META_BASE)
    return {"status": "success", "tables": data.get("tables", [])}


# Helper to get Airtable client


def _get_table(table_name: str) -> Airtable:
    return Airtable(_AIRTABLE_BASE_ID, table_name, api_key=_AIRTABLE_API_KEY)


def get_today_tasks(worker_name: str) -> str:
    """Returns today's tasks for the given worker (not completed)."""
    try:
        task_table = _get_table("作業タスク")
        today = date.today().isoformat()
        formula = (
            f"AND(IS_SAME({{予定日}}, '{today}', 'day'), "
            f"NOT({{ステータス}} = '完了'), "
            f"FIND('{worker_name}', ARRAYJOIN({{担当者}})))"
        )
        tasks = task_table.get_all(formula=formula)
        if not tasks:
            return f"{worker_name}さんの本日のタスクはありません。"
        task_list = []
        for task in tasks:
            fields = task.get("fields", {})
            task_name = fields.get("タスク名", "N/A")
            field_name = fields.get("圃場名 (from 圃場データ) (from 関連する作付計画)", ["N/A"])[0]
            task_list.append(f"・{task_name} (圃場: {field_name})")
        return f"{worker_name}さんの本日のタスク:\n" + "\n".join(task_list)
    except Exception as e:
        return f"タスクの取得中にエラーが発生しました: {e}"


def get_field_info(field_name: str) -> str:
    """圃場名（`作業場所`）を指定して、関連する作付け情報や土壌データを取得する。"""
    try:
        table = _get_table("圃場マスタ")
        records = table.get_all(formula=f"{{作業場所}} = '{field_name}'")
        if not records:
            return f"「{field_name}」という名前の圃場は見つかりませんでした。"
        # 1つの圃場名に複数のレコードが返ることはないと想定
        return f"圃場「{field_name}」の情報:\n{records[0]['fields']}"
    except Exception as e:
        return f"エラー: 圃場情報の取得中に問題が発生しました - {e}"


def create_daily_report(reporter_name: str, content: str) -> str:
    """LINEからの報告を日報ログテーブルに新規作成する。

    Args:
        reporter_name: 報告者の名前。
        content: 報告内容のテキスト。

    Returns:
        処理結果を示すメッセージ文字列。
    """
    try:
        today_str = date.today().isoformat()
        fields = {
            "報告日": today_str,
            "報告者": reporter_name,
            "報告内容": content,
        }
        result = airtable_create_record("日報ログ", fields)
        record_id = result.get("record", {}).get("id")
        return f"日報を作成しました。(レコードID: {record_id})"
    except AirtableError as e:
        return f"エラー: 日報の作成に失敗しました - {e}"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"


def update_task_status(record_id: str, status: str) -> str:
    """作業タスクのステータスを更新する。

    Args:
        record_id: 更新対象の作業タスクのレコードID。
        status: 新しいステータス（例: "完了", "保留"）。

    Returns:
        処理結果を示すメッセージ文字列。
    """
    try:
        # "作業タスク" テーブルの "ステータス" フィールドを更新
        fields = {"ステータス": status}
        result = airtable_update_record("作業タスク", record_id, fields)
        updated_id = result.get("record", {}).get("id")
        return f"タスク(ID: {updated_id})のステータスを「{status}」に更新しました。"
    except AirtableError as e:
        return f"エラー: タスクステータスの更新に失敗しました - {e}"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"


def search_materials(query: str, category: Optional[str] = None, crop: Optional[str] = None) -> str:
    """資材マスターテーブルから、指定された条件で資材を検索する。

    Args:
        query: 検索キーワード。資材名や主成分などを対象に部分一致で検索する。
        category: "農薬", "肥料" などの資材分類で絞り込む（任意）。
        crop: 適用作物名で絞り込む（任意）。

    Returns:
        検索結果のリスト、または見つからなかった場合のメッセージ。
    """
    try:
        table = _get_table("資材マスター")

        # フィルタ式を動的に構築
        formulas = []
        if query:
            # 複数のフィールドをORで検索
            or_clauses = [
                f"FIND('{query}', {{資材名}})",
                f"FIND('{query}', {{主成分}})",
                f"FIND('{query}', {{メーカー}})",
            ]
            formulas.append(f"OR({', '.join(or_clauses)})")

        if category:
            formulas.append(f"{{資材分類}} = '{category}'")

        if crop:
            formulas.append(f"FIND('{crop}', {{適用作物}})")

        filter_formula = f"AND({', '.join(formulas)})"

        records = table.get_all(formula=filter_formula)

        if not records:
            return "条件に合う資材は見つかりませんでした。"

        results = [f"「{query}」に一致する資材が{len(records)}件見つかりました："]
        for record in records:
            fields = record["fields"]
            info = (
                f"- {fields.get('資材名', 'N/A')} "
                f"({fields.get('メーカー', 'N/A')}, {fields.get('規格・容量', 'N/A')})\n"
                f"  分類: {fields.get('資材分類', 'N/A')}\n"
                f"  適用作物: {fields.get('適用作物', 'N/A')}"
            )
            results.append(info)

        return "\n".join(results)
    except Exception as e:
        return f"エラー: 資材の検索中に予期せぬ問題が発生しました - {e}"
