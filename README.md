# CNAMEFlattening

用于把 CDN CNAME 按线路解析结果同步为 DNS A/AAAA 记录。仓库包含 Python 和 Go 两类实现，并提供一个面向华为云 DNS 的可部署脚本。

## 版本说明
本脚本支持 Python 和 Go 两种版本，其中 Python 版本支持华为云 DNS、阿里云 DNS 和 DNSPod，Go 版本支持 DNSPod、华为云。

`deploy/huawei_flatten.py` 是当前线上使用的华为云 DNS 部署版，支持：

- 按华为云线路 ID 更新 A / AAAA 记录
- 使用 DoH 和 ECS 子网查询 CDN 调度结果
- 华为云限频自动等待重试
- DoH 超时、DNS 解析失败、502 等临时错误自动重试
- cron + flock 防止并发执行
- 缺失线路记录自动创建，默认 TTL 为 1

## 相关说明
本脚本用以拉平 CNAME 记录，当前仅支持 DNSPod、华为云DNS、阿里云 DNS。

DNSPod DNSPod DNS

HuaweiCloud 华为云 DNS

Aliyun 阿里云 DNS

请根据实际需要选择对应的脚本使用。

注意：本脚本仅测试了与腾讯云 CDN、腾讯云 EdgeOne、华为云 CDN、天翼云 CDN、阿里云 CDN 的兼容性，其他 CDN 厂商未测试兼容性，若有其他厂商需求请自行测试或提交Issue。
## 使用教程
该教程为 Python 版本，此处未列厂商说明可查看对于厂商文件夹下的 README.MD

DNSPod：[使用 DNSPod 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230108.html)

华为云DNS：[使用华为云 DNS 拉平 CNAME 记录（CDN 场景）](https://r2wind.cn/articles/20230109.html)

部署版说明见 [deploy/README.md](deploy/README.md)。

## 脚本示意
该示意为 DNSPod Python版本，其他厂商和版本流程类似。

![流程图](https://github.com/KincaidYang/CNAMEFlattening/blob/main/static/DNSPodFlattening.png)
