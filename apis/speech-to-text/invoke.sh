#!/bin/bash
PROJECT_ID=dx-project-dev

source .env

curl -s -X POST -H "Content-Type: application/json" --data-binary @sync-request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${GOOGLE_API_KEY}"