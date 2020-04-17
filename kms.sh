#!/bin/bash

set -e

eval "$(jq -r '@sh "KEY_ID=\(.key_id) PLAINTEXT=\(.plaintext)"')"

result=$(aws kms encrypt --key-id $KEY_ID --plaintext $PLAINTEXT --query CiphertextBlob --output text)

jq -n --arg result "$result" '{"result":$result}'