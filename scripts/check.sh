#!/usr/bin/env bash
# Run all repository validation checks. Exits non-zero if any check fails.
set -u
cd "$(dirname "$0")/.."
status=0
echo "== Skill format =="
python3 scripts/check_format.py || status=1
echo "== Privacy scan =="
python3 scripts/privacy_scan.py || status=1
echo "== Link integrity =="
python3 scripts/check_links.py || status=1
echo "== Component inventory =="
python3 scripts/check_inventory.py || status=1
if [ "$status" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "CHECKS FAILED"
fi
exit "$status"