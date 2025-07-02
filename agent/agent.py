from google.adk.agents import Agent

from .airtable_tools import (
    airtable_get_records,
    airtable_create_record,
    airtable_update_record,
    airtable_delete_record,
    airtable_create_table,
    airtable_update_table,
    airtable_delete_table,
)


# NOTE: Adjust the model name if you have access to a different Gemini tier.
_MODEL_NAME = "gemini-2.0-flash"


root_agent = Agent(
    model=_MODEL_NAME,
    name="agri_airtable_agent",
    description="An AI agent capable of managing Airtable tables and records for the Agri-Agent project.",
    instruction=(
        "You are an assistant designed to operate on Airtable. "
        "Use the provided tools to read from tables, insert new rows, update existing rows, "
        "and create or delete entire tables. When unsure about table or field names, "
        "ask the user for clarification before running a destructive operation."
    ),
    tools=[
        airtable_get_records,
        airtable_create_record,
        airtable_update_record,
        airtable_delete_record,
        airtable_create_table,
        airtable_update_table,
        airtable_delete_table,
    ],
)
