# 運用・トラブルシューティング
## コスト運用ポリシー

通常時：ECS サービスの desired count = 0
検証時：desired count = 1
/health 確認後、すぐ 0 に戻す
※ Fargate は起動中のみ課金されます。

## 起動確認ルール（重要）
■/health 確認が 必須 な変更

以下の変更時は、ECS のタスク数を 1 にして /health を確認します。
- Dockerfile / requirements.txt の変更
- GitHub Actions / deploy.yml の変更
- ECS タスク定義（CPU / メモリ / ポート / ログ）
- AWS ネットワーク設定（Security Group / Subnet）
- 起動コマンド（uvicorn 等）

■/health 確認を 省略可能 な変更
- アプリロジックのみの変更（CI成功前提）
- README などのドキュメント変更

## デプロイ確認
- /health が status ok を返す
- model_version が確認できる

## ロールバック手順
- モデル更新コミットを git revert
- GitHub Actions により自動反映
- /health の model_version で確認

## トラブルシューティング
### GitHub Actions が失敗する
- Actions のログを確認
- AWS Secrets / IAM 権限を確認

### ECS タスクが STOPPED になる
- ECS → タスク → Stopped reason を確認
- CloudWatch Logs を確認
- CannotPullContainerError
- ECR リポジトリのリージョン
- イメージタグの存在
- リポジトリ名の一致

### RUNNING だがアクセスできない
- Security Group のインバウンド（8000）
- パブリック IP の有無
- アプリの listen host / port