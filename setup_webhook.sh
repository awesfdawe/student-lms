#!/bin/bash

TOKEN=$(curl -s -X POST http://localhost:8055/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"adminpassword"}' | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('access_token', ''))")

if [ -z "$TOKEN" ]; then
    echo "Ошибка авторизации в Directus. Убедитесь, что контейнер запущен."
    exit 1
fi

FLOW_RESPONSE=$(curl -s -X POST http://localhost:8055/flows \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "name": "FastAPI Cache Invalidation",
    "icon": "bolt",
    "color": "#6644FF",
    "trigger": "event",
    "status": "active",
    "options": {
      "type": "action",
      "scope": ["items.create", "items.update", "items.delete"],
      "collections": ["landing_page", "globals", "ui_dictionary", "pages", "courses", "faqs", "quiz"]
    }
  }')

FLOW_ID=$(echo $FLOW_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('id', ''))")

curl -s -X POST http://localhost:8055/operations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "name": "Clear SSR Cache",
    "key": "clear_cache_req",
    "type": "request",
    "position_x": 0,
    "position_y": 0,
    "flow": "'"${FLOW_ID}"'",
    "options": {
      "method": "POST",
      "url": "http://host.docker.internal:8000/api/webhooks/directus_update",
      "headers": [
        {
          "header": "Content-Type",
          "value": "application/json"
        }
      ],
      "body": "{\"collection\": \"{{$trigger.collection}}\", \"event\": \"{{$trigger.event}}\", \"payload\": {}}"
    }
  }' > /dev/null

echo "✅ Универсальный вебхук успешно настроен!"
