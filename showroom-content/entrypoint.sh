#!/bin/bash

set -euo pipefail

CLONE_DIR="${CLONE_DIR:-/files}"

mkdir -p "${CLONE_DIR}"
rm -rf -- "${CLONE_DIR}"/* "${CLONE_DIR}"/.[!.]* "${CLONE_DIR}"/..?*
cp -R /bundle/. "${CLONE_DIR}/"
touch "${CLONE_DIR}/.git-cloner"

echo "Immutable Showroom content is ready"
