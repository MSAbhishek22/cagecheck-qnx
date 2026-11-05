# QEMU notes — running CageCheck on QNX 8.0 without hardware

## The official path (do this first)

1. **myQNX account + free licence** — user's tap (account creation is
   NOT done by agents). Get free non-commercial access at
   https://qnx.software/en/developers/get-started/qnx-everywhere
   ("Get free access to QNX SDP 8.0", ~5 min per the Devpost page),
   then accept/deploy the licence in myQNX License Manager
   (https://www.qnx.com/getqnx).
2. **Install SDP 8.0 on the host** — Windows or Linux host (QNX SDP
   8.0 does not support macOS or ARM hosts, per the install guide).
   Install takes ~30–60 min via QNX Software Center.
3. **Quick Start Target Image (QSTI) for QEMU** — in Software Center,
   Available tab, search "quick start", install "QNX SDP 8.0 Quick
   Start Target Image for QEMU". The image lands under
   `~/qnx800/images`; follow the README.md in the `qemu` directory
   there and the PDF in `./qemu_qsti/docs/` to boot it.
   - Alternative with a GUI: the **QNX Self-Hosted Developer Desktop**
     (XFCE on Wayland, ships as a QEMU image, Ubuntu 22.04/24.04 host)
     comes preloaded with Python, gcc, clang, git and sample projects —
     it is the fastest way to iterate a Python port natively on QNX
     (no cross-compilation).
4. **Boot QEMU** — follow the QSTI docs for the exact command line.
   QEMU networking: user-mode networking (SLIRP) is the simple path
   for host→guest HTTP; a tap/bridge gives the guest a real LAN IP.
   The CageCheck server binds `0.0.0.0:8766` on QNX (patch 002), so
   the host browser reaches it at the guest IP.
5. **Copy the port in** — `scp` the staged tree (`make stage`, then
   apply `patches/`) to `/opt/cagecheck-qnx` on the target, or use
   `mkqnximage` to build an image with the files baked in
   (see `qnx/cagecheck-qnx.build` — DRAFT, verify on target).
6. **Start it** — on the target, as root:
   `sh /opt/cagecheck-qnx/run-on-qnx.sh`
   This creates the `cagecheck_snippet` APS partition (5% budget),
   then starts the server. Verify with `ap show cagecheck_snippet`
   and `curl http://<guest-ip>:8766/health` from the host.
7. **Record the video from the host browser** hitting the live QEMU
   target URL — that is the submission video (under 3 min, public
   YouTube). Never a screenshot slideshow.

## What this sandbox proved, and what it cannot prove

- PROVED here: upstream baseline 10/10 tests; patches apply cleanly
  and keep 10/10 + live server smoke test green on Linux; APS command
  strings; rlimit enforcement in a child process.
- CANNOT prove here: no QEMU installed in this sandbox, no QNX image,
  no SDP. First QNX boot is the verification gate for: Python on QNX
  (version, `resource` module, `subprocess`+`preexec_fn` behaviour),
  `ap`/`aps`/`on -Xaps` on SDP 8.0, QEMU networking to the host
  browser, and the mkifs buildfile.

## Fallback if QEMU fails

If the QEMU target cannot be booted, the Ports category still accepts
a host-based tool, but the honest fallback is: **host-side QNX build
verification** — cross-compile/package with the SDP toolchain on the
Linux host and show the QNX build files + `mkifs` image build
succeeding, with the video showing the build + a clearly-labelled
host-side run. That is weaker than a QEMU run and must be labelled as
such in the submission — never presented as "running on QNX".
