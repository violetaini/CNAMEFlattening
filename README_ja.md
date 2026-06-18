<div align="center">

<img src="static/avatar.webp" alt="CNAMEFlattening" width="120" />

# **CNAMEFlattening**

[![CodeQL](https://img.shields.io/github/actions/workflow/status/violetaini/CNAMEFlattening/codeql.yml?branch=main&label=CodeQL&style=for-the-badge&logo=github)](https://github.com/violetaini/CNAMEFlattening/actions/workflows/codeql.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](deploy/huawei_flatten.py)
[![Go](https://img.shields.io/badge/Go-modules-00add8?style=for-the-badge&logo=go&logoColor=white)](go/go.mod)
[![Repo size](https://img.shields.io/github/repo-size/violetaini/CNAMEFlattening?style=for-the-badge)](https://github.com/violetaini/CNAMEFlattening)
[![Stars](https://img.shields.io/github/stars/violetaini/CNAMEFlattening?style=for-the-badge&logo=github)](https://github.com/violetaini/CNAMEFlattening/stargazers)
[![Forks](https://img.shields.io/github/forks/violetaini/CNAMEFlattening?style=for-the-badge&logo=github)](https://github.com/violetaini/CNAMEFlattening/forks)

</div>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_zh.md">简体中文</a> |
  <a href="README_zh-TW.md">繁體中文</a> |
  <a href="README_ja.md">日本語</a>
</p>

CNAMEFlattening は、CDN CNAME の回線別解決結果を DNS A/AAAA レコードへ同期するツールです。CNAME ではなくフラット化されたレコードを権威 DNS ゾーンに置きたい CDN シナリオ向けです。

## 機能

- DNSPod、Huawei Cloud DNS、Alibaba Cloud DNS 向けの Python と Go 実装。
- `deploy/huawei_flatten.py` は現在メンテナンスされている Huawei Cloud DNS 用の本番デプロイ版です。
- DoH と ECS サブネットヒントで CDN の応答を取得し、回線別に A/AAAA レコードを更新します。
- Huawei Cloud API のレート制限時に自動で待機して再試行します。
- DoH タイムアウト、DNS 解決失敗、502 などの一時的なエラーを自動再試行します。
- cron デプロイ向けで、ラッパースクリプトは `flock` により並行実行を防ぎます。
- 不足しているレコードの自動作成と TTL 設定に対応します。

## リポジトリ構成

```text
deploy/                Huawei Cloud DNS 本番ランナーとデプロイ文書
python/                DNSPod、Huawei Cloud、Alibaba Cloud の旧 Python スクリプト
go/                    DNSPod と Huawei Cloud の Go 実装
static/                図表とリポジトリアセット
```

## Huawei Cloud デプロイ

現在のデプロイ手順は [deploy/README.md](deploy/README.md) にあります。

一般的な実行レイアウト：

```text
/opt/CNAMEFlattening/
/usr/local/bin/huawei-cname-flatten
/etc/cname-flattening/huawei.env
/var/log/cname-flattening/huawei.log
```

cron 例：

```cron
*/5 * * * * root /usr/bin/flock -n /var/run/cname-flattening-huawei.lock /usr/local/bin/huawei-cname-flatten >> /var/log/cname-flattening/huawei.log 2>&1
```

成功時は通常、ログが次のように終わります。

```text
done changed=<n> skipped=<n> errors=0
elapsed=<seconds>s
```

## 設定の安全性

実際の DNS プロバイダー認証情報、クラウドアクセスキー、API トークン、秘密鍵、サーバーアドレス、本番環境ファイルをコミットしないでください。

本番設定は `/etc/cname-flattening/huawei.env` などのサーバー側環境ファイルに置きます。このリポジトリでは `.env`、`*.env`、`*.key`、`*.pem`、`id_rsa`、ログ、Python キャッシュ、仮想環境を git から除外しています。

古いサンプルスクリプト内の認証情報は、アスタリスクでマスクされたプレースホルダーであり、使用可能な秘密情報ではありません。これらの旧サンプルを実行する場合は、ローカルで自分の設定に置き換えてください。

## 互換性

このスクリプトは Tencent Cloud CDN、Tencent EdgeOne、Huawei Cloud CDN、China Telecom CDN、Alibaba Cloud CDN/DCDN 型の CNAME ターゲットで使用されています。CNAME 応答が安定しており DoH/ECS プローブと互換性があれば、他の CDN ベンダーでも利用できる可能性があります。

## 元のガイド

- DNSPod: [使用 DNSPod 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230108.html)
- Huawei Cloud DNS: [使用华为云 DNS 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230109.html)

## 図

下の図は DNSPod Python 版のフローです。他のプロバイダーも同様の流れです。

![DNSPod CNAME flattening flow](https://github.com/KincaidYang/CNAMEFlattening/blob/main/static/DNSPodFlattening.png)

## ライセンス

上流リポジトリには明示的なライセンスファイルが含まれていません。コードベース全体のライセンス条件を確認してから、必要に応じてライセンスを追加してください。
