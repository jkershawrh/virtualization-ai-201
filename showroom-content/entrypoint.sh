#!/bin/bash

set -euo pipefail

CLONE_DIR="${CLONE_DIR:-/files}"

mkdir -p "${CLONE_DIR}"
rm -f "${CLONE_DIR}/.git-cloner"
find "${CLONE_DIR}" -mindepth 1 -delete
cp -a /bundle/. "${CLONE_DIR}/"
touch "${CLONE_DIR}/.git-cloner"

echo "Immutable Showroom content is ready"
