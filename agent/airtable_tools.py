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


def get_today_tasks(worker_name: Optional[str] = None) -> str:
    """今日予定の作業タスクを取得します。

    Args:
        worker_name: 担当者名。省略した場合は担当者で絞り込みません。
    """
    try:
        task_table = _get_table("作業タスク")
        today = date.today().isoformat()

        # --- フィルタ式を動的に組み立て ---
        filters = [f"IS_SAME({{予定日}}, '{today}', 'day')", "NOT({ステータス} = '完了')"]

        # 担当者による絞り込みはオプション
        if worker_name:
            sanitized_name = _sanitize_airtable_string(worker_name)
            # 担当者フィールドが存在しない環境ではこの条件を追加しない
            filters.append(f"FIND('{sanitized_name}', ARRAYJOIN({{担当者}}))")

        filter_formula = "AND(" + ", ".join(filters) + ")"

        tasks = task_table.get_all(formula=filter_formula)

        if not tasks:
            if worker_name:
                return f"{worker_name}さんの本日のタスクはありません。"
            return "本日のタスクはありません。"

        task_list: list[str] = []
        for task in tasks:
            fields = task.get("fields", {})
            task_name = fields.get("タスク名", "N/A")
            # 圃場名フィールドはルックアップのため配列で返ることがある
            field_val = fields.get("圃場名 (from 圃場データ) (from 関連する作付計画)")
            if isinstance(field_val, list):
                field_name = field_val[0] if field_val else "N/A"
            else:
                field_name = field_val or "N/A"
            task_list.append(f"・{task_name} (圃場: {field_name})")

        header = f"{worker_name}さんの本日のタスク:" if worker_name else "本日のタスク:"
        return header + "\n" + "\n".join(task_list)
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


def _sanitize_airtable_string(value: str) -> str:
    """Sanitize string for use in Airtable formulas to prevent injection."""
    return value.replace("'", "\\'").replace('"', '\\"')


def search_materials(
    query: str,
    category: Optional[str] = None,
    crop: Optional[str] = None,
) -> str:
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
        sanitized_query = _sanitize_airtable_string(query)
        if sanitized_query:
            # 複数のフィールドをORで検索
            or_clauses = [
                f"FIND('{sanitized_query}', {{資材名}})",
                f"FIND('{sanitized_query}', {{主成分}})",
                f"FIND('{sanitized_query}', {{メーカー}})",
            ]
            formulas.append(f"OR({', '.join(or_clauses)})")

        if category:
            sanitized_category = _sanitize_airtable_string(category)
            formulas.append(f"{{資材分類}} = '{sanitized_category}'")

        if crop:
            sanitized_crop = _sanitize_airtable_string(crop)
            formulas.append(f"FIND('{sanitized_crop}', {{適用作物}})")

        if not formulas:
            return "検索条件が指定されていません。"

        filter_formula = f"AND({', '.join(formulas)})"

        records = table.get_all(formula=filter_formula)

        if not records:
            return "条件に合う資材は見つかりませんでした。"

        results = [f"「{query}」に一致する資材が{len(records)}件見つかりました："]
        for record in records:
            fields = record["fields"]
            info = (
                f"- {fields.get('資材名', 'N/A')} "
                f"({fields.get('メーカー', 'N/A')}, {fields.get('規格・容量', 'N/A')})\\n"
                f"  分類: {fields.get('資材分類', 'N/A')}\\n"
                f"  適用作物: {fields.get('適用作物', 'N/A')}"
            )
            results.append(info)

        return "\\n".join(results)
    except Exception as e:
        return f"エラー: 資材の検索中に予期せぬ問題が発生しました - {e}"


def search_tasks(
    task_keyword: str,
    month: Optional[str] = None,
    field_name: Optional[str] = None,
) -> str:
    """複数条件で作業タスクを検索する。

    Args:
        task_keyword: タスク名に含まれるキーワード（例: "防除"）
        month: 対象月。"2025-07" 形式または "7月" などを許容。省略可。
        field_name: 圃場名で絞り込む場合に指定。

    Returns:
        ヒットしたタスク一覧または見つからない旨のメッセージ。
    """
    try:
        table = _get_table("作業タスク")

        if not task_keyword:
            return "検索キーワードが指定されていません。"

        formulas: list[str] = []
        sanitized_kw = _sanitize_airtable_string(task_keyword)
        formulas.append(f"FIND('{sanitized_kw}', {{タスク名}})")

        # 月指定がある場合 → 予定日の YYYY-MM で一致を取る
        if month:
            # "7月" → "07", "2025-07" はそのまま
            import re

            if re.match(r"^\d{4}-\d{2}$", month):
                ym_str = month
            else:
                digits = re.sub(r"\D", "", month)
                if len(digits) == 1:
                    digits = f"0{digits}"
                # 年未指定 → 当年
                ym_str = f"{date.today().year}-{digits}"
            ym_safe = _sanitize_airtable_string(ym_str)
            formulas.append(f"SEARCH('{ym_safe}', DATETIME_FORMAT({{予定日}}, 'YYYY-MM'))")

        if field_name:
            fname = _sanitize_airtable_string(field_name)
            formulas.append(
                f"FIND('{fname}', ARRAYJOIN({{圃場名 (from 圃場データ) (from 関連する作付計画)}}))"
            )

        filter_formula = "AND(" + ", ".join(formulas) + ")"
        records = table.get_all(formula=filter_formula)

        if not records:
            return "条件に合うタスクは見つかりませんでした。"

        lines: list[str] = [f"条件に合うタスクが {len(records)} 件見つかりました:"]
        for rec in records:
            flds = rec["fields"]
            tname = flds.get("タスク名", "N/A")
            sched = flds.get("予定日", "N/A")
            fld_val = flds.get("圃場名 (from 圃場データ) (from 関連する作付計画)")
            if isinstance(fld_val, list):
                fld_disp = fld_val[0] if fld_val else "N/A"
            else:
                fld_disp = fld_val or "N/A"
            lines.append(f"・{sched}: {tname} (圃場: {fld_disp})")

        return "\n".join(lines)
    except Exception as e:
        return f"エラー: タスク検索中に問題が発生しました - {e}"
