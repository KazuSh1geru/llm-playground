#!/bin/bash
PROJECT_ID=dx-project-dev

gcloud auth application-default set-quota-project $PROJECT_ID

curl -s -H "Content-Type: application/json" \
    -H "Authorization: Bearer "$(gcloud auth print-access-token) \
    https://speech.googleapis.com/v1/speech:recognize \
    -d @sync-request.json