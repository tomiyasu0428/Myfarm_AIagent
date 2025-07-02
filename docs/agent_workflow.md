プロジェクト目標: 「考えるプロセスをなくし、AIが次の一手を指南する」

以下のワークフローは、現行の Airtable スキーマ（作業タスク／圃場データ／作付計画／作物マスター 等）と LINE 連携を前提に、
AI エージェントが日次タスク提案と完了報告処理を担う全体像を示します。

```mermaid
%%---------------------------------------------------------------------------
%% Main workflow diagram for Agri-AI multi-agent system
%%---------------------------------------------------------------------------
graph TD
    %% =====================
    %% 0. Scheduled Trigger
    %% =====================
    subgraph Scheduler
        CloudScheduler[Cloud Scheduler<br>(cron)]
    end

    %% ---------------------
    %% 1. User Interaction
    %% ---------------------
    subgraph User Interaction
        User[農作業員]
    end

    %% ---------------------
    %% 2. External Services
    %% ---------------------
    subgraph External Services
        LINE
        GCF[Google Cloud Functions<br>(Webhook)]
        Airtable[(Airtable Base)]
        WeatherAPI[外部API<br>(天候情報等)]
    end

    %% ---------------------
    %% 3. ADK Multi Agent
    %% ---------------------
    subgraph ADK Multi-Agent System
        direction LR
        Orchestrator[Orchestrator Agent<br>(司令塔)]
        subgraph Child Agents
            AnalysisAgent[状況分析エージェント]
            ProposalAgent[タスク提案エージェント]
            AutoTaskGen[タスク自動生成エージェント]
        end
        Tools[Airtable Tools<br>(CRUD / Metadata)]
    end

    %% =====================================================================
    %% Flow-A: 日次 / 定期タスク生成 & 通知
    %% =====================================================================
    CloudScheduler -- 毎朝 5:00<br>HTTP 呼び出し --> GCF
    GCF -- Agent Run --> Orchestrator
    Orchestrator -- 作業計画に基づく生成指示 --> AutoTaskGen
    AutoTaskGen -- 既存計画を取得 --> Tools
    Tools -- read 作付計画 / 圃場データ --> Airtable
    Airtable -- データ返却 --> Tools
    AutoTaskGen -- 新規「作業タスク」を書込 --> Tools
    Tools -- create 作業タスク --> Airtable
    Orchestrator -- LINE Push 用メッセージ生成 --> GCF
    GCF -- Push API --> LINE
    LINE -- 通知表示 --> User

    %% =====================================================================
    %% Flow-B: 質問へのオンデマンド応答
    %% =====================================================================
    User -- Q. LINE で質問<br>「A畑のトマト、次の作業は?」 --> LINE
    LINE -- Webhook --> GCF
    GCF -- Agent Run --> Orchestrator
    Orchestrator -- 状況分析依頼 --> AnalysisAgent
    AnalysisAgent -- データ取得要求 --> Tools
    AnalysisAgent -- WeatherAPI 呼び出し --> WeatherAPI
    Tools -- read 圃場 / 作物 / 作業履歴 --> Airtable
    WeatherAPI -- 気象データ返却 --> AnalysisAgent
    Airtable -- データ返却 --> Tools
    Tools -- データ返却 --> AnalysisAgent
    AnalysisAgent -- 提案依頼 --> ProposalAgent
    ProposalAgent -- 最適作業決定 --> ProposalAgent
    ProposalAgent -- 回答 --> Orchestrator
    Orchestrator -- LINE 返信生成 --> GCF
    GCF -- Reply API --> LINE
    LINE -- ユーザーへ表示 --> User

    %% =====================================================================
    %% Flow-C: 作業完了報告
    %% =====================================================================
    User -- 完了報告 --> LINE
    LINE -- Webhook --> GCF
    GCF -- Agent Run --> Orchestrator
    Orchestrator -- ステータス更新指示 --> Tools
    Tools -- update 作業タスク --> Airtable

    %% Styling
    classDef agent fill:#e6f2ff,stroke:#8ac4ff,stroke-width:2px;
    class Orchestrator,AnalysisAgent,ProposalAgent,AutoTaskGen,Tools agent;
    classDef external fill:#f5f5f5,stroke:#ccc,stroke-width:2px;
    class LINE,GCF,Airtable,WeatherAPI,CloudScheduler external;
```
