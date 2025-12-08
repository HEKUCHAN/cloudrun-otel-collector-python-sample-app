# Cloud Run デプロイ（yamlファイル）

このディレクトリは、Cloud Run へデプロイするためのマニフェスト（`cloudrun.yaml`）と、その関連手順をまとめています。FastAPI のアプリケーション本体は `${PROJECT_ROOT}/app` にあり、OpenTelemetry Collector の設定ファイルは `${PROJECT_ROOT}/otel/collector-config.yaml` にあります。

この Cloud Run manifest は、Google が提供している OpenTelemetry Collector（sidecar）を利用する構成になっています。公開している `cloudrun.yaml` はサンプルファイルになっているので、適宜必要なものを更新してください。

# 使用方法

## 1. yamlファイルの不足部分を修正

`cloudrun.yaml` をコピーして作業用ファイルを作成し、適宜必要な変数を変更してください。

```bash
cp cloudrun.yaml cloudrun-deploy.yaml
```

修正が必要な箇所:

```yaml
...
    spec:
      containers:
        - name: app
          image: APP_IMAGE # TODO: このサービス用にビルドしたアプリのコンテナイメージに変更する
          ports:
            - containerPort: 8080
          env:
            # PORT環境変数は削除（Cloud Runが自動設定）
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
...
        - name: collector
          image: "us-docker.pkg.dev/cloud-ops-agents-artifacts/google-cloud-opentelemetry-collector/otelcol-google:0.137.0"
          args:
            - --config=/etc/otelcol-google/config.yaml
          volumeMounts:
            - mountPath: /etc/otelcol-google
              name: collector-config
          startupProbe:  # TODO: startupProbeを追加（必須）
            httpGet:
              path: /
              port: 13133
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 10
            failureThreshold: 10
...
      volumes:
        - name: collector-config
          secret:
            secretName: OTEL_COLLECTOR_CONFIG # TODO: Collector用config設定を格納した Secret の名前に変更する
            items:
              - key: latest
                path: config.yaml
```

手動で修正が必要な箇所:
- `APP_IMAGE`: 自分でビルド・push したアプリケーションのコンテナイメージ名
- `OTEL_COLLECTOR_CONFIG`: OpenTelemetry Collector の設定ファイルを格納した Secret の名前
- `PORT` 環境変数: Cloud Run が自動設定するため削除
- `startupProbe`: collector コンテナに必須（ポート 13133 でヘルスチェック）

## 2. Secret Manager に Collector の設定を登録する

Collector の設定ファイル（`${PROJECT_ROOT}/otel/collector-config.yaml`）を Secret Manager に登録します。
このファイルは Cloud Run で動作するように必要な設定（health_check extension、debug exporter等）が既に含まれています。

```bash
gcloud secrets create otel-collector-config \
  --replication-policy="automatic" \
  --project=<PROJECT_ID>

gcloud secrets versions add otel-collector-config \
  --data-file=../../otel/collector-config.yaml \
  --project=<PROJECT_ID>
```

設定ファイルを更新した場合は、`gcloud secrets versions add ...` のコマンドだけ再実行すれば、最新バージョンとして登録されます。
`cloudrun-deploy.yaml` の `secretName` に指定した名前(例: `otel-collector-config`)と一致している必要があります。

### Secret へのアクセス権限を付与

Cloud Run のサービスアカウントに Secret Manager へのアクセス権限を付与します。

```bash
gcloud secrets add-iam-policy-binding otel-collector-config \
  --member="serviceAccount:<PROJECT_NUMBER>-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=<PROJECT_ID>
```

`<PROJECT_NUMBER>` はプロジェクト番号(数字)に置き換えてください。プロジェクト番号は以下のコマンドで確認できます:

```bash
gcloud projects describe <PROJECT_ID> --format="value(projectNumber)"
```

## 4. Docker イメージを Artifact Registry に push する

FastAPI のアプリケーションをビルドし、Artifact Registry に push します。
イメージ名は `cloudrun-deploy.yaml` の `image: APP_IMAGE` と同じものを指定してください。

まず、Artifact Registry のリポジトリを作成します(初回のみ):

```bash
gcloud artifacts repositories create <REPO> \
  --repository-format=docker \
  --location=asia-northeast1 \
  --project=<PROJECT_ID>
```

Docker 認証を設定します:

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev --project=<PROJECT_ID>
```

イメージをビルドして push します。Cloud Run は `linux/amd64` アーキテクチャを必要とするため、`--platform` と `--provenance=false` オプションを指定します:

```bash
docker buildx build --platform linux/amd64 \
  -t asia-northeast1-docker.pkg.dev/<PROJECT_ID>/<REPO>/fastapi-todo:latest \
  -f ../../docker/Dockerfile . \
  --push --provenance=false
```

`<PROJECT_ID>` や `<REPO>` は自分のプロジェクト・リポジトリ名に置き換えてください。

## 5. Cloud Run へデプロイ

作業用ファイル `cloudrun-deploy.yaml` を修正したあと、次のコマンドで Cloud Run に反映します。

```bash
gcloud run services replace cloudrun-deploy.yaml \
  --region=asia-northeast1 \
  --project=<PROJECT_ID>
```

リージョンを変更したい場合は `--region` の値を変更してください。

注意: 初回デプロイ時や Collector の設定を更新した後、古い設定がキャッシュされる場合があります。その場合は一度サービスを削除してから再度デプロイしてください:

```bash
gcloud run services delete <SERVICE_NAME> --region=asia-northeast1 --project=<PROJECT_ID> --quiet
gcloud run services replace cloudrun-deploy.yaml --region=asia-northeast1 --project=<PROJECT_ID>
```

## 6. 動作確認

デプロイが完了したら、Cloud Run のエンドポイントに対して実際にリクエストを送り、アプリケーションと Collector が動いているか確認します。

Trace やログは GCP コンソールから確認できます。

```text
Cloud Trace:
  https://console.cloud.google.com/traces/list

Cloud Logging:
  https://console.cloud.google.com/logs/query

Cloud Monitoring:
  https://console.cloud.google.com/monitoring
```

FastAPI 側で OTEL SDK を有効にしていれば、リクエストに応じたトレースが Cloud Trace 上に表示されます。
