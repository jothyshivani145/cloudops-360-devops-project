#!/usr/bin/env bash
set -euo pipefail

echo "Running CloudOps 360 health-check tests..."

bash -n scripts/health_check.sh
echo "PASS: Bash syntax validation"

echo "Testing an unavailable application..."

if ./scripts/health_check.sh http://127.0.0.1:59999; then
    echo "FAIL: Unavailable service was marked healthy"
    exit 1
else
    echo "PASS: Unavailable service detected"
fi

echo "All tests passed!"
