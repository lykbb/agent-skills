#!/usr/bin/env bash
# 整合版只读预检适配器，不执行旧脚本中的项目代码或写日志。
set -eu
MODULE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$MODULE_ROOT/../../scripts/check_project.py" "$@"
