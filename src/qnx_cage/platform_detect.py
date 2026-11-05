"""Platform detection for the CageCheck-on-QNX port.

QNX detection: ``os.uname().sysname`` is ``"QNX"`` on QNX Neutrino
(this is the documented uname behaviour; the ``sys.platform`` value
for the QNX Python port is NOT asserted here because it was not
verified against a real QNX target — see RESEARCH.md open question 1).
"""
import os
import platform
import sys


def is_qnx():
    """True only when running on QNX Neutrino."""
    try:
        if os.uname().sysname == "QNX":
            return True
    except Exception:
        pass
    # Secondary signal only: some QNX Python builds report sys.platform
    # starting with "nto". Not relied on alone.
    return sys.platform.startswith("nto")


def platform_summary():
    """Small dict describing the current platform (for receipts/logs)."""
    try:
        uname = os.uname()
        sysname, release = uname.sysname, uname.release
    except Exception:
        sysname, release = "unknown", "unknown"
    return {
        "sysname": sysname,
        "release": release,
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "is_qnx": is_qnx(),
    }
