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

CNAMEFlattening 用於把 CDN CNAME 的分線路解析結果同步為 DNS A/AAAA 記錄。適合需要在線路解析中使用拉平記錄，而不是直接設定 CNAME 的權威 DNS 場景。

## 功能

- 提供 DNSPod、華為雲 DNS、阿里雲 DNS 的 Python 與 Go 實作。
- `deploy/huawei_flatten.py` 是目前維護的華為雲 DNS 部署版。
- 使用 DoH 與 ECS 子網提示查詢 CDN 調度結果，並依線路更新 A/AAAA 記錄。
- 華為雲 API 限頻時自動等待重試。
- DoH 逾時、DNS 解析失敗、502 等暫時性錯誤自動重試。
- 適合 cron 部署，包裝腳本使用 `flock` 防止並行執行。
- 支援缺失記錄自動建立與 TTL 設定。

## 倉庫結構

```text
deploy/                華為雲 DNS 生產部署腳本與部署文件
python/                DNSPod、華為雲、阿里雲的歷史 Python 腳本
go/                    DNSPod 與華為雲的 Go 實作
static/                流程圖與倉庫展示資源
```

## 華為雲部署

目前維護的部署說明見 [deploy/README.md](deploy/README.md)。

典型執行路徑：

```text
/opt/CNAMEFlattening/
/usr/local/bin/huawei-cname-flatten
/etc/cname-flattening/huawei.env
/var/log/cname-flattening/huawei.log
```

cron 範例：

```cron
*/5 * * * * root /usr/bin/flock -n /var/run/cname-flattening-huawei.lock /usr/local/bin/huawei-cname-flatten >> /var/log/cname-flattening/huawei.log 2>&1
```

成功執行通常以這些日誌結束：

```text
done changed=<n> skipped=<n> errors=0
elapsed=<seconds>s
```

## 設定安全

不要提交真實 DNS 服務商憑據、雲廠商 Access Key、API Token、私鑰、伺服器位址或生產環境檔案。

生產設定應放在伺服器側環境檔案中，例如 `/etc/cname-flattening/huawei.env`。倉庫已忽略 `.env`、`*.env`、`*.key`、`*.pem`、`id_rsa`、日誌、Python 快取與虛擬環境。

舊範例腳本中的憑據是帶星號的占位範例，不是可用密鑰。執行這些歷史範例前，請在本機替換為自己的設定。

## 相容性

腳本已用於騰訊雲 CDN、騰訊雲 EdgeOne、華為雲 CDN、天翼雲 CDN、阿里雲 CDN/DCDN 類型的 CNAME 場景。其他 CDN 廠商只要 CNAME 回應穩定且相容 DoH/ECS 探測，也可自行測試。

## 原始教學

- DNSPod：[使用 DNSPod 拉平 CNAME 記錄（CDN 場景）](https://r2wind.cn/articles/20230108.html)
- 華為雲 DNS：[使用華為雲 DNS 拉平 CNAME 記錄（CDN 場景）](https://r2wind.cn/articles/20230109.html)

## 流程圖

下圖是 DNSPod Python 版本流程，其他廠商流程類似。

![DNSPod CNAME 拉平流程](https://github.com/KincaidYang/CNAMEFlattening/blob/main/static/DNSPodFlattening.png)

## 授權

上游倉庫未包含明確授權文件。只有在確認完整程式碼庫授權條款後，才應補充授權文件。
