from google.adk.agents import Agent

from .airtable_tools import (
    create_daily_report,
    get_field_info,
    get_today_tasks,
    search_materials,
    update_task_status,
)


# NOTE: Adjust the model name if you have access to a different Gemini tier.
_MODEL_NAME = "gemini-1.5-flash"


root_agent = Agent(
    model=_MODEL_NAME,
    name="agri_agent",
    description="農作業に関するタスク管理、日報作成、情報検索を行うためのAIアシスタントです。",
    instruction=(
        "あなたは熟練の農業アシスタントです。"
        "ユーザーからの自然言語による指示を理解し、提供されたツールを使って以下の操作を行ってください。\n"
        "- 今日の作業タスクを確認する (get_today_tasks)\n"
        "- 作業日報を記録する (create_daily_report)\n"
        "- 作業タスクの状況を更新する (update_task_status)\n"
        "- 圃場の情報を調べる (get_field_info)\n"
        "- 農薬や肥料などの資材を検索する (search_materials)\n"
        "特にタスク更新の際は、まずタスクを取得してから更新対象を特定するなど、複数のツールを段階的に使用して目的を達成してください。"
    ),
    tools=[
        get_today_tasks,
        create_daily_report,
        update_task_status,
        get_field_info,
        search_materials,
    ],
)
