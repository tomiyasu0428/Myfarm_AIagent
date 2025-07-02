import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数の確認
print(f"GOOGLE_API_KEY is set: {'GOOGLE_API_KEY' in os.environ}")
print(f"AIRTABLE_PAT is set: {'AIRTABLE_PAT' in os.environ}")
print(f"AIRTABLE_BASE_ID is set: {'AIRTABLE_BASE_ID' in os.environ}")

# エージェントのインポートテスト
try:
    from agent import root_agent

    print("✅ Agent loaded successfully!")
    print(f"   Name: {root_agent.name}")
    print(f"   Description: {root_agent.description}")
    print(f"   Model: {root_agent.model}")
    print(f"   Number of tools: {len(root_agent.tools)}")

    # ツールの一覧表示
    print("\n📋 Available tools:")
    for i, tool in enumerate(root_agent.tools, 1):
        print(f"   {i}. {tool.__name__}")

except Exception as e:
    print(f"❌ Error loading agent: {e}")
    import traceback

    traceback.print_exc()
