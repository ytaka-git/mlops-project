# MLOps API ポートフォリオ(推論API × ECS × CI/CD)

## 概要
FastAPI で実装した **推論 API** を Docker 化し、  
GitHub Actions → Amazon ECR → Amazon ECS(Fargate) へ  
**自動デプロイ・ロールバック可能な構成**を実装した MLOps ポートフォリオです。

学習と推論を分離し、推論ログを CloudWatch Logs に保存することで、  
将来的な再学習につながる構成を確認しています。

## 本リポジトリの目的
本リポジトリは、MLOps / DevOps 初級レベルの実装例として、

- CI/CD パイプライン構築
- コンテナ運用（Docker / ECS）
- AWS 権限設計（最小権限）
- 推論 API の運用・ロールバック

を目的に構築しています。

## 詳細ドキュメント
- [アーキテクチャ詳細](./ARCHITECTURE.md)
- [運用・トラブルシューティング](./RUNBOOK.md)

## 提供機能
- 学習済みモデルを使った推論 API（FastAPI）
- /health による起動・デプロイ確認
- GitHub Actions による自動デプロイ
- モデル更新時の差し替え・ロールバック
- 推論入力・出力を JSON ログとして保存（CloudWatch Logs）

## 技術スタック
- 言語：Python
- 推論API：FastAPI
- 学習：scikit-learn（LogisticRegression）
- コンテナ：Docker
- CI/CD：GitHub Actions
- 実行環境：Amazon ECS (Fargate)
- レジストリ：Amazon ECR
- ログ：CloudWatch Logs
---
## 全体フロー
学習からデプロイまでの全体の流れは以下の通りです。
1. train.py で学習し model.joblib を生成
2. Docker イメージにモデルとAPIを同梱
3. main ブランチに push
4. GitHub Actions が起動
5. ECR に push → ECS にデプロイ
6. ECS 上で推論APIが稼働

※ README などのドキュメント変更のみの場合は  
**デプロイは実行されない**よう制御しています。

## エンドポイント

### GET /health
- APIの起動確認
- 使用中のモデル識別子(model_version)を返却

### POST /predict
- 推論を実行し結果を返却
- 推論時の情報をログとして保存

## IAM 権限設計

GitHub Actions 用 IAM ユーザーを作成し以下の必要最小限の権限のみ付与
- ECR（特定リポジトリ）
- ECS（TaskDefinition / Service 更新）
- iam:PassRole（ecs-tasks.amazonaws.com 限定）

※AdministratorAccess 不使用

## スコープ外
本構成は学習・検証目的のため、以下は最小限としています。

- ALB / オートスケーリング
- 精度監視・ドリフト検知
- 学習の自動化
- 実データの扱い

※ 本ポートフォリオでは正解ラベルは未蓄積です。
　推論ログを基に、後段で正解付与・再学習を行う想定としています。