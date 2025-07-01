# Agri-Agent: 農業管理AIエージェント

## 1. プロジェクトビジョン

> **「考えるプロセスをなくし、AIが次の一手を指南する」**

本プロジェクトは、日々の農作業における判断の負荷を劇的に削減し、誰もが熟練者のように最適な作業を実践できる世界を目指します。

## 2. 概要

`Agri-Agent`は、Googleの**Agents SDK (ADK)** を活用して構築された、次世代の農業管理AIエージェントです。

農作業員や管理者が日常的に使用する**LINE**をインターフェースとし、AIとの対話を通じて「今日のタスクは？」「この畑の次の作業は？」といった質問に答えるだけでなく、圃場の状況や天候に応じて最適な農薬や肥料を提案します。

まずは自社農場での運用を目指すためバックエンドでは**Airtable**をデータベースとして利用し、圃場情報、作物、作業計画、農薬マスターなどを一元管理。AIエージェントはこれらのデータを参照・更新する「ツール」を持つことで、データに基づいた的確な指示を生成します。

このプロジェクトは、属人的な経験と勘に頼りがちだった農業の現場に、データドリブンで標準化されたワークフローをもたらし、生産性と品質の向上、そして技術伝承の効率化を実現します。

## 3. 主な機能

- **タスク管理:**
    - LINEを通じてその日の作業タスクを自動で通知・確認できます。
    - 作業完了を報告すると、Airtable上のタスクステータスが自動で更新されます。
- **インテリジェントな作業提案:**
    - 圃場、作物、天候、生育ステージなどの複合的な情報から、AIが次に実施すべき最適な作業（特に農薬散布や施肥）を判断し、具体的な手順を提案します。
- **情報検索:**
    - 「A畑のトマトの情報を教えて」といった自然言語での問い合わせに対し、作付け情報や過去の作業履歴を回答します。
    - 「この病気に効く農薬は？」といった質問に対し、Airtableのマスターデータから適切な農薬を検索・提案します。
- **作業記録:**
    - LINEでの報告を通じて、使用した資材や作業時間などを簡単にAirtableへ記録できます。

## 4. 技術スタック・アーキテクチャ

- **言語:** Python 3.9+
- **AIエージェントフレームワーク:** Google Agents SDK (ADK)
- **大規模言語モデル (LLM):** Google Gemini
- **データベース:** Airtable
- **UI/UX:** LINE Messaging API
- **インフラストラクチャ:**
    - **デプロイ環境:** Google Cloud Run (または Vertex AI Agent Engine)
    - **Webhook処理:** Google Cloud Functions
    - **定期実行:** Google Cloud Scheduler
- **ソースコード管理:** Git / GitHub

![Architecture Diagram](https://user-images.githubusercontent.com/12345/architecture.png)  
*(アーキテクチャ図は後ほど追加)*

## 5. 開発ロードマップ

開発は大きく3つのフェーズで進行します。

- **[フェーズ1] 基盤構築:**
    - ADKの開発環境をセットアップします。
    - Airtableのデータを操作するための基本的なツール群（タスク取得、情報検索、作業記録など）を開発します。
    - 簡単な質疑応答ができる基本エージェントを構築し、ローカルで動作確認を行います。
- **[フェーズ2] インテリジェント機能開発:**
    - 複数の専門エージェント（状況分析、農薬選定、施肥提案など）を連携させるマルチエージェントシステムを構築します。
    - LINE Messaging APIと連携し、Webhook経由でエージェントを呼び出せるようにします。
    - 定期的なタスク通知やリッチメニューを実装します。
- **[フェーズ3] 本番化・運用:**
    - `AgentEvaluator`を用いた性能評価の仕組みを導入します。
    - `adk deploy cloudrun`コマンドで本番環境へデプロイします。
    - ログ収集とモニタリング体制を構築し、継続的な改善サイクルを回します。

詳細なタスクリストは[こちら](./docs/アグリエージェント_タスク.md)を参照してください。

## 6. 開発環境セットアップ

### 前提条件
- Python 3.9以上
- Google Cloud SDK (`gcloud` CLI)
- AirtableアカウントとAPIキー

### 手順

1. **リポジトリのクローン:**
   ```bash
   git clone https://github.com/your-username/Agri_AI.git
   cd Agri_AI
   ```

2. **Python仮想環境の構築と有効化:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # Windowsの場合: .venv\Scripts\activate
   ```

3. **Google Cloud認証:**
   Vertex AI APIを有効化した上で、ローカル環境からアクセスするための認証を行います。
   ```bash
   gcloud auth application-default login
   ```

4. **依存ライブラリのインストール:**
   `google-adk`とAirtableクライアントをインストールします。（`requirements.txt`を作成後、変更予定）
   ```bash
   pip install google-adk airtable-python-wrapper python-dotenv
   ```

5. **環境変数の設定:**
   プロジェクトルートに`.env`ファイルを作成し、以下の情報を記述します。
   ```.env
   # .env
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   AIRTABLE_API_KEY="your_airtable_api_key"
   AIRTABLE_BASE_ID="your_airtable_base_id"
   LINE_CHANNEL_ACCESS_TOKEN="your_line_channel_access_token"
   LINE_CHANNEL_SECRET="your_line_channel_secret"
   ```
   **注意:** `.env`ファイルは絶対にGitでコミットしないでください。

6. **ローカルでのエージェント実行:**
   ADKのWeb UIを使って、ローカルでエージェントの動作テストができます。
   ```bash
   adk web
   ```
   ブラウザで `http://127.0.0.1:8080` を開くと、対話インターフェースが表示されます。

## 7. ディレクトリ構成（予定）

```
Agri_AI/
├── .venv/
├── agent/
│   ├── __init__.py         # エージェントモジュールの定義
│   ├── agent.py            # メインエージェントの定義
│   └── tools/
│       ├── __init__.py
│       └── airtable_tools.py # Airtable操作ツール群
├── docs/                     # プロジェクト関連ドキュメント
│   ├── アグリエージェント_要件定義.md
│   ├── アグリエージェント_タスク.md
│   └── ...
├── .env                    # 環境変数（Git管理外）
├── .gitignore
└── README.md
``` 