#!/usr/bin/env bash
# Example curl requests for the API

echo "Health check"
curl -s http://127.0.0.1:8000/health | jq

echo "\nCreate a quick note via chat"
curl -s -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{"message":"Save note: Buy milk tomorrow"}' | jq

echo "\nAdd a task via chat"
curl -s -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{"message":"Remind me to finish the report tomorrow"}' | jq
