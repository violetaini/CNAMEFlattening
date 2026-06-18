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

CNAMEFlattening synchronizes CDN CNAME resolution results into DNS A/AAAA records. It is designed for line-aware DNS providers and CDN scenarios where the authoritative DNS zone needs flattened records instead of a CNAME.

## Features

- Python and Go implementations for DNSPod, Huawei Cloud DNS, and Alibaba Cloud DNS.
- Production Huawei Cloud DNS runner in `deploy/huawei_flatten.py`.
- Line-aware A and AAAA updates using CDN answers queried with DoH and ECS subnet hints.
- Automatic retry for Huawei Cloud API rate limits.
- Automatic retry for transient DoH failures such as timeouts, DNS resolution failures, and 502 responses.
- Cron-friendly wrapper with `flock` to prevent concurrent runs.
- Optional missing-record creation and configurable TTL.

## Repository Layout

```text
deploy/                Production Huawei Cloud DNS runner and deployment docs
python/                Historical Python scripts for DNSPod, Huawei Cloud, and Alibaba Cloud
go/                    Go implementations for DNSPod and Huawei Cloud
static/                Diagrams and repository assets
```

## Huawei Cloud Deployment

The maintained deployment path is documented in [deploy/README.md](deploy/README.md).

Typical runtime layout:

```text
/opt/CNAMEFlattening/
/usr/local/bin/huawei-cname-flatten
/etc/cname-flattening/huawei.env
/var/log/cname-flattening/huawei.log
```

Cron entry:

```cron
*/5 * * * * root /usr/bin/flock -n /var/run/cname-flattening-huawei.lock /usr/local/bin/huawei-cname-flatten >> /var/log/cname-flattening/huawei.log 2>&1
```

Expected successful ending:

```text
done changed=<n> skipped=<n> errors=0
elapsed=<seconds>s
```

## Configuration Safety

Do not commit real DNS provider credentials, cloud access keys, API tokens, private keys, server addresses, or production environment files.

Use environment files on the server side, for example `/etc/cname-flattening/huawei.env`, and keep `.env`, `*.env`, `*.key`, `*.pem`, `id_rsa`, logs, Python caches, and virtual environments ignored by git.

The checked-in credentials in old example scripts are masked placeholders and are not usable secrets. Replace them locally before running those historical examples.

## Compatibility

The scripts have been used with Tencent Cloud CDN, Tencent EdgeOne, Huawei Cloud CDN, China Telecom CDN, and Alibaba Cloud CDN/DCDN style CNAME targets. Other CDN vendors may work if their CNAME answers are stable and compatible with DoH/ECS probing.

## Original Guides

- DNSPod: [使用 DNSPod 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230108.html)
- Huawei Cloud DNS: [使用华为云 DNS 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230109.html)

## Diagram

The diagram below shows the DNSPod Python flow. Other providers follow the same general process.

![DNSPod CNAME flattening flow](https://github.com/KincaidYang/CNAMEFlattening/blob/main/static/DNSPodFlattening.png)

## License

No explicit license file is included in the upstream repository. Add a license only after confirming the intended terms for the full codebase.
