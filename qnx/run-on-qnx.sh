#!/bin/sh
# run-on-qnx.sh — start CageCheck on the QNX 8.0 target (QEMU image).
# Run as root on the target, from /opt/cagecheck-qnx.
# VERIFY-ON-TARGET: `ap`/`aps` availability, python3 binary name.
set -e
cd "$(dirname "$0")"

# 1. Adaptive Partitioning: 5% CPU budget for snippet runners.
aps modify -s recommended
ap create -b 5 -B 0 cagecheck_snippet || true

# 2. Server: listens on all interfaces so the host browser (QEMU
# networking) can reach it. Receipts land in ./runs/audit.jsonl.
export CAGE_QNX_APS_PARTITION=cagecheck_snippet
export HOST=0.0.0.0
export PORT=8766
export PYTHONPATH=/opt/cagecheck-qnx

echo "CageCheck-on-QNX starting on http://$(hostname):8766/ (cage: qnx-aps-partition)"
exec python3 -m app.server
