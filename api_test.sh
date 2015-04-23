#!/bin/bash

# json
CONSTELLATION='{
  "name": "test constellation",
  "vectors": [
    [0, 1],
    [1, 2]
  ]
}'

echo "login test"
JSON=$(curl -su default:default -X GET http://127.0.0.1:5000/api/v1/login)
printf "response:\n$JSON\n\n"

TOKEN=$(echo $JSON | jq '.token')
TOKEN="${TOKEN%\"}"
TOKEN="${TOKEN#\"}"

echo "GET user test"
JSON=$(curl -su ${TOKEN}:default -X GET http://127.0.0.1:5000/api/v1/user)
printf "response:\n$JSON\n\n"

echo "POST constellation test"
JSON=$(curl -su ${TOKEN}:default -X POST -H "Content-Type: application/json" -d "${CONSTELLATION}" http://127.0.0.1:5000/api/v1/constellations)
printf "response:\n$JSON\n\n"

CONSTELLATION_ID=$(echo $JSON | jq '.constellation_id')
CONSTELLATION_ID="${CONSTELLATION_ID%\"}"
CONSTELLATION_ID="${CONSTELLATION_ID#\"}"

echo "GET constellations test"
JSON=$(curl -su ${TOKEN}:default -X GET http://127.0.0.1:5000/api/v1/constellations)
printf "response:\n$JSON\n\n"

echo "GET constellation/id test"
JSON=$(curl -su ${TOKEN}:default -X GET http://127.0.0.1:5000/api/v1/constellations/${CONSTELLATION_ID})
printf "response:\n$JSON\n\n"
