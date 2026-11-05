"""Verify the upstream CageCheck baseline without copying its code.

Reads the upstream modules from the existing local CageCheck tree
(read-only import — this script never writes to that tree) and runs
the same policy scan vectors the upstream test suite uses, proving the
pure-stdlib modules that the QNX port depends on behave identically
here. Run:  python3 src/qnx_cage/verify_upstream.py <path-to-cagecheck>

Exit 0 = baseline green. This is a port-readiness check, not a test
of QNX itself: it proves the code we port is sound on Linux; the QNX
run is still a separate, on-target verification (see BUILD_PLAN.md).
"""
import importlib.util
import os
import sys

VECTORS = [
    # (snippet, expected verdict)
    ("x = 1 + 1\nprint(x)\n", "CLEAN"),
    ("open('/home/u/.ssh/id_ed25519').read()\n", "BLOCKED"),
    ("import subprocess\nsubprocess.run(['ls'])\n", "BLOCKED"),
    ("import socket\nprint('socket imported, never used')\n", "HELD"),
    ("import socket\ns = socket.socket()\ns.connect(('example.com', 80))\n", "BLOCKED"),
    ("os.environ['API_KEY']\n", "BLOCKED"),
    ("open('/etc/passwd').read()\n", "BLOCKED"),
]


def load_policy(cagecheck_root):
    path = os.path.join(cagecheck_root, "app", "policy.py")
    spec = importlib.util.spec_from_file_location("upstream_policy", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        print("usage: verify_upstream.py <path-to-cagecheck-tree>")
        return 2
    policy = load_policy(sys.argv[1])
    failures = 0
    for snippet, expected in VECTORS:
        verdict, rule, _detail = policy.scan(snippet)
        status = "OK  " if verdict == expected else "FAIL"
        if verdict != expected:
            failures += 1
        print(f"{status} expected={expected:8s} got={verdict:8s} rule={rule}")
    print(f"{len(VECTORS) - failures}/{len(VECTORS)} policy vectors pass")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
