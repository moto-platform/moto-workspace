#!/usr/bin/env bash
# setup.sh — clones (or updates) every repo listed in manifest.yaml.
# Usage: run from the moto-platform workspace root.
#   ./setup.sh                    → clone/update all
#   ./setup.sh moto-vehicle-defs  → apply only that repo's ref
#
# Requires: yq (YAML reader) — install: brew install yq  (or pip install yq)

set -euo pipefail
MANIFEST="manifest.yaml"

if ! command -v yq &> /dev/null; then
  echo "yq not found. Install: brew install yq  (or pip install yq)"
  exit 1
fi

REPO_COUNT=$(yq '.repos | length' "$MANIFEST")

for i in $(seq 0 $((REPO_COUNT - 1))); do
  NAME=$(yq -r ".repos[$i].name" "$MANIFEST")
  URL=$(yq -r ".repos[$i].url" "$MANIFEST")
  REF=$(yq -r ".repos[$i].ref" "$MANIFEST")

  # If a single repo was requested, skip the others
  if [ $# -gt 0 ] && [ "$1" != "$NAME" ]; then
    continue
  fi

  if [ -d "$NAME" ]; then
    echo "→ $NAME exists, updating to $REF..."
    (cd "$NAME" && git fetch --all --tags && git checkout "$REF" && git pull --ff-only origin "$REF" 2>/dev/null || true)
  else
    echo "→ cloning $NAME ($REF)..."
    git clone "$URL" "$NAME"
    (cd "$NAME" && git checkout "$REF" && git submodule update --init --recursive)
  fi
done

echo ""
echo "Done. Current combination (versions from manifest.yaml):"
yq -r '.repos[] | "  " + .name + " @ " + .ref' "$MANIFEST"
