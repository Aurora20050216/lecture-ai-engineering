# 講義書き起こし修正AIシステム

## 概要

このプロジェクトは、講義の自動書き起こしテキスト（.txt）と講義資料（.pptx）をアップロードし、
AWS Bedrock上のLLM連携によりテキストを整形・修正した結果をダウンロード可能にするWebサービスを構築します。  

---

## ディレクトリ構成

app/ # アプリケーション
docs/ # ドキュメント

---

## 動作環境

- Python 3.9以上
- AWSアカウント・権限

---

## セットアップ・デプロイ手順

1. 依存パッケージをインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. AWSを利用可能にする

```bash
export AWS_ACCESS_KEY_ID="あなたのAWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="あなたのAWS_SECRET_ACCESS_KEY"
export AWS_SESSION_TOKEN="あなたのAWS_SESSION_TOKEN"
```

3. 実行

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. アクセス
http://自分のコンピュータのIPアドレス:8000 にアクセスして、pptxファイルとtxtファイルをアップロードしてください。