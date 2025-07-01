

# **Google Agents SDK (ADK) 徹底解説：アプリ開発者のための導入から実践まで**

## **Section 1: Google Agents SDK (ADK)へようこそ \- 最初のAIエージェントを構築するための第一歩**

### **Introduction: Beyond a Library, a Framework for Production Agents**

Google Agents SDK (ADK)は、AIエージェント開発という、時に混沌としがちな領域にソフトウェア開発の規律をもたらすために設計された、オープンソースでコードファーストのPythonおよびJavaツールキットです 1。その中心的な哲学は、エージェント開発を従来のソフトウェア開発の感覚に近づけ、単純な単機能エージェントから、複数のエージェントが連携して動作する複雑なオーケストレーションシステムまで、あらゆるものの構築を可能にすることにあります 1。

ADKはGoogleのGeminiモデルやエコシステムに最適化されている一方で、意図的にモデルに依存せず、デプロイ環境にも依存しないように設計されており、開発者に高い柔軟性を提供します 1。これにより、開発者は特定のモデルやインフラストラクチャに縛られることなく、最適なツールを選択してエージェントを構築できます。

### **The Pillars of ADK: A High-Level Architecture Overview**

ADKの強力な機能は、いくつかの基本要素（ピラー）によって支えられています。これらはエージェント開発のライフサイクル全体をカバーしています 4。

* **Multi-Agent by Design（マルチエージェント設計）:** ADKは、複数の特化したエージェントを階層的に組み合わせることで、モジュール化され、スケーラブルなアプリケーションを構築することを基本思想としています。これにより、複雑なタスクの協調や委任が可能になります 4。  
* **Rich Tool Ecosystem（豊富なツールエコシステム）:** エージェントに現実世界の能力を与える「ツール」の概念が中心にあります。Google検索のような組み込み済みツールから、あらゆるAPIと連携するカスタム関数まで、多様なツールを利用できます 2。  
* **Flexible Orchestration（柔軟なオーケストレーション）:** ADKは、LLM（大規模言語モデル）による動的なルーティングと、WorkflowAgents（Sequential, Parallel, Loop）を用いた決定論的なワークフローの両方をサポートしており、予測可能なパイプラインと適応的な挙動を使い分けることができます 2。  
* **Integrated Developer Experience（統合された開発者体験）:** 強力なコマンドラインインターフェース（CLI）と視覚的なWeb UIが提供されており、ローカル環境での開発、テスト、デバッグをスムーズに行えます。イベント、状態、エージェントの実行ステップを詳細に追跡することが可能です 3。  
* **Built-in Evaluation & Deployment Readiness（組み込みの評価とデプロイ準備）:** エージェントの性能を体系的に評価するためのフレームワークが組み込まれています。また、コンテナ化を通じて、Vertex AI Agent EngineやCloud Runといったプラットフォームへ容易にデプロイできる、本番環境への明確な道筋が用意されています 2。  
* **Rich Multimodality（豊かなマルチモーダル性）:** テキストだけでなく、双方向の音声および映像ストリーミングをサポートしている点がユニークです。これにより、数行のコードで、より自然で人間らしい対話を実現できます 4。

これらの特徴は、ADKが単なるエージェント構築ライブラリではなく、エンタープライズレベルの堅牢なアプリケーションを構築するための包括的なフレームワークであることを示しています。その設計思想は、断片化しがちなAIエージェントのエコシステムにおいて、「結合組織」として機能することを目指しているように見受けられます。ADKがデプロイ環境に依存せず、LangChainやCrewAIといったサードパーティ製ツールをサポートしていること 2、そして「普遍的な通信規格」としてAgent2Agent (A2A) プロトコルを導入していること 6 は、その証左です。A2Aは、ADK、LangGraphなど、異なるフレームワークで構築されたエージェント間の通信を可能にすることを目的としています。このことから、ADKは、あるタスクはADKで構築したエージェントが、別のタスクはLangChainで構築したレガシーエージェントが、そしてまた別のタスクはサードパーティベンダーがMCP経由で提供するツールが処理する、といった複雑なワークフローを管理する中央オーケストレーターとして位置づけられていると考えられます。この構造と相互運用性への注力が、ADKを「エンタープライズグレード」たらしめているのです。

## **Section 2: 開発環境の構築 \- 成功へのセットアップガイド**

堅牢なAIエージェントを構築するための第一歩は、安定した開発環境を整えることです。ここでは、ADKを使用するために必要な前提条件から、具体的な設定手順までを詳細に解説します。

### **Prerequisites: What You'll Need**

開発を始める前に、以下の環境が整っていることを確認してください。

* **Python:** バージョン3.9以上が必要です。ADKはモダンなPythonの機能を活用しています 7。Javaで開発する場合は、Java 17以上が必要です 2。  
* **ローカルIDE:** Visual Studio Code (VS Code)やPyCharmなど、使い慣れた統合開発環境 7。  
* **ターミナルアクセス:** コマンドライン操作に習熟していることが望ましいです 7。

### **Step 1: Google Cloud Project and API Configuration**

ADK、特にVertex AIの機能を最大限に活用するには、Google Cloudプロジェクトの設定が不可欠です。

1. **Google Cloudプロジェクトの選択または作成:** Google Cloudコンソールにログインし、プロジェクトセレクターページで既存のプロジェクトを選択するか、新しいプロジェクトを作成します 7。テスト目的でリソースを作成し、後で削除する予定の場合は、新しいプロジェクトを作成することが推奨されます 7。  
2. **課金の有効化:** 選択したGoogle Cloudプロジェクトで課金が有効になっていることを確認してください。多くのGoogle Cloudサービスは課金設定が必要ですが、新規顧客には無料クレジットが付与される場合があります 7。  
3. **Vertex AI APIの有効化:** プロジェクトでVertex AI APIを有効にする必要があります。これは、エージェントがGoogleの強力なAIモデルやインフラストラクチャにアクセスするために必要です 7。

### **Step 2: Authentication with Google Cloud CLI**

Vertex AIのGemini APIなどは、単純なAPIキーではなく、IAM (Identity and Access Management) を用いてアクセスを管理します 7。ローカル開発環境から安全にアクセスするために、Google Cloud CLIを使用して認証情報を設定します。

1. **Google Cloud CLIのインストールと更新:** gcloud CLIがインストールされていない場合は、公式ドキュメントに従ってインストールと初期化を行います。すでにインストール済みの場合は、以下のコマンドで最新の状態に更新してください 7。  
   Bash  
   gcloud components update

2. **アプリケーションのデフォルト認証情報 (ADC) の設定:** 以下のコマンドを実行すると、ブラウザが開き、Googleアカウントでの認証が求められます。認証が完了すると、ローカルマシンに認証情報ファイルが生成され、ADKアプリケーションはこれを自動的に使用してGoogle Cloudサービスにアクセスします 7。  
   Bash  
   gcloud auth application-default login

### **Step 3: Local Environment and ADK Installation**

プロジェクトの依存関係をクリーンに保つため、Pythonの仮想環境を使用することが強く推奨されます。

1. **仮想環境の作成と有効化:** プロジェクトディレクトリで以下のコマンドを実行し、仮想環境を作成して有効化します 7。  
   Bash  
   \# 仮想環境を作成  
   python \-m venv.venv

   \# 有効化 (お使いの環境に合わせてコメントを外してください)  
   \# macOS/Linux:  
   \# source.venv/bin/activate  
   \# Windows (CMD):  
   \#.venv\\Scripts\\activate.bat  
   \# Windows (PowerShell):  
   \#.venv\\Scripts\\Activate.ps1

2. **ADKのインストール:** 仮想環境が有効化された状態で、pipコマンドを使ってADKの安定版をインストールします 1。  
   Bash  
   pip install google-adk

### **Step 4: Standard Project Structure**

ADKは規約に基づいたプロジェクト構造を推奨しています。これにより、フレームワークがエージェントを正しく認識し、開発体験が向上します。

以下は、推奨される基本的なディレクトリ構造です 7。

parent\_folder/  
└── my\_first\_agent/  
    ├── \_\_init\_\_.py  \# このディレクトリをPythonパッケージとして認識させる  
    ├── agent.py     \# エージェントのコアロジックを定義する  
    └──.env         \# APIキーやプロジェクトIDなどの環境変数を格納する

* **\_\_init\_\_.py:** このファイルは、my\_first\_agentディレクトリがPythonパッケージであることを示します。中身は、エージェントモジュールをインポートする一行だけで十分です 7。  
  Python  
  from. import agent

* **agent.py:** ここに、エージェントの定義、使用するツール、指示（プロンプト）など、エージェントの振る舞いを決定する主要なコードを記述します。  
* **.env:** APIキーなどの機密情報をコードから分離するためのファイルです。このファイルはバージョン管理システム（Gitなど）に含めないように注意してください。

この構造に従うことで、ADKのCLIツールがエージェントを自動的に検出し、Web UIでのテストやデプロイをスムーズに行えるようになります。

## **Section 3: ADKの核心概念をマスターする**

ADKを効果的に使用するためには、その中心となるいくつかの概念を深く理解することが不可欠です。Agent、Tool、そしてSession、State、Memoryという3つのコンテキスト管理の概念は、ADKアプリケーションの設計と実装の基盤となります。

### **3.1. The Agent: The "Brain" of Your Application**

ADKにおけるAgentとは、特定の目標を達成するために自律的に行動するように設計された、自己完結型の実行ユニットです 12。すべてのエージェントは

BaseAgentクラスを基礎としており、用途に応じて主に3つのカテゴリに分類されます。

* **LLM Agents (LlmAgent):** これはアプリケーションの「思考」エンジンです。LLMの能力を活用して自然言語を理解し、推論し、計画を立て、どのツールを使用するかを動的に決定します。その振る舞いは非決定的で柔軟性が高く、言語中心のタスクに適しています 12。  
  LlmAgentを定義する際の主要なパラメータは以下の通りです 13。  
  * name: エージェントの一意な識別子。特にマルチエージェントシステムでのタスク委任において重要です。  
  * model: エージェントの推論の核となるLLMのID（例: "gemini-1.5-flash"）。  
  * description: 他のエージェントがこのエージェントにタスクを委任すべきかを判断するために使用する、機能の簡潔な説明。  
  * instruction: エージェントのペルソナ、目標、制約、ツールの使用方法などを定義する「システムプロンプト」。  
  * tools: エージェントが利用可能な能力のリスト。  
* **Workflow Agents (SequentialAgent, ParallelAgent, LoopAgent):** これは「オーケストレーター」です。LLMを介さず、あらかじめ定義された決定論的なパターン（順次、並列、ループ）で他のエージェントの実行フローを制御します。構造化されたプロセスや予測可能な実行が必要な場合に最適です 10。  
* **Custom Agents:** 非常に特殊なロジックや統合が必要な場合、開発者はBaseAgentを直接継承して、独自のカスタムエージェントを作成できます 12。

これらのエージェントタイプを適切に選択することは、効率的で保守性の高いアプリケーションを設計するための鍵となります。以下の表は、それぞれの特徴を比較し、選択の指針を示します。

#### **Table 1: エージェントタイプの選択ガイド**

| 特徴 | LLM Agent (LlmAgent) | Workflow Agent | Custom Agent (BaseAgent subclass) |  |
| :---- | :---- | :---- | :---- | :---- |
| **主な機能** | 推論、生成、ツール利用 | エージェント実行フローの制御 | 独自のロジック/統合の実装 |  |
| **コアエンジン** | 大規模言語モデル (LLM) | 事前定義されたロジック（順次、並列、ループ） | カスタムコード |  |
| **決定性** | 非決定的（柔軟） | 決定的（予測可能） | 実装に依存 |  |
| **主な用途** | 言語タスク、動的な意思決定 | 構造化されたプロセス、オーケストレーション | 特化した要件、特定のワークフロー |  |
| Data Source: 12 |  |  |  |  |

### **3.2. The Tool: Giving Your Agent Capabilities**

Toolは、エージェントが外部の世界と対話し、その能力を拡張するための関数です。APIのクエリ、データベース検索、計算実行など、テキスト生成能力だけでは不可能なアクションを可能にします 15。

ADKにおけるツールの設計には、特筆すべきパラダイムが存在します。それは、ツールのdocstring（ドキュメンテーション文字列）が、単なる人間向けの説明書ではなく、機械が読み取るためのAPI契約の一部として機能するという点です。LlmAgentは非決定論的であり、ユーザーのクエリに対してどのツールを呼び出すべきかを、その中核となるLLMの推論能力を使って判断します 12。公式ドキュメントでは、LLMがツールの機能、使用すべきタイミング、必要な引数を理解するために、関数のdocstringに大きく依存していると明記されています 15。

これは、曖昧または誤解を招くdocstringが、LLMの不適切な判断を引き起こし、実行時エラーや非論理的な振る舞いにつながることを意味します。つまり、docstringは、関数のシグネチャや戻り値と同じくらい、ツールの機能にとって極めて重要なのです。開発者は、ドキュメンテーションとプログラミングロジックを融合させた、「プロンプトエンジニアリングされた」docstringを書くという新しいスキルを習得する必要があります。

以下は、明確なdocstringを持つ単純なPython関数ツールの例です 15。

Python

def get\_weather(city: str) \-\> dict:  
    """指定された都市の現在の天気予報を取得します。

    Args:  
        city (str): 天気予報を取得する都市の名前（例: "New York", "London", "Tokyo"）。

    Returns:  
        dict: 天気情報を含む辞書。'status'キー（'success'または'error'）を含む。  
              'success'の場合は'report'キーに天気の詳細が含まれる。  
              'error'の場合は'error\_message'キーが含まれる。  
    """  
    \#... 関数の実装...

このdocstringは、LLMに対して、このツールが何をするのか、cityという文字列引数を必要とすること、そしてどのような形式の辞書を返すのかを明確に伝えています。

### **3.3. Session, State, and Memory: Managing Conversational Context**

人間同士の会話のように、文脈を維持し、意味のある複数ターンにわたる対話を実現するため、ADKはSession、State、Memoryという3つの概念を提供しています 18。

* **Session:** 現在進行中の、単一の会話スレッド全体を表します。その対話におけるイベント（ユーザーの発言、エージェントの応答、ツールの実行など）の履歴を保持します 18。  
* **State (session.state):** 現在のセッションに**のみ**関連する一時的なデータを格納するための「メモ帳」のようなものです。例えば、ショッピングカートの中身などがこれにあたります。このデータはセッションが終了すると失われます 18。  
* **Memory:** 複数のセッションをまたいで、あるいは外部データソースから得られる、長期的な検索可能な知識ベースです。永続化が必要な情報（例: ユーザーの過去の購入履歴）はここに格納します 18。

これらの概念を正しく使い分けることが、洗練されたエージェントを設計する上で重要になります。以下の表は、それぞれの概念の役割と使い分けの指針をまとめたものです。

#### **Table 2: コンテキスト管理の概念比較**

| 概念 | 目的 | スコープ | 永続性 | 管理者 | 使用例 |  |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Session** | 単一の進行中の会話を追跡 | 一つの対話 | 一時的（セッションの寿命に依存） | SessionService | 「こんにちは」から「さようなら」までの一連のチャット対話 |  |
| **State** | 現在の会話のための一時データを保存 | 一つのSession内 | 一時的（セッション終了時に失われる） | SessionService | ショッピングカートの中身、ユーザーの直前の質問 |  |
| **Memory** | 長期的な検索可能知識を保存 | 全てのセッションとユーザーを横断 | 永続的 | MemoryService | ユーザーの購入履歴、製品ドキュメント |  |
| Data Source: Synthesized from 18 |  |  |  |  |  |  |

## **Section 4: 実践編①：シンプルな「天気・時刻案内エージェント」の構築**

これまでに学んだ核心概念を具体的に理解するため、実際に動作するシンプルなエージェントを構築します。このエージェントは、特定の都市（この例ではニューヨーク）の天気と時刻に関する質問に答える能力を持ちます。

### **Step 1: Defining the Tools (get\_weather, get\_current\_time)**

まず、エージェントに能力を与えるための2つのツールをPython関数として定義します。これらの関数は、agent.pyファイル内に記述します。

Python

import datetime  
from zoneinfo import ZoneInfo

def get\_weather(city: str) \-\> dict:  
    """指定された都市の現在の天気予報を取得します。  
    Args:  
        city (str): 天気予報を取得する都市の名前。  
    Returns:  
        dict: 天気情報を含む辞書。  
    """  
    print(f"--- Tool: get\_weather が都市: {city} で呼び出されました \---")  
    if city.lower() \== "new york":  
        return {  
            "status": "success",  
            "report": "ニューヨークの天気は晴れ、気温は摂氏25度です。",  
        }  
    else:  
        return {  
            "status": "error",  
            "error\_message": f"'{city}'の天気情報は利用できません。",  
        }

def get\_current\_time(city: str) \-\> dict:  
    """指定された都市の現在時刻を取得します。  
    Args:  
        city (str): 現在時刻を取得する都市の名前。  
    Returns:  
        dict: 時刻情報を含む辞書。  
    """  
    print(f"--- Tool: get\_current\_time が都市: {city} で呼び出されました \---")  
    if city.lower() \== "new york":  
        tz\_identifier \= "America/New\_York"  
        tz \= ZoneInfo(tz\_identifier)  
        now \= datetime.datetime.now(tz)  
        report \= f'ニューヨークの現在時刻は {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")} です。'  
        return {"status": "success", "report": report}  
    else:  
        return {  
            "status": "error",  
            "error\_message": f"申し訳ありませんが、{city}のタイムゾーン情報はありません。",  
        }

このコードでは、get\_weatherとget\_current\_timeという2つの関数を定義しています 10。現時点では、外部APIを呼び出す代わりに、都市が「new york」の場合に固定の応答を返すモック（模擬）実装となっています。重要なのは、各関数のdocstringが、LLMがそのツールの目的と使い方を理解できるように、明確に記述されている点です。

### **Step 2: Configuring the agent.py file**

次に、これらのツールを使用するエージェント本体を定義します。先ほどのツール関数の下に、以下のコードを追記します。

Python

from google.adk.agents import Agent

root\_agent \= Agent(  
    name="weather\_time\_agent",  
    model="gemini-1.5-flash",  
    description="都市の時刻と天気に関する質問に答えるエージェント。",  
    instruction=(  
        "あなたは、ユーザーからの都市に関する時刻と天気の質問に答えることができる、"  
        "親切なエージェントです。ユーザーの質問を分析し、get\_weatherまたは"  
        "get\_current\_timeのいずれかのツールを呼び出して、その応答に基づいて回答してください。"  
    ),  
    tools=\[get\_weather, get\_current\_time\],  
)

このコードでは、google.adk.agentsからAgentクラス（LlmAgentのエイリアス）をインポートし、root\_agentという名前でエージェントをインスタンス化しています 10。

* name, model, descriptionでエージェントの基本情報を設定します。  
* instructionパラメータで、エージェントの役割と、ツールをどのように使うべきかを具体的に指示しています。  
* toolsパラメータに、先ほど定義したget\_weatherとget\_current\_timeの関数をリストとして渡すことで、エージェントがこれらのツールを利用できるようになります。

### **Step 3: Setting up the .env file**

エージェントが使用するLLM（この場合はGemini）にアクセスするためには、APIキーの設定が必要です。プロジェクトのルートにある.envファイルに、以下の内容を記述します 7。

GOOGLE\_GENAI\_USE\_VERTEXAI=FALSE  
GOOGLE\_API\_KEY=PASTE\_YOUR\_ACTUAL\_API\_KEY\_HERE

* GOOGLE\_GENAI\_USE\_VERTEXAI=FALSEは、Vertex AI経由ではなく、Google AI Studioから取得したAPIキーを直接使用することを示します。これは初心者にとって最も簡単な設定方法です 11。  
* PASTE\_YOUR\_ACTUAL\_API\_KEY\_HEREの部分を、ご自身のGoogle AI Studioで取得したAPIキーに置き換えてください。

### **Step 4: Running and Interacting with the Agent**

すべての設定が完了したら、エージェントを実行して対話してみましょう。プロジェクトの親ディレクトリ（my\_first\_agentフォルダがある階層）から、ターミナルで以下のコマンドを実行します。

Bash

adk web

このコマンドは、ADKの開発用Webサーバーを起動します 7。ターミナルに表示されたURL（通常は

http://localhost:8000）をブラウザで開くと、ADKのWeb UIが表示されます。

UIの左上にあるドロップダウンメニューから、今回作成したweather\_time\_agentを選択します。これで、画面下部のテキストボックスに質問を入力してエージェントと対話する準備が整いました 11。

以下のプロンプトを試してみてください 7。

* What is the weather in New York?  
* What is the time in New York?  
* ニューヨークの天気は？

エージェントは質問の内容を理解し、適切なツール（get\_weatherまたはget\_current\_time）を呼び出し、その結果を基に回答を生成するはずです。

### **Step 5: Basic Debugging with the Events Tab**

ADKのWeb UIの強力な機能の一つが、左側のパネルにある「Events」タブです。このタブをクリックすると、エージェントの実行トレースが詳細に表示されます 4。

ここを調べることで、以下の情報を確認できます。

* モデルがユーザーのプロンプトをどのように解釈したか。  
* モデルがどのツールを呼び出すと決定したか。  
* ツールにどのようなパラメータを渡したか。  
* ツールがどのようなデータを返したか。  
* 最終的な応答を生成するために、モデルがツールの結果をどのように利用したか。

このイベントログは、エージェントが期待通りに動作しない場合のデバッグにおいて、非常に価値のある情報源となります。なぜ特定のツールが呼ばれたのか（あるいは呼ばれなかったのか）を理解するための第一歩です 24。

## **Section 5: 実践編②：外部APIと連携する高度なエージェント**

シンプルなモック実装のエージェントを構築したところで、次はより実践的な、外部のWeb APIと連携するエージェントの構築に進みます。ADKは、開発者のスキルレベルやプロジェクトの要件に応じて、ツール連携のための段階的なパスを提供しています。単純な内部関数から始め、サードパーティのライブラリをラップし、複雑な認証フローを処理し、最終的にはMCPのようなエンタープライズ級のプロトコルに接続することができます。この柔軟性はADKの大きな強みです。このセクションでは、その中から代表的な3つの方法を解説します。

### **Method 1: Custom FunctionTool with the requests library**

最も直接的な方法は、Pythonの標準的なライブラリであるrequestsを使用して、外部APIを呼び出すカスタムFunctionToolを作成することです。ここでは、暗号資産の情報を取得する公開API（CoinGecko API）を呼び出すツールを例に挙げます 25。

Python

import requests  
import json

def get\_crypto\_details(coin\_id: str) \-\> dict:  
    """指定された暗号資産ID（例: 'bitcoin', 'ethereum'）の詳細情報を取得します。

    Args:  
        coin\_id (str): CoinGeckoでのコインのID。

    Returns:  
        dict: APIからの応答、またはエラー情報を含む辞書。  
    """  
    COINGECKO\_API\_URL \= f"https://api.coingecko.com/api/v3/coins/{coin\_id}"  
    try:  
        response \= requests.get(COINGECKO\_API\_URL)  
        \# ステータスコードが200番台でない場合に例外を発生させる  
        response.raise\_for\_status()  
          
        \# 成功した場合はJSONデータを返す  
        return response.json()  
    except requests.exceptions.HTTPError as http\_err:  
        \# HTTPエラー（例: 404 Not Found, 500 Server Error）  
        return {"error": "HTTP error occurred", "details": str(http\_err)}  
    except requests.exceptions.RequestException as req\_err:  
        \# ネットワーク関連のエラー（例: 接続タイムアウト）  
        return {"error": "Request error occurred", "details": str(req\_err)}

\# このツールをエージェントのtoolsリストに追加する  
\# crypto\_agent \= Agent(..., tools=\[get\_crypto\_details\])

このツールは、coin\_idを引数として受け取り、CoinGecko APIにGETリクエストを送信します。重要なのは、try...exceptブロックによる堅牢なエラーハンドリングです 24。API呼び出しはネットワークや外部サービスに依存するため、失敗する可能性があります。

raise\_for\_status()でHTTPエラーを検出し、RequestExceptionでより広範なリクエスト関連のエラーを捕捉することで、エージェントが予期せぬ状況に陥るのを防ぎ、エラー情報を辞書形式で返すようにしています。これにより、LLMはツールが失敗したことを認識し、「情報を取得できませんでした」といった適切な応答をユーザーに返すことができます。

### **Method 2: Authenticated APIs \- The Google Tasks Example**

多くの実用的なAPIは認証を必要とします。ADKは、OAuth 2.0のような複雑な認証フローもツール内で処理できます。ここでは、ユーザー自身のGoogle ToDoリストを操作するエージェントの構築を例に、認証付きAPIの連携方法を解説します 26。

1. **Google Cloudでの事前準備:**  
   * Google Cloudプロジェクトで**Google Tasks API**を有効にします。  
   * 「APIとサービス」\>「認証情報」から、「**OAuth 2.0 クライアント ID**」を作成します。  
   * アプリケーションの種類として「**デスクトップアプリ**」を選択します。作成後、JSONファイルをダウンロードし、credentials.jsonとしてプロジェクトに保存します 26。  
2. 認証サービス関数の実装:  
   以下のコードは、OAuth 2.0フローを処理し、認証済みのGoogle Tasks APIサービスオブジェクトを返す関数です。  
   Python  
   import os.path  
   import pickle  
   from google.auth.transport.requests import Request  
   from google.oauth2.credentials import Credentials  
   from google\_auth\_oauthlib.flow import InstalledAppFlow  
   from googleapiclient.discovery import build

   \# 必要なスコープを定義  
   SCOPES \= \['https://www.googleapis.com/auth/tasks'\]  
   CREDENTIALS\_FILE \= 'credentials.json'  
   TOKEN\_PICKLE\_FILE \= 'token.pickle'

   def get\_tasks\_service():  
       """認証済みのGoogle Tasks APIサービスオブジェクトを返す。"""  
       creds \= None  
       \# 以前に保存された認証情報（token.pickle）が存在するか確認  
       if os.path.exists(TOKEN\_PICKLE\_FILE):  
           with open(TOKEN\_PICKLE\_FILE, 'rb') as token:  
               creds \= pickle.load(token)

       \# 認証情報が存在しないか、無効な場合  
       if not creds or not creds.valid:  
           \# 期限切れでリフレッシュトークンがある場合はリフレッシュ  
           if creds and creds.expired and creds.refresh\_token:  
               creds.refresh(Request())  
           \# それ以外の場合は、新規に認証フローを開始  
           else:  
               flow \= InstalledAppFlow.from\_client\_secrets\_file(CREDENTIALS\_FILE, SCOPES)  
               \# ローカルサーバーを起動し、ユーザーにブラウザでの認証を促す  
               creds \= flow.run\_local\_server(port=0)

           \# 新しい認証情報を次回のために保存  
           with open(TOKEN\_PICKLE\_FILE, 'wb') as token:  
               pickle.dump(creds, token)

       \# 認証済みのサービスオブジェクトを構築して返す  
       service \= build('tasks', 'v1', credentials=creds)  
       return service

   このget\_tasks\_service関数は、初回実行時にInstalledAppFlowを使ってブラウザを起動し、ユーザーにGoogleアカウントでのログインと権限の許可を求めます。認証が成功すると、アクセストークンとリフレッシュトークンがtoken.pickleファイルに保存されます。次回以降の実行では、このファイルから認証情報を読み込むため、ユーザーは再認証する必要がありません。このサービスオブジェクトを使えば、タスクの一覧取得や追加といったAPI呼び出しを行うツールを簡単に作成できます 26。これは非常に実践的で、現実世界のアプリケーション開発に近い例と言えます。

### **Method 3: Integrating with the Broader Ecosystem \- LangChain & MCP**

ADKは閉じたエコシステムではなく、他のフレームワークやプロトコルとの連携も重視しています。

* LangChain Tools:  
  LangChainは、多様なAPIラッパーを含む広範なツールライブラリを提供しています。ADKはこれらのツールを簡単に統合できるため、開発者はAPIクライアントの定型的なコードを書く手間を省けます 27。以下は、LangChainの  
  StackExchangeToolをADKエージェントで利用する例です。  
  Python  
  from google.adk.tools.langchain\_tool import LangchainTool  
  from langchain\_community.tools import StackExchangeTool  
  from langchain\_community.utilities import StackExchangeAPIWrapper

  \# LangChainのツールをインスタンス化  
  stack\_exchange\_langchain\_tool \= StackExchangeTool(api\_wrapper=StackExchangeAPIWrapper())

  \# ADKのLangchainToolでラップする  
  stack\_exchange\_adk\_tool \= LangchainTool(stack\_exchange\_langchain\_tool)

  \# このツールをエージェントのtoolsリストに追加  
  \# bug\_assistant\_agent \= Agent(..., tools=\[stack\_exchange\_adk\_tool\])

  このように、既存のLangChainツールをLangchainToolでラップするだけで、ADKエージェントの能力として追加できます 27。  
* MCP Tools:  
  Model Context Protocol (MCP)は、AIエージェントとツールの間の通信を標準化するためのオープンプロトコルです 6。MCPを利用することで、エージェントはツールがどのように実装されているかを意識することなく、標準化された方法でツールを呼び出せます。これは、特にエンタープライズ環境において、ツールの再利用性と管理性を高めます。以下は、GitHubが提供するリモートMCPサーバーに接続し、そのツールを利用する例です。  
  Python  
  import os  
  from google.adk.tools.mcp\_tool import MCPToolset, StreamableHTTPConnectionParams

  \# GitHubのMCPサーバーに接続  
  github\_mcp\_tools \= MCPToolset(  
      connection\_params=StreamableHTTPConnectionParams(  
          url="https://api.githubcopilot.com/mcp/",  
          headers={  
              "Authorization": "Bearer " \+ os.getenv("GITHUB\_PERSONAL\_ACCESS\_TOKEN"),  
          },  
      ),  
      \# 利用するツールをフィルタリング（読み取り専用のツールのみ）  
      tool\_filter=\[  
          "search\_repositories",  
          "search\_issues",  
          "get\_issue",  
      \]  
  )

  \# このツールセットをエージェントのtoolsリストに追加  
  \# dev\_ops\_agent \= Agent(..., tools=\[\*github\_mcp\_tools\])

  この例では、MCPToolsetを使ってGitHubのMCPエンドポイントに接続し、利用したいツールをtool\_filterで指定しています。これにより、エージェントはリモートで提供される標準化されたツール群を、あたかもローカルのツールであるかのように利用できます 27。

## **Section 6: マルチエージェントシステムへの拡張**

### **The Power of Collaboration: Why Use Multiple Agents?**

単一のエージェントで複雑な問題を解決しようとすると、プロンプト（指示）が肥大化し、管理が困難になることがあります。マルチエージェントシステムは、このような複雑な問題を、より小さく管理しやすいタスクに分割し、それぞれを専門のエージェントに担当させるアプローチです。これにより、システム全体の堅牢性と保守性が向上します 4。例えば、ブログ記事を生成するという大きなタスクを、「アイデア出し」「執筆」「フォーマット」という3つの専門エージェントの協業によって実現できます。

### **Orchestration and Delegation**

マルチエージェントシステムの鍵となるのが、「オーケストレーション」と「デリゲーション（委任）」です。ADKでは、親となるエージェント（ルーターエージェントとも呼ばれる）が、受け取ったタスクの内容を判断し、それを処理するのに最も適した子エージェントにタスクを委任します 4。

この委任のメカニズムの中心にあるのは、LlmAgentの推論能力です。ルーターエージェントのLLMは、子エージェントのdescription（機能説明）を読み取り、現在のタスクに最も合致するエージェントを選択します 4。このため、子エージェントの

descriptionを明確かつ具体的に記述することが、適切なデリゲーションのために非常に重要になります。

技術的には、AgentToolという特殊なツールを使って、あるエージェントを別のエージェントのツールとして扱えるようにします。これにより、エージェント間の階層的な連携が可能になります 3。

### **Practical Example: The "Blog Post Generation Team"**

ここでは、ブログ記事を生成する「チーム」として機能するマルチエージェントシステムを構築します。このシステムは、決定論的なワークフローで動作するSequentialAgentによって統括されます 9。

1. Idea Agent (アイデア出し担当):  
   ブログ記事のトピックに関するアイデアをブレインストーミングするLlmAgentです。  
   Python  
   idea\_agent \= LlmAgent(  
       name="idea\_agent",  
       model="gemini-1.5-flash",  
       description="特定のトピックに関する創造的なブログ投稿のアイデアをブレインストーミングする。",  
       instruction="あなたはブログ記事のアイデアを出す専門家です。与えられたトピックについて、4〜6個の魅力的なタイトル案を箇条書きで提案してください。"  
   )

2. Writer Agent (執筆担当):  
   アイデアを基に、記事の草稿を作成するLlmAgentです。  
   Python  
   writer\_agent \= LlmAgent(  
       name="writer\_agent",  
       model="gemini-1.5-flash",  
       description="アイデアやアウトラインを基に、ブログ記事の草稿を執筆する。",  
       instruction="あなたはプロのライターです。与えられたアイデアリストの中から最も優れたものを1つ選び、それに基づいて約300語のブログ記事の草稿を作成してください。"  
   )

3. Formatter Agent (フォーマット担当):  
   草稿を整形し、公開可能なMarkdown形式にするLlmAgentです。  
   Python  
   formatter\_agent \= LlmAgent(  
       name="formatter\_agent",  
       model="gemini-1.5-flash",  
       description="テキストの草稿をクリーンなMarkdown形式にフォーマットする。",  
       instruction="あなたはMarkdownの専門家です。与えられた草稿に見出し、小見出し、箇条書きなどを適切に使用して、読みやすいMarkdown形式に整形してください。"  
   )

4. Orchestrator Agent (統括担当):  
   これらの専門エージェントを順番に実行するSequentialAgent（WorkflowAgentの一種）です。SequentialAgentはLLMを使わず、定義された順序で子エージェントを確定的に実行します。  
   Python  
   from google.adk.agents import SequentialAgent

   \# 上記で定義した3つのLlmAgentを子エージェントとして指定  
   blog\_pipeline\_agent \= SequentialAgent(  
       name="blog\_pipeline\_agent",  
       sub\_agents=\[idea\_agent, writer\_agent, formatter\_agent\]  
   )

   このblog\_pipeline\_agentに「AIエージェントの未来」といったトピックを与えると、まずidea\_agentがアイデアを出し、その出力がwriter\_agentに渡されて草稿が書かれ、最後にその草稿がformatter\_agentに渡されて整形される、という一連のプロセスが自動的に実行されます 10。このように、  
   WorkflowAgentを使うことで、予測可能で信頼性の高いエージェントパイプラインを簡単に構築できます。

## **Section 7: 会話の記憶と永続化 \- セッション管理の応用**

単発の応答で完結するタスクとは異なり、人間との自然な対話では、過去のやり取りを記憶し、文脈を維持することが不可欠です 18。このセクションでは、ADKが提供するセッション管理機能を応用し、会話の文脈を維持・永続化する方法について掘り下げます。

### **Beyond Single Turns: The Need for Session Persistence**

これまでの例では、adk webコマンドが裏側でセッション管理を行っていました。しかし、より複雑なアプリケーションや、Web UIを介さずにエージェントを直接実行する場合には、セッションを明示的に管理する必要があります。セッション管理を行わないと、エージェントは毎回の対話で記憶を失い、「前に何を話したか」を覚えておくことができません。

### **The SessionService: Your Conversation's Database**

ADKでは、SessionServiceがセッションのライフサイクル（作成、取得、更新、削除）を管理する責任を担います 20。ADKは、用途に応じて選択できるいくつかの

SessionService実装を提供しています。

* **InMemorySessionService:**  
  * **特徴:** 全てのセッションデータをアプリケーションのメモリ上に保存します。特別な設定は不要で、ローカルでのテストや迅速な開発に最適です。  
  * **注意点:** アプリケーションを再起動すると、全ての会話データが失われる揮発性のストレージです 20。  
* **DatabaseSessionService:**  
  * **特徴:** SQLite、PostgreSQL、MySQLなどのリレーショナルデータベースにセッションデータを永続的に保存します。データベースへの接続URLを指定するだけで利用できます。  
  * **用途:** アプリケーションの再起動後も会話の履歴を保持したい場合に適しています 20。  
* **VertexAiSessionService:**  
  * **特徴:** Google CloudのVertex AI Agent Engineを利用した、フルマネージドでスケーラブルなセッション管理サービスです。  
  * **用途:** 本番環境での運用や、他のVertex AI機能との連携を想定した、最も堅牢な選択肢です 20。

### **Reading and Writing to Session State**

セッション内の複数ターンにわたって情報を引き継ぐには、session.stateを使用します。ツール関数内では、tool\_contextオブジェクトを通じて現在のセッションのstateにアクセスできます。stateはPythonの辞書のように振る舞い、自由にデータの読み書きが可能です。

以下は、ユーザーが指定した通貨をstateに保存し、次のターンでその通貨を再利用するツールの概念的な例です。

Python

def set\_preferred\_currency(currency\_code: str, tool\_context) \-\> dict:  
    """ユーザーの希望通貨をセッション状態に保存します。"""  
    \# tool\_context.stateに書き込む  
    tool\_context.state\['preferred\_currency'\] \= currency\_code.upper()  
    return {"status": "success", "message": f"希望通貨を{currency\_code.upper()}に設定しました。"}

def get\_price\_in\_preferred\_currency(tool\_context) \-\> dict:  
    """保存された希望通貨で価格を表示します。"""  
    \# tool\_context.stateから読み込む  
    currency \= tool\_context.state.get('preferred\_currency', 'USD') \# デフォルトはUSD  
    price \= 100 \# 何らかの基本価格  
    \# ここで通貨に応じた価格計算を行う  
    return {"status": "success", "price": f"{price} {currency}"}

最初のツール呼び出しでset\_preferred\_currencyを実行すると、stateに'preferred\_currency': 'JPY'のような情報が保存されます。その後、ユーザーが「価格を教えて」と尋ねると、エージェントはget\_price\_in\_preferred\_currencyツールを呼び出し、stateから'JPY'を読み取って応答を生成できます。このようにして、stateは会話の短期的な記憶として機能します 16。

### **Running an Agent from a Script**

adk web UIを使わずに、Pythonスクリプトから直接エージェントを対話的に実行することも可能です。そのためには、RunnerオブジェクトとSessionServiceを明示的に初期化し、セッションIDを介して会話のコンテキストを維持します。

以下は、InMemorySessionServiceを使用して、コンソールで対話的にエージェントを実行するスクリプトの例です。

Python

import asyncio  
from google.adk.runners import Runner  
from google.adk.sessions import InMemorySessionService  
from google.adk.contents import content\_from\_text

\# 以前に定義したエージェント（例: weather\_time\_agent）をインポート  
\# from my\_agent\_project.agent import root\_agent  
\# この例ではダミーエージェントを使用  
from google.adk.agents import Agent  
root\_agent \= Agent(name="dummy\_agent", model="gemini-1.5-flash", instruction="Respond briefly.")

async def main():  
    \# 1\. SessionServiceを初期化  
    session\_service \= InMemorySessionService()  
      
    \# 2\. Runnerを初期化  
    runner \= Runner(session\_service=session\_service)  
      
    \# アプリケーションとユーザーの情報を定義  
    APP\_NAME \= "console\_chat\_app"  
    USER\_ID \= "user\_001"  
      
    \# 3\. 新しいセッションを作成  
    session \= await session\_service.create\_session(app\_name=APP\_NAME, user\_id=USER\_ID)  
    print(f"新しいセッションを開始しました。ID: {session.id}")  
    print("チャットを開始します。（終了するには 'quit' と入力してください）")  
      
    \# 4\. ユーザーからの入力を受け付けるループ  
    while True:  
        user\_input \= input("You \> ")  
        if user\_input.lower() \== 'quit':  
            break  
              
        \# 5\. runner.run\_async()を呼び出し、セッションIDを渡す  
        events \= runner.run\_async(  
            agent=root\_agent,  
            session\_id=session.id,  
            user\_id=USER\_ID,  
            \# ユーザー入力をADKのContent形式に変換  
            content=content\_from\_text(user\_input)  
        )  
          
        print("Agent \> ", end="", flush=True)  
        \# 6\. エージェントからの応答を非同期で処理して表示  
        final\_response \= ""  
        async for event in events:  
            if event.is\_agent\_response():  
                text\_content \= event.stringify\_content()  
                print(text\_content, end="", flush=True)  
                final\_response \+= text\_content  
        print() \# 改行

if \_\_name\_\_ \== "\_\_main\_\_":  
    asyncio.run(main())

このスクリプトは、RunnerとSessionServiceをセットアップし、create\_sessionで会話を開始します。ループ内でユーザーからの入力を受け取り、runner.run\_asyncを呼び出す際に必ずsession.idを渡すことで、会話のコンテキストが維持されます 19。これにより、エージェントは複数ターンにわたる対話の文脈を記憶し続けることができます。

## **Section 8: 本番環境への道 \- 評価とデプロイ**

AIエージェントを構築することは、パズルの半分に過ぎません。そのエージェントが本番環境で期待通りに、そして確実に動作することを保証するためには、体系的な評価と信頼性の高いデプロイ戦略が不可欠です。ADKは、このライフサイクルの最終段階においても、開発者を強力にサポートします。

### **Evaluating Agent Performance**

エージェントの振る舞いは、特にLLMを使用する場合、本質的に非決定的です。そのため、本番投入前にその性能と正確性を検証するプロセスが極めて重要になります 4。ADKは、この目的のために組み込みの評価フレームワークを提供しています。

このフレームワークでは、あらかじめ定義されたテストケース（例: test.jsonファイル）を用いて、エージェントの性能を体系的に評価できます。評価の対象は、エージェントが生成する最終的な応答の品質だけでなく、その応答に至るまでの中間ステップ（どのツールを、どのような引数で呼び出したかなど）の実行軌跡も含まれます 4。

AgentEvaluator.evaluate()といった関数を使用することで、これらの評価をプログラム的に実行し、CI/CDパイプラインに組み込むことも可能です。これにより、コードの変更がエージェントの振る舞いに意図しない悪影響を与えていないかを、継続的に自動でテストすることができます。

### **Deployment Options: From Local to Cloud**

ADKは、開発から本番までの移行をスムーズにするための、柔軟なデプロイオプションを提供しています。これは、デプロイを利用者任せにする多くのフレームワークに対する大きな利点です。ローカルでの開発から、シンプルなクラウドデプロイ、そしてフルマネージドのランタイムまで、プロジェクトの成熟度や要件に応じて最適な選択が可能です。

1. **ローカル開発サーバー (adk web):** 開発の初期段階では、このコマンド一つで起動するローカルUIが最も効率的です 7。  
2. **カスタムAPIサーバー:** より細かい制御や既存のシステムとの統合が必要な場合、ADKエージェントをFastAPIサーバーとしてラップして実行することもできます 21。  
3. **Cloud Runへのデプロイ:** クラウドへの第一歩として、コンテナベースのデプロイが一般的です。ADKは、adk deploy cloudrunというCLIコマンドを提供しており、このプロセスを大幅に簡素化します 30。  
4. **Vertex AI Agent Engineへのデプロイ:** 最大限のスケーラビリティと最小限の運用負荷を求める場合、最終的な目的地はフルマネージドのVertex AI Agent Engineとなります 4。

この段階的なオプションは、開発者が自身のスキルレベルやインフラ要件に合わせて、無理なく本番環境へと移行できる、明確で整備された道筋を提供します。

* Option 1: Cloud Run (Serverless Containers)  
  Cloud Runは、サーバーの管理を意識することなくコンテナを実行できる、Google Cloudのサーバーレスプラットフォームです。インフラストラクチャをある程度自身で制御したい場合に適しています。ADKは、エージェントアプリケーションをCloud Runにデプロイするための簡単なCLIコマンドを提供しています 30。  
  Bash  
  adk deploy cloudrun

  このコマンドは、エージェントのコードをコンテナ化し、Cloud Runサービスとしてデプロイするまでの一連のプロセスを自動化します。  
* Option 2: Vertex AI Agent Engine (Fully Managed)  
  Agent Engineは、ADKエージェントのための、フルマネージドでエンタープライズグレードのランタイム環境です。インフラ管理、スケーリング、セキュリティ、モニタリングといった運用上の懸念事項をすべてGoogle Cloudが処理するため、開発者はエージェントのロジック開発に集中できます 6。

  Agent Engineは、ADKだけでなく、LangChainなど他のフレームワークで構築されたエージェントのデプロイもサポートしています。また、短期記憶（セッション）と長期記憶の両方をサポートしており、人間らしい文脈を維持した対話を実現します 6。最も簡単かつ堅牢に本番環境を構築したい場合、Agent Engineが最適な選択肢となります。

## **Section 9: 結論と次のステップ**

### **Summary: The Power and Nuance of ADK**

Google Agents SDK (ADK)は、単なるライブラリを超え、AIエージェント開発に構造と規律をもたらす包括的なフレームワークです。その主な強みは、以下の点に集約されます。

* **構造化されたエンタープライズ対応のアプローチ:** ソフトウェア開発のベストプラクティスを取り入れ、保守性と信頼性の高いエージェント構築を可能にします。  
* **強力なマルチエージェントオーケストレーション:** 複雑なタスクを専門エージェントに分割し、協調させることで、スケーラブルなシステムを設計できます。  
* **柔軟なツールエコシステム:** 内部関数から外部API、サードパーティライブラリ、MCPプロトコルまで、多様なツールをシームレスに統合できます。  
* **明確なデプロイパス:** ローカルでの開発から、Cloud Run、そしてフルマネージドのVertex AI Agent Engineまで、本番環境へのスムーズな移行をサポートします。

一方で、コミュニティからはその学習コストの高さや複雑さについてのフィードバックも見られます 3。ADKは、初期の単純さよりも、長期的な堅牢性、スケーラビリティ、保守性を優先する設計思想を持っていると言えるでしょう。そのため、迅速なプロトタイピングよりも、本番運用を見据えた本格的なアプリケーション開発において、その真価を発揮するフレームワークです。

### **The Broader Ecosystem: Agent Builder and A2A**

ADKは、Googleのより大きなビジョンの一部です。Google Cloudが提供する**Agent Builder**プラットフォームは、ADKを含む様々なツールやサービスを統合し、エージェント開発をエンドツーエンドで支援するものです 6。

さらに、Googleが推進するオープンな**Agent2Agent (A2A) プロトコル**は、このエコシステムの将来を考える上で極めて重要です。A2Aは、ADK、LangGraph、Crew.aiなど、どのフレームワークで構築されたかに関わらず、エージェント同士が通信できるようにするための「普遍的な通信規格」を目指しています 6。これは、ベンダーやフレームワークにロックインされることなく、様々なエージェントが協調して動作する、真にオープンなAIコラボレーションの未来を示唆しています。

### **Resources for Your Journey**

ADKを用いたエージェント開発の旅を続けるために、以下のリソースが役立つでしょう。

* **Official ADK Documentation:**  
  * ADKの機能、チュートリアル、APIリファレンスが網羅された公式ドキュメントです 1。  
* **ADK Python GitHub Repository:**  
  * ソースコード、イシュー、最新の変更点などを確認できます 1。  
* **ADK Sample Agents:**  
  * 様々なユースケースに対応するサンプルエージェントのコレクションです。実践的なコード例として非常に参考になります 1。  
* **Streaming and Advanced Tutorials:**  
  * 音声・映像ストリーミングや、より高度な機能に関するチュートリアルが提供されています 31。

#### **引用文献**

1. google/adk-python: An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control. \- GitHub, 6月 27, 2025にアクセス、 [https://github.com/google/adk-python](https://github.com/google/adk-python)  
2. Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)  
3. Just did a deep dive into Google's Agent Development Kit (ADK). Here are some thoughts, nitpicks, and things I loved (unbiased) : r/AI\_Agents \- Reddit, 6月 27, 2025にアクセス、 [https://www.reddit.com/r/AI\_Agents/comments/1jvsu4l/just\_did\_a\_deep\_dive\_into\_googles\_agent/](https://www.reddit.com/r/AI_Agents/comments/1jvsu4l/just_did_a_deep_dive_into_googles_agent/)  
4. Agent Development Kit: Making it easy to build multi-agent applications, 6月 27, 2025にアクセス、 [https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)  
5. Google's New Agent Developer Kit: What You Need to Know \- WebMob Technologies, 6月 27, 2025にアクセス、 [https://webmobtech.com/blog/googles-new-agent-developer-kit-what-you-need-to-know/](https://webmobtech.com/blog/googles-new-agent-developer-kit-what-you-need-to-know/)  
6. Vertex AI Agent Builder | Google Cloud, 6月 27, 2025にアクセス、 [https://cloud.google.com/products/agent-builder](https://cloud.google.com/products/agent-builder)  
7. Quickstart: Build an agent with the Agent Development Kit ..., 6月 27, 2025にアクセス、 [https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart)  
8. A Step-by-Step Guide to Using Google's Agent Development Kit (ADK) | by Munsif Raza, 6月 27, 2025にアクセス、 [https://medium.com/@munsifrazaofficial/a-step-by-step-guide-to-using-googles-agent-development-kit-adk-73dd467cae44](https://medium.com/@munsifrazaofficial/a-step-by-step-guide-to-using-googles-agent-development-kit-adk-73dd467cae44)  
9. Easy Guide to Building Your First AI Agent in Python with Google ADK \- Medium, 6月 27, 2025にアクセス、 [https://medium.com/@proflead/easy-guide-to-building-your-first-ai-agent-in-python-with-google-adk-73fabd40c0e2](https://medium.com/@proflead/easy-guide-to-building-your-first-ai-agent-in-python-with-google-adk-73fabd40c0e2)  
10. The Complete Guide to Google's Agent Development Kit (ADK) \- Sid Bharath, 6月 27, 2025にアクセス、 [https://www.siddharthbharath.com/the-complete-guide-to-googles-agent-development-kit-adk/](https://www.siddharthbharath.com/the-complete-guide-to-googles-agent-development-kit-adk/)  
11. Quickstart \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/get-started/quickstart/](https://google.github.io/adk-docs/get-started/quickstart/)  
12. Agents \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/agents/](https://google.github.io/adk-docs/agents/)  
13. LLM agents \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/agents/llm-agents/](https://google.github.io/adk-docs/agents/llm-agents/)  
14. Building AI Agents with Google Agent Development Kit (ADK), Java and MCP Tools : Build a learning… | by Code Wiz | Javarevisited | May, 2025 | Medium, 6月 27, 2025にアクセス、 [https://medium.com/javarevisited/building-ai-agents-with-google-agent-development-kit-adk-java-and-mcp-tools-build-a-learning-0acc29a4e1cb](https://medium.com/javarevisited/building-ai-agents-with-google-agent-development-kit-adk-java-and-mcp-tools-build-a-learning-0acc29a4e1cb)  
15. Build Your First Intelligent Agent Team: A Progressive Weather Bot with ADK \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/tutorials/agent-team/](https://google.github.io/adk-docs/tutorials/agent-team/)  
16. Tools \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/tools/](https://google.github.io/adk-docs/tools/)  
17. Develop an Agent Development Kit agent | Generative AI on Vertex AI \- Google Cloud, 6月 27, 2025にアクセス、 [https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk)  
18. Introduction to Conversational Context: Session, State, and Memory ..., 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/sessions/](https://google.github.io/adk-docs/sessions/)  
19. Google Agent Development Kit (ADK): Sessions, Memory, and Runtime \- Medium, 6月 27, 2025にアクセス、 [https://medium.com/@danushidk507/google-agent-development-kit-adk-sessions-memory-and-runtime-705c0730892a](https://medium.com/@danushidk507/google-agent-development-kit-adk-sessions-memory-and-runtime-705c0730892a)  
20. Session \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/sessions/session/](https://google.github.io/adk-docs/sessions/session/)  
21. Building AI Agents with Google ADK, FastAPI, and MCP \- DEV Community, 6月 27, 2025にアクセス、 [https://dev.to/timtech4u/building-ai-agents-with-google-adk-fastapi-and-mcp-26h7](https://dev.to/timtech4u/building-ai-agents-with-google-adk-fastapi-and-mcp-26h7)  
22. Python \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/](https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/)  
23. Google's ADK Agent Development kit | by abhinav singhal \- Medium, 6月 27, 2025にアクセス、 [https://abhinav1singhal.medium.com/googles-adk-agent-development-kit-8a76d18a32ce](https://abhinav1singhal.medium.com/googles-adk-agent-development-kit-8a76d18a32ce)  
24. Google ADK Masterclass Part 2: Adding Tools to Your Agents \- Saptak Sen, 6月 27, 2025にアクセス、 [https://saptak.in/writing/2025/05/10/google-adk-masterclass-part2](https://saptak.in/writing/2025/05/10/google-adk-masterclass-part2)  
25. Communicating Between uAgents and Google ADK: A Step-by-Step Guide | by GautamManak | Fetch.ai | Medium, 6月 27, 2025にアクセス、 [https://medium.com/fetch-ai/communicating-between-uagents-and-google-adk-a-step-by-step-guide-c15f355a8dcf](https://medium.com/fetch-ai/communicating-between-uagents-and-google-adk-a-step-by-step-guide-c15f355a8dcf)  
26. Your First ADK Agent: Building a Google Tasks To-Do Manager \- Medium, 6月 27, 2025にアクセス、 [https://medium.com/google-cloud/your-first-adk-agent-building-a-google-tasks-to-do-manager-c3d4d2c317cd](https://medium.com/google-cloud/your-first-adk-agent-building-a-google-tasks-to-do-manager-c3d4d2c317cd)  
27. Tools Make an Agent: From Zero to Assistant with ADK | Google ..., 6月 27, 2025にアクセス、 [https://cloud.google.com/blog/topics/developers-practitioners/tools-make-an-agent-from-zero-to-assistant-with-adk/](https://cloud.google.com/blog/topics/developers-practitioners/tools-make-an-agent-from-zero-to-assistant-with-adk/)  
28. Multi-Turn Conversations \- Oracle Help Center, 6月 27, 2025にアクセス、 [https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/adk/api-reference/examples/multi-turns.htm](https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/adk/api-reference/examples/multi-turns.htm)  
29. Manage sessions with Agent Development Kit | Generative AI on ..., 6月 27, 2025にアクセス、 [https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-sessions-adk](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-sessions-adk)  
30. Google Agent Development Kit: EASIEST way to create AI Agents\! \- YouTube, 6月 27, 2025にアクセス、 [https://www.youtube.com/watch?v=RFFcBkSupxk](https://www.youtube.com/watch?v=RFFcBkSupxk)  
31. ADK Tutorials\! \- Agent Development Kit \- Google, 6月 27, 2025にアクセス、 [https://google.github.io/adk-docs/tutorials/](https://google.github.io/adk-docs/tutorials/)