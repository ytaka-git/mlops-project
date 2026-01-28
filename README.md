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

```json
{
  "status": "ok"
}