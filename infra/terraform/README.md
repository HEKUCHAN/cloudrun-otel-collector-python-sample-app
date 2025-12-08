# Cloud Run デプロイ（Terraform）

このディレクトリは、Terraform を使用して Cloud Run へデプロイするための設定ファイルをまとめています。

## 前提条件

- Terraform >= 1.14.0
- Google Cloud SDK (gcloud)
- Docker

## デプロイ手順

### 1. terraform.tfvars ファイルの設定

`terraform.tfvars` ファイルを作成し、必要な変数を設定してください。

```hcl
project_id         = "your-project-id"
region             = "asia-northeast1"
service_name       = "fastapi-todo"
artifact_repo_name = "app"
image_tag          = "latest"
otel_secret_name   = "otel-collector-config"
environment        = "dev"
service_label_env  = "dev"
network_name       = "cloudrun-network"
subnet_name        = "cloudrun-subnet"
subnet_ip_cidr_range = "10.0.0.0/24"
```

### 2. Terraform の初期化

```bash
cd infra/terraform
terraform init
```

### 3. Terraform の実行計画を確認

```bash
terraform plan
```

### 4. Terraform の初回適用（リポジトリ作成）

初回は Cloud Run サービスがエラーになりますが、Artifact Registry リポジトリなどの他のリソースが作成されます。

```bash
terraform apply
```

確認プロンプトで `yes` を入力します。

> **注意**: この時点では Docker イメージが存在しないため、Cloud Run サービスの作成は失敗しまが、動作としては正常です。

### 5. Docker イメージのビルドとプッシュ

Artifact Registry リポジトリが作成されたので、Docker イメージをビルド & プッシュします。

```bash
# プロジェクトルートに移動
cd ../..

# Docker 認証を設定
gcloud auth configure-docker asia-northeast1-docker.pkg.dev --project=<PROJECT_ID>

# イメージをビルド & プッシュ
docker buildx build --platform linux/amd64 \
  -t asia-northeast1-docker.pkg.dev/<PROJECT_ID>/app/fastapi-todo:latest \
  -f docker/Dockerfile . \
  --push --provenance=false
```

### 6. Terraform の再適用

Docker イメージがプッシュされたので、再度 Terraform を適用して Cloud Run サービスを作成します。

```bash
cd infra/terraform
terraform apply
```

## イメージの更新

アプリケーションコードを変更した場合:

1. Docker イメージを再ビルド & プッシュ
2. `terraform apply` を実行してCloud Runサービスを更新

```bash
# Docker イメージを再ビルド & プッシュ
docker buildx build --platform linux/amd64 \
  -t asia-northeast1-docker.pkg.dev/<PROJECT_ID>/app/fastapi-todo:latest \
  -f docker/Dockerfile . \
  --push --provenance=false

# Terraform で更新
cd infra/terraform
terraform apply
```

## クリーンアップ

全てのリソースを削除する場合:

```bash
terraform destroy
```

## トラブルシューティング

### エラー: Image not found

```
Error: Error waiting to create Service: Error code 5, message: Image 'asia-northeast1-docker.pkg.dev/...' not found.
```

**原因**: Docker イメージが Artifact Registry に存在しません。

**解決策**: 手順2を実行して、Docker イメージをビルド & プッシュしてください。

### エラー: Secret not found

Secret Manager のシークレットが見つからないエラーが発生した場合、Terraform が自動的にシークレットとその内容を作成します。`otel/collector-config.yaml` が存在することを確認してください。
