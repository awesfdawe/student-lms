#!/bin/bash

set -e

cat << 'EOF' > backend/.env
DIRECTUS_URL=http://localhost:8055
DIRECTUS_ADMIN_EMAIL=admin@example.com
DIRECTUS_ADMIN_PASSWORD=adminpassword
REDIS_URL=redis://127.0.0.1:6379
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_USER=directus
POSTGRES_PASSWORD=directus_password
POSTGRES_DB=student_lms
SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://directus:directus_password@127.0.0.1:5433/student_lms
WEBHOOK_SECRET=dev_secret_key
EOF

set -a
. backend/.env
set +a

until $(curl --output /dev/null --silent --head --fail "$DIRECTUS_URL/server/ping"); do
    sleep 5
done

docker compose exec -T directus npx directus schema apply ./directus-schema.yaml --yes

cd backend
uv run alembic stamp head
uv run python seed.py
uv run python seed_assets.py
cd ..

get_token() {
    curl -s -X POST "$DIRECTUS_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"$DIRECTUS_ADMIN_EMAIL\",\"password\":\"$DIRECTUS_ADMIN_PASSWORD\"}" \
        | jq -r '.data.access_token'
}

TOKEN=$(get_token)
if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "Failed to obtain token"
    exit 1
fi

create_permission() {
    POLICY_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
        "$DIRECTUS_URL/policies?filter[name][_eq]=Public" | jq -r '.data[0].id // empty')

    if [ -z "$POLICY_ID" ] || [ "$POLICY_ID" == "null" ]; then
        POLICY_ID=$(curl -s -X POST "$DIRECTUS_URL/policies" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d '{"name": "Public", "icon": "public", "description": "Default public policy", "app_access": false, "admin_access": false}' | jq -r '.data.id')
    fi

    if [ -z "$POLICY_ID" ] || [ "$POLICY_ID" == "null" ]; then
        exit 1
    fi

    CURRENT_POLICIES=$(curl -s -H "Authorization: Bearer $TOKEN" "$DIRECTUS_URL/settings" | jq -c '.data.public_policies // []')
    NEW_POLICIES=$(echo "$CURRENT_POLICIES" | jq -c --arg id "$POLICY_ID" '(. + [$id]) | unique')

    curl -s -X PATCH "$DIRECTUS_URL/settings" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "{\"public_policies\": $NEW_POLICIES}" > /dev/null

    PERM_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
        "$DIRECTUS_URL/permissions?filter[policy][_eq]=$POLICY_ID&filter[collection][_eq]=directus_files&filter[action][_eq]=read" | jq -r '.data[0].id // empty')

    if [ -z "$PERM_ID" ] || [ "$PERM_ID" == "null" ]; then
        curl -s -X POST "$DIRECTUS_URL/permissions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d "{\"policy\": \"$POLICY_ID\", \"collection\": \"directus_files\", \"action\": \"read\", \"fields\": [\"*\"]}" > /dev/null
    fi
}

create_flow() {
    local NAME=$1
    local ICON=$2
    local COLOR=$3
    local COLLECTIONS_JSON=$4

    EXISTING=$(curl -s -H "Authorization: Bearer $TOKEN" \
        "$DIRECTUS_URL/flows?filter[name][_eq]=$NAME" | jq -r '.data[0].id // empty')
    
    if [ -n "$EXISTING" ] && [ "$EXISTING" != "null" ]; then
        return
    fi

    FLOW_PAYLOAD=$(jq -n \
        --arg name "$NAME" \
        --arg icon "$ICON" \
        --arg color "$COLOR" \
        --argjson collections "$COLLECTIONS_JSON" \
        '{name: $name, icon: $icon, color: $color, trigger: "event", status: "active", options: {type: "action", scope: ["items.create","items.update","items.delete"], collections: $collections}}')
    
    FLOW_ID=$(curl -s -X POST "$DIRECTUS_URL/flows" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "$FLOW_PAYLOAD" | jq -r '.data.id')

    OP_PAYLOAD=$(jq -n \
        --arg flow_id "$FLOW_ID" \
        '{name: "Call Webhook", key: "call_webhook", type: "webhook", position_x: 1, position_y: 1, flow: $flow_id, options: {method: "POST", url: "http://host.docker.internal:8000/api/webhooks/directus_update", payload: "{\"collection\": \"{{$trigger.collection}}\", \"event\": \"{{$trigger.event}}\", \"payload\": {}}"}}')
    
    curl -s -X POST "$DIRECTUS_URL/operations" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "$OP_PAYLOAD" > /dev/null
}

create_permission

create_flow "Sync Users" "sync" "#2196F3" '["users"]'
create_flow "Invalidate File Cache" "cached" "#FFC107" '["directus_files"]'
create_flow "FastAPI Cache Invalidation" "bolt" "#6644FF" '["landing_page","globals","ui_dictionary","pages","courses","faqs","quiz"]'

echo "Done."
