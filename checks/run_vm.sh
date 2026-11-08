#!/usr/bin/env bash
# C2 and C4: run the certificate inside the Lima VM "primegaps" (aarch64, Ubuntu, CPython 3.14), never on the host.
# usage: run_vm.sh SRC_DIR quick|full      SRC_DIR is the isolated host directory written by fetch.py.
set -euo pipefail
SRC="$1"; MODE="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"
VMDIR="$(limactl shell primegaps -- bash -lc 'echo $HOME' | tr -d '\r')/zhang240"
limactl shell primegaps -- bash -lc "rm -rf '$VMDIR' && mkdir -p '$VMDIR'"
limactl copy -r "$SRC/." "primegaps:$VMDIR/"
if [ "$MODE" = quick ]; then
  limactl shell primegaps -- bash -lc "cd '$VMDIR' && python3 --version && /usr/bin/time -v python3 -B -I -S verify.py" > "$HERE/logs/quick.log" 2>&1 || true
  tail -n 30 "$HERE/logs/quick.log"
else
  limactl shell primegaps -- bash -lc "cd '$VMDIR' && python3 -m venv .venv && .venv/bin/pip install -q -r requirements-full.txt && .venv/bin/pip freeze && /usr/bin/time -v .venv/bin/python -B verify.py --full" > "$HERE/logs/full.log" 2>&1 || true
  tail -n 30 "$HERE/logs/full.log"
fi
