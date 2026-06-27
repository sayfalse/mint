#!/usr/bin/env bash
# scripts/compute-checksums.sh — compute SHA-256 for AUR + Chocolatey.
# Usage: ./scripts/compute-checksums.sh <version> [tar.gz|zip]
set -euo pipefail
VERSION="${1:-}"
FORMAT="${2:-both}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version> [tar.gz|zip|both]"
  exit 1
fi
if [[ "$FORMAT" == "tar.gz" || "$FORMAT" == "both" ]]; then
  echo "AUR (tar.gz) SHA-256:"
  curl -fsSL "https://github.com/sayfalse/mint/archive/refs/tags/v${VERSION}.tar.gz" | sha256sum
fi
if [[ "$FORMAT" == "zip" || "$FORMAT" == "both" ]]; then
  echo "Chocolatey (zip) SHA-256:"
  curl -fsSL "https://github.com/sayfalse/mint/archive/refs/tags/v${VERSION}.zip" | sha256sum
fi
