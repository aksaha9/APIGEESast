#!/bin/bash
BUNDLE_DIR=$1
OUTPUT=$2

# Assumes image is built as 'apigeelint:latest'
docker run --rm \
  -v "$BUNDLE_DIR:/bundle" \
  apigeelint:latest \
  apigeelint -s /bundle -f json.js > "$OUTPUT"