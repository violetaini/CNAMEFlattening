#!/usr/bin/env python3
import argparse
import ipaddress
import os
import sys
import time

import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkdns.v2 import (
    CreateRecordSetWithLineRequest,
    CreateRecordSetWithLineRequestBody,
    DnsClient,
    ListPublicZonesRequest,
    ShowRecordSetByZoneRequest,
    UpdateRecordSetsReq,
    UpdateRecordSetsRequest,
)
from huaweicloudsdkdns.v2.region.dns_region import DnsRegion


SHANGHAI_TELECOM_ECS = "202.96.209.133"
HONG_KONG_ECS = "203.80.96.10"
MACAU_ECS = "202.175.3.8"
TAIWAN_ECS = "168.95.1.1"
PENGBOSHI_ECS = "124.207.160.106"


DNS_SERVERS = {
    "Dianxin_Liaoning": "219.148.204.66",
    "Yidong_Liaoning": "211.137.32.178",
    "Liantong_Liaoning": "202.96.64.68",
    "Dianxin_Jilin": "219.149.194.55",
    "Yidong_Jilin": "211.141.16.99",
    "Liantong_Jilin": "202.98.0.68",
    "Dianxin_Heilongjiang": "112.100.100.100",
    "Yidong_Heilongjiang": "211.137.241.34",
    "Liantong_Heilongjiang": "202.97.224.68",
    "Dianxin_Beijing": "219.141.136.10",
    "Yidong_Beijing": "221.130.33.52",
    "Liantong_Beijing": "202.106.196.115",
    "Dianxin_Tianjin": "219.150.32.132",
    "Yidong_Tianjin": "211.137.160.5",
    "Liantong_Tianjin": "202.99.96.68",
    "Dianxin_Hebei": "222.222.222.222",
    "Yidong_Hebei": "211.138.13.66",
    "Liantong_Hebei": "202.99.160.68",
    "Dianxin_Shanxi": "219.149.135.188",
    "Yidong_Shanxi": "211.138.106.3",
    "Liantong_Shanxi": "202.99.216.113",
    "Dianxin_Neimenggu": "219.148.162.31",
    "Yidong_Neimenggu": "211.138.91.1",
    "Liantong_Neimenggu": "202.99.224.68",
    "Dianxin_Hainan": "202.100.192.68",
    "Yidong_Hainan": "221.176.88.95",
    "Liantong_Hainan": "221.11.132.2",
    "Dianxin_Guangdong": "202.96.134.133",
    "Yidong_Guangdong": "211.139.163.6",
    "Liantong_Guangdong": "210.21.196.6",
    "Dianxin_Guangxi": "202.103.225.68",
    "Yidong_Guangxi": "211.138.245.180",
    "Liantong_Guangxi": "221.7.128.68",
    "Dianxin_Fujian": "218.85.152.99",
    "Yidong_Fujian": "211.138.151.161",
    "Liantong_Fujian": "218.104.128.106",
    "Dianxin_Hunan": "222.246.129.80",
    "Yidong_Hunan": "211.142.210.98",
    "Liantong_Hunan": "58.20.127.238",
    "Dianxin_Hubei": "202.103.24.68",
    "Yidong_Hubei": "211.137.58.20",
    "Liantong_Hubei": "218.104.111.114",
    "Dianxin_Henan": "222.85.85.85",
    "Yidong_Henan": "211.138.24.71",
    "Liantong_Henan": "202.102.224.68",
    "Dianxin_Jiangxi": "202.101.224.69",
    "Yidong_Jiangxi": "211.141.90.68",
    "Liantong_Jiangxi": "220.248.192.12",
    "Dianxin_Shanghai": "202.96.209.133",
    "Yidong_Shanghai": "211.136.112.50",
    "Liantong_Shanghai": "210.22.70.3",
    "Dianxin_Jiangsu": "218.2.2.2",
    "Yidong_Jiangsu": "221.131.143.69",
    "Liantong_Jiangsu": "221.6.4.66",
    "Dianxin_Zhejiang": "202.101.172.35",
    "Yidong_Zhejiang": "211.140.13.188",
    "Liantong_Zhejiang": "221.12.1.227",
    "Dianxin_Anhui": "61.132.163.68",
    "Yidong_Anhui": "211.138.180.2",
    "Liantong_Anhui": "218.104.78.2",
    "Dianxin_Shandong": "219.146.1.66",
    "Yidong_Shandong": "218.201.96.130",
    "Liantong_Shandong": "202.102.128.68",
    "Dianxin_Chongqing": "61.128.192.68",
    "Yidong_Chongqing": "218.201.4.3",
    "Liantong_Chongqing": "221.5.203.98",
    "Dianxin_Sichuan": "61.139.2.69",
    "Yidong_Sichuan": "211.137.82.4",
    "Liantong_Sichuan": "119.6.6.6",
    "Dianxin_Guizhou": "202.98.192.67",
    "Yidong_Guizhou": "211.139.5.29",
    "Liantong_Guizhou": "221.13.28.234",
    "Dianxin_Yunnan": "222.172.200.68",
    "Yidong_Yunnan": "211.139.29.68",
    "Liantong_Yunnan": "221.3.131.11",
    "Dianxin_Xizang": "202.98.224.68",
    "Yidong_Xizang": "211.139.73.34",
    "Liantong_Xizang": "221.13.65.34",
    "Dianxin_Shaanxi": "218.30.19.40",
    "Yidong_Shaanxi": "211.137.130.3",
    "Liantong_Shaanxi": "221.11.1.67",
    "Dianxin_Gansu": "202.100.64.68",
    "Yidong_Gansu": "218.203.160.194",
    "Liantong_Gansu": "221.7.34.10",
    "Dianxin_Qinghai": "202.100.128.68",
    "Yidong_Qinghai": "211.138.75.123",
    "Liantong_Qinghai": "221.207.58.58",
    "Dianxin_Ningxia": "222.75.152.129",
    "Yidong_Ningxia": "218.203.123.116",
    "Liantong_Ningxia": "211.93.0.81",
    "Dianxin_Xinjiang": "61.128.114.166",
    "Yidong_Xinjiang": "218.202.152.130",
    "Liantong_Xinjiang": "221.7.1.21",
    "Tietong": "222.44.33.244",
    "Tietong_Liaoning": "61.236.12.27",
    "Tietong_Jilin": "222.34.29.166",
    "Tietong_Heilongjiang": "61.236.93.33",
    "Tietong_Beijing": "61.233.9.61",
    "Tietong_Hebei": "211.98.2.4",
    "Tietong_Shanxi": "61.233.139.2",
    "Tietong_Neimenggu": "222.39.47.53",
    "Tietong_Tianjin": "61.234.95.2",
    "Tietong_Shanghai": "222.44.33.244",
    "Tietong_Jiangsu": "222.45.233.34",
    "Tietong_Zhejiang": "36.192.156.255",
    "Tietong_Anhui": "36.192.157.0",
    "Tietong_Fujian": "222.47.29.93",
    "Tietong_Jiangxi": "61.235.0.228",
    "Tietong_Shandong": "61.233.154.33",
    "Tietong_Henan": "211.98.192.3",
    "Tietong_Hubei": "61.232.206.103",
    "Tietong_Hunan": "61.234.254.6",
    "Tietong_Guangdong": "61.235.70.252",
    "Tietong_Guangxi": "222.52.118.163",
    "Tietong_Hainan": "222.61.0.98",
    "Tietong_Chongqing": "211.98.112.168",
    "Tietong_Sichuan": "61.236.159.99",
    "Tietong_Guizhou": "61.236.192.206",
    "Tietong_Yunnan": "211.98.72.8",
    "Tietong_Xizang": "222.62.3.255",
    "Tietong_Shaanxi": "61.232.202.158",
    "Tietong_Gansu": "211.98.121.27",
    "Tietong_Qinghai": "36.193.126.0",
    "Tietong_Ningxia": "222.58.108.8",
    "Tietong_Xinjiang": "211.98.127.101",
    "Pengboshi": PENGBOSHI_ECS,
    "Pengboshi_Liaoning": PENGBOSHI_ECS,
    "Pengboshi_Jilin": PENGBOSHI_ECS,
    "Pengboshi_Heilongjiang": PENGBOSHI_ECS,
    "Pengboshi_Beijing": PENGBOSHI_ECS,
    "Pengboshi_Hebei": PENGBOSHI_ECS,
    "Pengboshi_Shanxi": PENGBOSHI_ECS,
    "Pengboshi_Neimenggu": PENGBOSHI_ECS,
    "Pengboshi_Tianjin": PENGBOSHI_ECS,
    "Pengboshi_Shanghai": PENGBOSHI_ECS,
    "Pengboshi_Jiangsu": PENGBOSHI_ECS,
    "Pengboshi_Zhejiang": PENGBOSHI_ECS,
    "Pengboshi_Anhui": PENGBOSHI_ECS,
    "Pengboshi_Fujian": PENGBOSHI_ECS,
    "Pengboshi_Jiangxi": PENGBOSHI_ECS,
    "Pengboshi_Shandong": PENGBOSHI_ECS,
    "Pengboshi_Henan": PENGBOSHI_ECS,
    "Pengboshi_Hubei": PENGBOSHI_ECS,
    "Pengboshi_Hunan": PENGBOSHI_ECS,
    "Pengboshi_Guangdong": PENGBOSHI_ECS,
    "Pengboshi_Guangxi": PENGBOSHI_ECS,
    "Pengboshi_Hainan": PENGBOSHI_ECS,
    "Pengboshi_Chongqing": PENGBOSHI_ECS,
    "Pengboshi_Sichuan": PENGBOSHI_ECS,
    "Pengboshi_Guizhou": PENGBOSHI_ECS,
    "Pengboshi_Yunnan": PENGBOSHI_ECS,
    "Pengboshi_Xizang": PENGBOSHI_ECS,
    "Pengboshi_Shaanxi": PENGBOSHI_ECS,
    "Pengboshi_Gansu": PENGBOSHI_ECS,
    "Pengboshi_Qinghai": PENGBOSHI_ECS,
    "Pengboshi_Ningxia": PENGBOSHI_ECS,
    "Pengboshi_Xinjiang": PENGBOSHI_ECS,
    "Jiaoyuwang": "202.112.144.30",
    "CN": SHANGHAI_TELECOM_ECS,
    "Abroad": HONG_KONG_ECS,
    "HK": HONG_KONG_ECS,
    "MO": MACAU_ECS,
    "TW": TAIWAN_ECS,
    "default_view": SHANGHAI_TELECOM_ECS,
}

# Huawei documents provincial Tietong line IDs, but this zone's current DNS
# bundle rejects them with DNS.0806. Keep the IPs for upgraded bundles, while
# FLATTEN_LINES=all uses only deployable lines.
UNSUPPORTED_DEFAULT_LINES = {
    line_id for line_id in DNS_SERVERS if line_id.startswith("Tietong_")
}


def env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value


def int_env(name, default):
    return int(env(name, str(default)))


def float_env(name, default):
    return float(env(name, str(default)))


def truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def fqdn(domain, subdomain):
    subdomain = "" if subdomain in {"", "@"} else subdomain.rstrip(".") + "."
    return f"{subdomain}{domain.rstrip('.')}."


def wanted_lines():
    raw = env("FLATTEN_LINES", "all").strip()
    if raw.lower() == "all":
        if truthy(env("FLATTEN_INCLUDE_UNSUPPORTED_LINES", "0")):
            return list(DNS_SERVERS.items())
        return [
            (line_id, subnet)
            for line_id, subnet in DNS_SERVERS.items()
            if line_id not in UNSUPPORTED_DEFAULT_LINES
        ]
    lines = []
    for item in raw.split(","):
        line_id = item.strip()
        if not line_id:
            continue
        if line_id not in DNS_SERVERS:
            raise RuntimeError(f"unknown line id in FLATTEN_LINES: {line_id}")
        lines.append((line_id, DNS_SERVERS[line_id]))
    return lines


def wanted_record_types():
    raw = env("FLATTEN_RECORD_TYPES", "A")
    values = [item.strip().upper() for item in raw.split(",") if item.strip()]
    invalid = [item for item in values if item not in {"A", "AAAA"}]
    if invalid:
        raise RuntimeError(f"unsupported FLATTEN_RECORD_TYPES values: {', '.join(invalid)}")
    return values


def huawei_rate_limited(exc):
    return (
        getattr(exc, "status_code", None) == 429
        or getattr(exc, "error_code", None) == "APIGW.0308"
    )


def huawei_request(action, description, write=False):
    attempts = int_env("FLATTEN_HUAWEICLOUD_RETRIES", 4)
    sleep_seconds = float_env("FLATTEN_HUAWEICLOUD_RATE_LIMIT_SLEEP", 65)
    write_delay = float_env("FLATTEN_HUAWEICLOUD_WRITE_DELAY", 0.75)
    for attempt in range(1, attempts + 1):
        if write and write_delay > 0:
            time.sleep(write_delay)
        try:
            return action()
        except exceptions.ClientRequestException as exc:
            if huawei_rate_limited(exc) and attempt < attempts:
                print(
                    f"huaweicloud throttled {description}; "
                    f"sleep {sleep_seconds:.0f}s retry {attempt + 1}/{attempts}"
                )
                time.sleep(sleep_seconds)
                continue
            raise


def build_client():
    credentials = BasicCredentials(
        env("HUAWEICLOUD_AK", required=True),
        env("HUAWEICLOUD_SK", required=True),
        env("HUAWEICLOUD_PROJECT_ID", required=True),
    )
    return (
        DnsClient.new_builder()
        .with_credentials(credentials)
        .with_region(DnsRegion.value_of(env("HUAWEICLOUD_REGION", "cn-north-4")))
        .build()
    )


def zone_id(client, domain):
    request = ListPublicZonesRequest()
    request.type = "public"
    request.name = domain.rstrip(".")
    response = huawei_request(lambda: client.list_public_zones(request), "list zones")
    zones = getattr(response, "zones", None) or []
    if not zones:
        raise RuntimeError(f"no public zone found for {domain}")
    return zones[0].id


def ip_version(record_type):
    return 4 if record_type == "A" else 6


def fetch_ips(doh_url, cname, record_type, subnet):
    attempts = int_env("FLATTEN_DOH_RETRIES", 3)
    timeout = float_env("FLATTEN_DOH_TIMEOUT", 20)
    retry_delay = float_env("FLATTEN_DOH_RETRY_DELAY", 2)
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                doh_url,
                params={"name": cname, "type": record_type, "edns_client_subnet": subnet},
                headers={"Accept": "application/dns-json"},
                timeout=timeout,
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("Status") != 0:
                raise RuntimeError(f"DoH status {payload.get('Status')} for {cname} {record_type}")
            values = []
            for answer in payload.get("Answer", []):
                data = str(answer.get("data", "")).rstrip(".")
                try:
                    parsed = ipaddress.ip_address(data)
                except ValueError:
                    continue
                if parsed.version == ip_version(record_type) and data not in values:
                    values.append(data)
            if not values:
                raise RuntimeError(f"no {record_type} address in DoH answer for {cname}")
            return values
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            if attempt >= attempts:
                raise
            print(
                f"doh retry {attempt + 1}/{attempts} "
                f"{record_type} subnet={subnet} after {retry_delay:.0f}s "
                f"reason={type(exc).__name__}: {exc}"
            )
            time.sleep(retry_delay)


def recordsets_by_line(client, zone, record_type, name):
    request = ShowRecordSetByZoneRequest()
    request.zone_id = zone
    request.status = "ACTIVE"
    request.type = record_type
    request.name = name
    request.limit = 500
    response = huawei_request(
        lambda: client.show_record_set_by_zone(request),
        f"list {record_type} recordsets",
    )
    recordsets = getattr(response, "recordsets", None) or []
    by_line = {}
    for recordset in recordsets:
        if (
            getattr(recordset, "name", None) == name
            and getattr(recordset, "type", None) == record_type
        ):
            by_line[getattr(recordset, "line", None)] = recordset
    return by_line


def create_recordset(client, zone, line_id, record_type, name, ttl, records):
    request = CreateRecordSetWithLineRequest()
    request.zone_id = zone
    request.body = CreateRecordSetWithLineRequestBody(
        name=name,
        type=record_type,
        ttl=ttl,
        records=records,
        line=line_id,
    )
    return huawei_request(
        lambda: client.create_record_set_with_line(request),
        f"create {record_type} {line_id}",
        write=True,
    )


def update_recordset(client, zone, recordset_id, record_type, name, ttl, records):
    request = UpdateRecordSetsRequest()
    request.zone_id = zone
    request.recordset_id = recordset_id
    request.body = UpdateRecordSetsReq(
        name=name,
        type=record_type,
        ttl=ttl,
        records=records,
    )
    return huawei_request(
        lambda: client.update_record_sets(request),
        f"update {record_type} {recordset_id}",
        write=True,
    )


def recordset_records(recordset):
    return list(getattr(recordset, "records", None) or [])


def recordset_ttl(recordset):
    return int(getattr(recordset, "ttl", 0) or 0)


def recordset_id(recordset):
    return getattr(recordset, "id", None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dry_run = args.dry_run or truthy(env("FLATTEN_DRY_RUN", "0"))
    create_missing = truthy(env("FLATTEN_CREATE_MISSING", "1"))
    domain = env("FLATTEN_DOMAIN", required=True)
    name = fqdn(domain, env("FLATTEN_SUBDOMAIN", "@"))
    cname = env("FLATTEN_CNAME", required=True)
    ttl = int(env("FLATTEN_TTL", "1"))
    doh_url = env("FLATTEN_DOH_URL", "https://doh.pub/dns-query")
    lines = wanted_lines()
    record_types = wanted_record_types()

    print(
        f"start domain={domain} name={name} cname={cname} "
        f"types={','.join(record_types)} doh={doh_url} lines={len(lines)} dry_run={dry_run}"
    )

    client = build_client()
    zone = zone_id(client, domain)
    errors = 0
    changed = 0
    skipped = 0

    for record_type in record_types:
        try:
            existing_by_line = recordsets_by_line(client, zone, record_type, name)
        except exceptions.ClientRequestException as exc:
            errors += 1
            print(
                f"huaweicloud error list {record_type}: "
                f"{exc.status_code} {exc.error_code} {exc.error_msg}"
            )
            continue

        for line_id, subnet in lines:
            try:
                records = fetch_ips(doh_url, cname, record_type, subnet)
                recordset = existing_by_line.get(line_id)
                if recordset is None:
                    if not create_missing:
                        print(f"missing {record_type} {line_id}; create_missing disabled")
                        skipped += 1
                        continue
                    print(f"create {record_type} {line_id} -> {','.join(records)}")
                    if not dry_run:
                        create_recordset(client, zone, line_id, record_type, name, ttl, records)
                    changed += 1
                    continue

                current_records = recordset_records(recordset)
                if sorted(current_records) == sorted(records) and recordset_ttl(recordset) == ttl:
                    print(f"skip {record_type} {line_id}; unchanged")
                    skipped += 1
                    continue

                print(
                    f"update {record_type} {line_id} "
                    f"{','.join(current_records)} -> {','.join(records)}"
                )
                if not dry_run:
                    update_recordset(
                        client,
                        zone,
                        recordset_id(recordset),
                        record_type,
                        name,
                        ttl,
                        records,
                    )
                changed += 1
            except exceptions.ClientRequestException as exc:
                errors += 1
                print(
                    f"huaweicloud error {record_type} {line_id}: "
                    f"{exc.status_code} {exc.error_code} {exc.error_msg}"
                )
            except Exception as exc:
                errors += 1
                print(f"error {record_type} {line_id}: {exc}")

    print(f"done changed={changed} skipped={skipped} errors={errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    started = time.time()
    code = main()
    print(f"elapsed={time.time() - started:.1f}s")
    sys.exit(code)
