#!/bin/bash

# json
CONSTELLATION='{
  "name": "test constellation",
  "vectors": [
    [0, 1],
    [1, 2]
  ]
}'

JSON=$(curl -su default:default -X GET http://127.0.0.1:5000/api/v1/login)

TOKEN=$(echo $JSON | jq '.token')
TOKEN="${TOKEN%\"}"
TOKEN="${TOKEN#\"}"

echo "GET user test"
curl -su ${TOKEN}:default -X GET http://127.0.0.1:5000/api/v1/user
printf "\n"

echo "POST constellation test"
curl -su ${TOKEN}:default -X POST -H "Content-Type: application/json" -d "${CONSTELLATION}" http://127.0.0.1:5000/api/v1/constellations
printf "\n"

echo "GET constellations test"
curl -su ${TOKEN}:default -i -X GET http://127.0.0.1:5000/api/v1/constellations
printf "\n"
