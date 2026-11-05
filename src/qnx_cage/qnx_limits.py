"""Resource-limit backends for the snippet runner.

Two backends, one interface:

- LinuxRlimitBackend — the upstream behaviour: POSIX rlimits applied
  in the child via preexec_fn (RLIMIT_CPU 5 s, RLIMIT_AS 256 MiB,
  RLIMIT_FSIZE 1 MiB). VERIFIED in this sandbox.
- QnxApsBackend — the QNX-native behaviour: the CPU budget is enforced
  by the Adaptive Partitioning scheduler (see aps.py), not by rlimits.
  QNX Neutrino DOES support POSIX rlimits (QNX security docs: "Process
  resource limits (POSIX rlimits)"), so the rlimit path is kept as a
  second layer where the QNX Python port provides the `resource`
  module — that is a VERIFY-ON-TARGET item, not an assumption.
  This backend refuses to execute anywhere except QNX: it raises
  RuntimeError on Linux instead of pretending to enforce anything.

Neither backend is a container boundary. On QNX the real boundary is
the microkernel itself: the snippet runner is a separate process, the
server is a separate process, and a crashed/malicious runner cannot
take the server (or the kernel) down with it — that is the honest
QNX version of the "cage tier" claim.
"""
import os

from . import aps
from .platform_detect import is_qnx

CPU_SECONDS = 5
MEMORY_BYTES = 256 * 1024 * 1024
FILESIZE_BYTES = 1024 * 1024

try:
    import resource
    _RESOURCE_AVAILABLE = True
except ImportError:
    resource = None
    _RESOURCE_AVAILABLE = False


class LinuxRlimitBackend:
    """POSIX rlimits via preexec_fn. Works on Linux; also the fallback
    shape for QNX if its Python port ships the `resource` module."""

    name = "linux-rlimit"

    def preexec_fn(self):
        if not _RESOURCE_AVAILABLE:
            return None

        def preexec():
            try:
                resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS))
                resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
                resource.setrlimit(resource.RLIMIT_FSIZE, (FILESIZE_BYTES, FILESIZE_BYTES))
            except Exception:
                pass

        return preexec

    def launch_prefix(self):
        return []


class QnxApsBackend:
    """QNX Adaptive Partitioning. CPU budget enforced by the scheduler;
    rlimits applied as well when the `resource` module exists."""

    name = "qnx-aps-partition"

    def __init__(self, partition=aps.PARTITION_NAME):
        self.partition = partition

    def setup_commands(self):
        """Run once on the target (root) before the server starts."""
        return aps.setup_commands(self.partition)

    def launch_prefix(self):
        if not is_qnx():
            raise RuntimeError(
                "QnxApsBackend.launch_prefix() requires a QNX target — "
                "refusing to pretend APS enforcement exists on this host."
            )
        return aps.launch_prefix(self.partition)

    def preexec_fn(self):
        """Second layer: POSIX rlimits, only if the QNX Python port
        provides the `resource` module. Returns None (no-op) otherwise
        — the APS partition is the primary enforcement on QNX."""
        if not _RESOURCE_AVAILABLE:
            return None
        return LinuxRlimitBackend().preexec_fn()

    def cage_tier_label(self):
        return (
            "qnx-aps-partition (microkernel process isolation + "
            "Adaptive Partitioning 5% CPU budget)"
        )


def default_backend():
    """Pick the backend for the machine this code is running on."""
    if is_qnx():
        return QnxApsBackend()
    return LinuxRlimitBackend()


def cage_tier_label():
    """Label stamped on receipts, describing the actual enforcement."""
    if is_qnx():
        return QnxApsBackend().cage_tier_label()
    if _RESOURCE_AVAILABLE:
        return (
            "local-process-patch (NOT a container boundary — QNX APS "
            "partition is the real boundary on the target)"
        )
    return "local-process-patch (no rlimit module — limits unenforced)"
