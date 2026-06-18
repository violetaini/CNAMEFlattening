# Huawei Cloud deployment

This directory contains the production-oriented Huawei Cloud DNS flattening runner.

## Files

- `huawei_flatten.py`: queries CDN CNAME answers through DoH with ECS subnet hints, then updates Huawei Cloud DNS line records.
- `huawei-cname-flatten.sh`: wrapper used by cron on Linux hosts.

## Runtime layout

The current production deployment uses this layout:

```text
/opt/CNAMEFlattening/
  .venv/
  deploy/huawei_flatten.py
/usr/local/bin/huawei-cname-flatten
/etc/cname-flattening/huawei.env
/var/log/cname-flattening/huawei.log
```

Cron entry:

```cron
*/5 * * * * root /usr/bin/flock -n /var/run/cname-flattening-huawei.lock /usr/local/bin/huawei-cname-flatten >> /var/log/cname-flattening/huawei.log 2>&1
```

The deployment wrapper sources `/etc/cname-flattening/huawei.env` and then runs the Python script from the virtual environment.

## Environment

Required:

```bash
HUAWEICLOUD_SDK_AK=...
HUAWEICLOUD_SDK_SK=...
HUAWEICLOUD_REGION=cn-north-4
FLATTEN_DOMAIN=example.com
FLATTEN_CNAME=target.example.net.
```

Common options:

```bash
FLATTEN_SUBDOMAIN=@
FLATTEN_RECORD_TYPES=A,AAAA
FLATTEN_LINES=all
FLATTEN_TTL=1
FLATTEN_CREATE_MISSING=1
FLATTEN_DRY_RUN=0
FLATTEN_DOH_URL=https://doh.pub/dns-query
FLATTEN_DOH_RETRIES=3
FLATTEN_DOH_TIMEOUT=20
FLATTEN_DOH_RETRY_DELAY=2
FLATTEN_HUAWEICLOUD_RETRIES=4
FLATTEN_HUAWEICLOUD_RATE_LIMIT_SLEEP=65
FLATTEN_HUAWEICLOUD_WRITE_DELAY=0.75
```

`FLATTEN_LINES=all` uses deployable Huawei Cloud line IDs only. Use `FLATTEN_INCLUDE_UNSUPPORTED_LINES=1` only when intentionally testing unsupported or custom line IDs.

## Install

```bash
apt-get update
apt-get install -y python3-venv python3-pip
cd /opt/CNAMEFlattening
python3 -m venv .venv
.venv/bin/pip install requests huaweicloudsdkdns huaweicloudsdkcore
install -m 755 deploy/huawei-cname-flatten.sh /usr/local/bin/huawei-cname-flatten
install -d -m 755 /etc/cname-flattening /var/log/cname-flattening
touch /var/log/cname-flattening/huawei.log
```

Create `/etc/cname-flattening/huawei.env` with the required environment variables, then add the cron entry above.

## Operations

Check current status:

```bash
systemctl is-active cron
pgrep -af 'huawei_flatten|huawei-cname-flatten|cname-flattening' || true
tail -n 120 /var/log/cname-flattening/huawei.log
```

Expected successful ending:

```text
done changed=<n> skipped=<n> errors=0
elapsed=<seconds>s
```

DoH transient failures are expected occasionally. The runner logs retry attempts like:

```text
doh retry 2/3 A subnet=<ecs-subnet> after 2s reason=<error-type>: <error>
```

If the final `done` line still has `errors=0`, the retry recovered and no manual action is needed.
