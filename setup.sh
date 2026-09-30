#!/usr/bin/env bash
# setup.sh — clones (or updates) every repo listed in manifest.yaml.
# Usage: run from the moto-platform workspace root.
#   ./setup.sh                    → clone/update all
#   ./setup.sh moto-vehicle-defs  → apply only that repo's ref
#
# Every repo ends on its manifest ref with its submodules (external/moto-vehicle-defs)
# at the commits that ref pins. Any git error stops the script.
#
# Requires: yq (YAML reader) — install: brew install yq  (or pip install yq)

set -euo pipefail
MANIFEST="manifest.yaml"
NAME=""
trap 'echo "✗ setup.sh stopped${NAME:+ at $NAME}: see the error above" >&2' ERR

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
    git -C "$NAME" fetch --all --tags
  else
    echo "→ cloning $NAME ($REF)..."
    git clone "$URL" "$NAME"
  fi
  git -C "$NAME" checkout "$REF"
  # A branch ref fast-forwards to its remote; a tag checks out as a detached HEAD, already exact.
  if git -C "$NAME" symbolic-ref -q HEAD > /dev/null; then
    git -C "$NAME" pull --ff-only origin "$REF"
  fi
  git -C "$NAME" submodule update --init --recursive
done

echo ""
echo "Done. Current combination (versions from manifest.yaml):"
yq -r '.repos[] | "  " + .name + " @ " + .ref' "$MANIFEST"
