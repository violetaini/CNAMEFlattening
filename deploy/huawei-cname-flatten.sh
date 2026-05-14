#!/usr/bin/env bash
set -euo pipefail

cd /opt/CNAMEFlattening
set -a
# shellcheck disable=SC1091
. /etc/cname-flattening/huawei.env
set +a

exec /opt/CNAMEFlattening/.venv/bin/python /opt/CNAMEFlattening/deploy/huawei_flatten.py "$@"
