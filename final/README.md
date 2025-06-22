# 講義書き起こし修正AIシステム

## 概要

このプロジェクトは、講義の自動書き起こしテキスト（.txt）と講義資料（.pptx）をアップロードし、  
簡易的にテキストを整形・修正した結果をダウンロード可能にするWebサービスをAWS Lambda上に構築します。  

将来的にはAWS Bedrock上のLLM連携による高度な修正を目指しています。

---

## ディレクトリ構成

cdk/ # AWS CDKアプリケーション
lambda/ # Lambda関数コード（FastAPIアプリ）
lambda_layer/ # Lambda Layer用Pythonパッケージ
data/ # （任意）サンプルデータ置き場
scripts/ # （任意）補助スクリプト
utils/ # （任意）共通ユーティリティ

---

## 動作環境

- Python 3.9以上
- AWS CLI / CDK v2 インストール済み
- Node.js / npm (CDK依存の可能性あり)
- AWSアカウント・権限

---

## セットアップ・デプロイ手順

1. Lambda Layerの依存パッケージをインストール

```bash
cd lambda_layer/python
pip install -r requirements.txt -t .
cd ../..
```

2. CDKブートストラップ(初回のみ)

```bash
cdk bootstrap
```

3. CDKデプロイ

```bash
cdk deploy
```