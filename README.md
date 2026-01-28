# MLOps API (ECS / GitHub Actions)

## 概要
FastAPI アプリケーションを Docker 化し、  
GitHub Actions → Amazon ECR → Amazon ECS(Fargate) へ  
**自動デプロイ**する構成を実装しています。

本リポジトリは **MLOps / DevOps 初級レベルの実装例**として、
- CI/CD
- コンテナ運用
- AWS 権限設計（最小権限）
を目的に構築しています。

---

## 構成図（論理）

Developer
|
| git push (main)
v
GitHub Actions
|
| Docker build
| Docker push
v
Amazon ECR
|
| Task Definition 更新
v
Amazon ECS (Fargate)
|
| 起動確認
v
/health

## デプロイフロー

1. main ブランチに push
2. GitHub Actions が起動
3. Docker イメージを build
4. Amazon ECR に push
5. ECS タスク定義を更新
6. ECS サービスが新タスクを起動

※ README などのドキュメント変更のみの場合は  
**デプロイは実行されない**よう制御しています。

## エンドポイント

### `/health`
- アプリケーションの起動確認用
- ECS / ALB のヘルスチェック用途
- デプロイ検証時に使用

## 起動確認ルール（重要）
/health 確認が 必須 な変更

以下の変更時は、ECS のタスク数を 1 にして /health を確認します。

Dockerfile / requirements.txt の変更

GitHub Actions / deploy.yml の変更

ECS タスク定義（CPU / メモリ / ポート / ログ）

AWS ネットワーク設定（Security Group / Subnet）

起動コマンド（uvicorn 等）

/health 確認を 省略可能 な変更

アプリロジックのみの変更（CI成功前提）

README などのドキュメント変更

## コスト運用ポリシー

通常時：ECS サービスの desired count = 0

検証時：desired count = 1

/health 確認後、すぐ 0 に戻す

※ Fargate は起動中のみ課金されます。

## CI / CD の役割分担
CI（Pull Request）

Python import チェック

Docker build チェック

PR 作成時のみ実行

CD（main push）

Docker build

ECR push

ECS デプロイ

## IAM 権限設計

GitHub Actions 用 IAM ユーザーを作成

AdministratorAccess 不使用

必要最小限の権限のみ付与

ECR（特定リポジトリ）

ECS（TaskDefinition / Service 更新）

iam:PassRole（ecs-tasks.amazonaws.com 限定）

## トラブルシューティング
GitHub Actions が失敗する

Actions のログを確認

AWS Secrets / IAM 権限を確認

## ECS タスクが STOPPED になる

ECS → タスク → Stopped reason を確認

CloudWatch Logs を確認

CannotPullContainerError

ECR リポジトリのリージョン

イメージタグの存在

リポジトリ名の一致

## RUNNING だがアクセスできない

Security Group のインバウンド（8000）

パブリック IP の有無

アプリの listen host / port

## 補足

本構成は学習・検証目的のため、

オートスケール

ALB

本番監視
は最小限としています。