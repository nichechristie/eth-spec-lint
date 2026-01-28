#!/bin/sh
set -e

MODE="${1:-pr}"
shift || true

if [ "$MODE" = "full" ]; then
    eth-spec-lint "$@" scan
elif [ "$MODE" = "pr" ]; then
    eth-spec-lint "$@" check-pr
else
    eth-spec-lint "$@" "$MODE"
fi
