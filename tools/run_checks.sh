#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOCALES_DIR="${1:-${LOCALES_DIR:-${REPO_ROOT}/locales}}"
REPORT_DIR="${REPO_ROOT}/reports"
REPORT_FILE="${REPORT_DIR}/locale-report.txt"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: Python is required, but neither python3 nor python was found on PATH." >&2
  exit 127
fi

SOURCE_FILE="${LOCALES_DIR}/en.json"
if [[ ! -f "${SOURCE_FILE}" ]]; then
  echo "Error: English source file not found at ${SOURCE_FILE}" >&2
  exit 1
fi

mkdir -p "${REPORT_DIR}"

KEY_COUNT="$("${PYTHON_BIN}" -c 'import json, sys; print(len(json.load(open(sys.argv[1], encoding="utf-8"))))' "${SOURCE_FILE}")"
LOCALE_COUNT="$(find "${LOCALES_DIR}" -maxdepth 1 -type f -name "*.json" ! -name "en.json" | wc -l | tr -d " ")"

echo "English source keys: ${KEY_COUNT}"
echo "Locale files found: ${LOCALE_COUNT}"
echo "Locale report: ${REPORT_FILE}"

set +e
"${PYTHON_BIN}" "${REPO_ROOT}/tools/check_locales.py" --locales-dir "${LOCALES_DIR}" | tee "${REPORT_FILE}"
VALIDATOR_EXIT=${PIPESTATUS[0]}
set -e

exit "${VALIDATOR_EXIT}"
