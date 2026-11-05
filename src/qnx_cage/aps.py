"""Adaptive Partitioning (APS) command builders for the QNX port.

QNX Adaptive Partitioning guarantees a group of processes a share of
CPU time, so a runaway or malicious snippet can never starve the
CageCheck server itself. This module only BUILDS the command lines —
it never executes them. Execution happens on the QNX target (see
qemu/QEMU_NOTES.md) via the `ap`/`aps` utilities and the `on -Xaps=`
launch option, all documented in the QNX Neutrino docs:

- `ap create -b <budget> <partition>` — create a partition with a
  percentage CPU budget (QNX docs: `ap` utility).
- `on -Xaps=<partition>` — launch a process into a partition.
- `aps modify -S ... -s recommended` — scheduler/security policies.

The design choice: one partition `cagecheck_snippet` with a 5%
budget (matching the 5 s CPU cap the Linux cage enforces with
RLIMIT_CPU), a critical budget of 0, and the `recommended` security
policy so only the System partition can change scheduling parameters.

These strings are pure data and are fully unit-tested in this sandbox.
Whether `ap`/`aps` behave exactly this way on QNX SDP 8.0 is a
VERIFY-ON-TARGET item (the docs fetched are 6.4.1/7.1-era; the APS
feature itself is confirmed present in SDP 8.0 docs).
"""

PARTITION_NAME = "cagecheck_snippet"
PARTITION_BUDGET_PERCENT = 5
PARTITION_CRITICAL_BUDGET_MS = 0
SECURITY_POLICY = "recommended"


def setup_commands(partition=PARTITION_NAME, budget=PARTITION_BUDGET_PERCENT,
                   critical_ms=PARTITION_CRITICAL_BUDGET_MS):
    """Commands to run once on the QNX target (as root) before starting
    the server. Returns a list of argv lists, in order."""
    return [
        # Lock the scheduler down first: only the System partition may
        # change scheduling parameters afterwards.
        ["aps", "modify", "-s", SECURITY_POLICY],
        # 5% CPU budget for anything the snippet runner does.
        ["ap", "create", "-b", str(budget),
         "-B", str(critical_ms), partition],
    ]


def launch_prefix(partition=PARTITION_NAME):
    """argv prefix that launches a process inside the snippet partition."""
    return ["on", "-Xaps=" + partition]


def show_command(partition=PARTITION_NAME):
    """Command to inspect the partition at runtime (receipt evidence)."""
    return ["ap", "show", partition]


def teardown_command(partition=PARTITION_NAME):
    """Command to remove the partition (after judging / shutdown)."""
    return ["ap", "destroy", partition]
