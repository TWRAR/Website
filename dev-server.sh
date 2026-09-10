#!/bin/bash
# TWRAR Website - Local dev server
# Usage: ./dev-server.sh [port] [--no-dev-mode]
#   port            default: 8000
#   --no-dev-mode   serve pages untouched, matching production
#
# DEV_MODE is forced ON for every run of this script, regardless of what
# was passed last time - every page gets a dev banner injected so it's
# obvious you're looking at a local build. Pass --no-dev-mode to test the
# site as it behaves in production instead.
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(command -v python3 || command -v python)"
if [ -z "$PYTHON" ]; then
    echo "Python 3 is required to run dev-server.py" >&2
    exit 1
fi

exec "$PYTHON" "$DIR/dev-server.py" "$@"
