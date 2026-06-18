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

CNAMEFlattening 用于把 CDN CNAME 的按线路解析结果同步为 DNS A/AAAA 记录。适合需要在线路解析里使用拉平记录、而不是直接配置 CNAME 的权威 DNS 场景。

## 功能

- 提供 DNSPod、华为云 DNS、阿里云 DNS 的 Python 和 Go 实现。
- `deploy/huawei_flatten.py` 是当前维护的华为云 DNS 部署版。
- 使用 DoH 与 ECS 子网提示查询 CDN 调度结果，并按线路更新 A/AAAA 记录。
- 华为云 API 限频时自动等待重试。
- DoH 超时、DNS 解析失败、502 等临时错误自动重试。
- 适合 cron 部署，包装脚本使用 `flock` 防止并发执行。
- 支持缺失记录自动创建和 TTL 配置。

## 仓库结构

```text
deploy/                华为云 DNS 生产部署脚本与部署文档
python/                DNSPod、华为云、阿里云的历史 Python 脚本
go/                    DNSPod 和华为云的 Go 实现
static/                流程图和仓库展示资源
```

## 华为云部署

当前维护的部署说明见 [deploy/README.md](deploy/README.md)。

典型运行路径：

```text
/opt/CNAMEFlattening/
/usr/local/bin/huawei-cname-flatten
/etc/cname-flattening/huawei.env
/var/log/cname-flattening/huawei.log
```

cron 示例：

```cron
*/5 * * * * root /usr/bin/flock -n /var/run/cname-flattening-huawei.lock /usr/local/bin/huawei-cname-flatten >> /var/log/cname-flattening/huawei.log 2>&1
```

成功执行通常以这些日志结束：

```text
done changed=<n> skipped=<n> errors=0
elapsed=<seconds>s
```

## 配置安全

不要提交真实 DNS 服务商凭据、云厂商 Access Key、API Token、私钥、服务器地址或生产环境文件。

生产配置应放在服务器侧环境文件中，例如 `/etc/cname-flattening/huawei.env`。仓库已忽略 `.env`、`*.env`、`*.key`、`*.pem`、`id_rsa`、日志、Python 缓存和虚拟环境。

旧示例脚本中的凭据是带星号的占位示例，不是可用密钥。运行这些历史示例前，请在本地替换为自己的配置。

## 兼容性

脚本已用于腾讯云 CDN、腾讯云 EdgeOne、华为云 CDN、天翼云 CDN、阿里云 CDN/DCDN 类型的 CNAME 场景。其他 CDN 厂商只要 CNAME 响应稳定且兼容 DoH/ECS 探测，也可自行测试。

## 原始教程

- DNSPod：[使用 DNSPod 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230108.html)
- 华为云 DNS：[使用华为云 DNS 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230109.html)

## 流程图

下图是 DNSPod Python 版本流程，其他厂商流程类似。

![DNSPod CNAME 拉平流程](https://github.com/KincaidYang/CNAMEFlattening/blob/main/static/DNSPodFlattening.png)

## 许可证

上游仓库未包含明确许可证文件。只有在确认完整代码库授权条款后，才应补充许可证。
