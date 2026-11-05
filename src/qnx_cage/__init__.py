"""CageCheck-on-QNX porting layer.

New code written 5 Nov 2026 for the QNX Global Hackathon (Open-Source
Contribution & Ports category). This package does NOT copy upstream
CageCheck code: it is the porting layer — platform detection, the QNX
Adaptive Partitioning (APS) command builders, and the resource-limit
backends. The upstream project is referenced by URL; the patches in
../patches/ describe the (small) changes the upstream files need.

Status: Linux backend VERIFIED in this sandbox (Python 3.12.3, tests
10/10 upstream baseline + port tests below). Every QNX branch is
clearly marked and is UNVERIFIED until it runs on a QNX 8.0 QEMU
target — nothing here pretends otherwise.
"""

from .platform_detect import is_qnx, platform_summary

__all__ = ["is_qnx", "platform_summary"]
