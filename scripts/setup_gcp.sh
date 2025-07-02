#!/usr/bin/env bash
# =============================================
# Agri_AI - GCP 初期セットアップスクリプト
# ---------------------------------------------
# 使い方:
#   ./scripts/setup_gcp.sh <GCP_PROJECT_ID>
#
# このスクリプトは次を実行します。
#   1. gcloud でプロジェクトを選択
#   2. 必要な API (Vertex AI / Secret Manager) を有効化
#   3. サービスアカウントを作成し、必要ロールを付与
#   4. サービスアカウント鍵 (JSON) を生成
#   5. 生成した鍵ファイル名を出力
# ---------------------------------------------
set -euo pipefail

PROJECT_ID=${1:-}
if [ -z "$PROJECT_ID" ]; then
  echo "Usage: $0 <GCP_PROJECT_ID>" >&2
  exit 1
fi

SA_NAME="agri-ai-sa"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
KEY_FILE="service-account-key.json"

# 1) プロジェクト設定
printf "\n▶️  gcloud プロジェクトを %s に設定\n" "$PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# 2) 必要 API を有効化
printf "\n▶️  必要な API を有効化 (Vertex AI, Secret Manager)\n"
gcloud services enable \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com

# 3) サービスアカウント作成
printf "\n▶️  サービスアカウント %s を作成 (既にあれば無視)\n" "$SA_EMAIL"
gcloud iam service-accounts create "$SA_NAME" \
  --display-name "Agri AI Service Account" || true

# 4) ロール付与
printf "\n▶️  必要ロールを付与\n"
for ROLE in roles/aiplatform.user roles/storage.objectAdmin; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="$ROLE" --quiet || true
done

# 5) 鍵の生成
printf "\n▶️  サービスアカウント鍵を生成 (%s)\n" "$KEY_FILE"
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account "$SA_EMAIL" --quiet

printf "\n✅  完了: %s に鍵ファイルを生成しました。\n" "$KEY_FILE" 