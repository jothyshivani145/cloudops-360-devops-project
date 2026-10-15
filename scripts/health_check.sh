
#!/usr/bin/env bash

# CloudOps 360 - Application Health Check

URL="${1:-http://127.0.0.1:8080}"

echo "Checking application: $URL"

HTTP_CODE=$(curl -L -sS --max-time 5 -o /dev/null -w "%{http_code}" "$URL")
CURL_STATUS=$?

if [ "$CURL_STATUS" -ne 0 ]; then
    echo "UNHEALTHY: Could not connect to the application"
    exit 1
elif [[ "$HTTP_CODE" =~ ^2[0-9][0-9]$ ]]; then
    echo "HEALTHY: Application responded with HTTP $HTTP_CODE"
    exit 0
else
    echo "UNHEALTHY: Application responded with HTTP $HTTP_CODE"
    exit 1
fi
