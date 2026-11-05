# QNX Global Hackathon — research notes (verified 5 Nov 2026)

All facts below were read from the official pages on 5 Nov 2026
(Devpost page crawled 18:07 UTC). Anything marked UNVERIFIED was not
confirmed from an official source in this pass.

## 1. The hackathon (official: https://qnx.devpost.com/)

- **Organiser/sponsor:** BlackBerry Ltd (QNX); administrator Devpost.
- **Submission period:** 2 Nov 2026 11:00 ET – 15 Dec 2026 14:00 ET.
  **Deadline in IST: Wed 16 Dec 2026 00:30 IST** (verified by date
  conversion: 14:00 EST = 19:00 UTC = 00:30 IST next day).
- **Judging:** 15–29 Jan 2027. **Community voting:** same window.
  **Winners announced on or around 4 Feb 2027 14:00 ET = Fri 5 Feb
  2027 00:30 IST.**
- **Prizes — $50,000+ total:** Grand $10,000 (1) + podcast episode +
  coffee chat with John Wall (QNX CEO); Best of each category $4,000
  (5); Runner-up per category $2,000 (5); Honorable Mention $1,000
  (3); Best Codelab/Tutorial $3,500 (1); Best use of QNX-specific
  Technologies $3,500 (1); Community Choice — blog/social feature +
  swag (no cash). Category prizes for Open-Source Contribution &
  Ports: Best $4,000, Runner-up $2,000.
- **Categories (pick one):** Robotics & Medical; Automotive &
  Mobility; Low-level Software; Developer Tooling & Host Tools;
  **Open-Source Contribution & Ports** (our category).

## 2. Eligibility (official rules, https://qnx.devpost.com/rules)

- 18+ at time of entry. Solo entry allowed; teams allowed.
- NOT open to residents of countries where US/local law prohibits
  participation — listed: Brazil, Russia, Crimea, Cuba, Iran, North
  Korea + US-sanctioned countries. **India is NOT in the excluded
  list → India eligible (verified against the rules text).**
- No purchase/payment necessary. Free access to QNX SDP 8.0 via QNX
  Everywhere (non-commercial licence).
- Project must be newly created 2 Nov–15 Dec 2026, OR pre-existing
  and "significantly updated" in the period (explain the update).
  **Ports category: NEW repository created during the Submission
  Period**, containing the patches/porting layer, QNX build files,
  build+run instructions, documentation. Reference upstream by URL,
  do NOT copy its history, do NOT submit a fork.
- Repo must be public, open-source licenced (licence file detectable
  in the About section), and must SHOW the project genuinely builds
  for / runs on QNX 8.0 — not merely name QNX in the README.
- Submission needs: repo URL, text description, **demo video < 3 min,
  public on YouTube, showing the project functioning on the device it
  was built for**, build/run instructions (QNX version, target
  hardware-or-QEMU, toolchain), one category. Ports: upstream URL (+
  PR URL if opened). Optional: codelab URL for the bonus prize.
- Judging criteria: Technological Implementation; Design; Potential
  Impact; Innovation & AI Creativity.
- Evidence of QNX use may include QNX-specific source/APIs, libraries,
  headers, buildfiles, toolchains, system images, config files, a
  demo running on QNX 8.0. POSIX-compatible code and ports remain
  eligible when the submission clearly demonstrates a meaningful QNX
  connection.

## 3. What QNX is, and the port path

- QNX Neutrino is a microkernel RTOS: the kernel does scheduling,
  message passing, signals/timers/interrupts/synchronisation only.
  Filesystems, networking, drivers run as user-space processes,
  MMU-protected; a crashing driver can restart without taking the
  system down. procnto = microkernel + process manager.
  275M+ vehicles; also medical, industrial, rail, robotics.
- **QNX SDP 8.0** (via QNX Everywhere, free non-commercial): GCC 12,
  C++20, Rust, Python; scales 64+ cores. Host: Linux/Windows (not
  macOS/ARM hosts). Licence via myQNX account + License Manager.
- **No hardware needed:** Quick Start Target Image (QSTI) for QEMU,
  and a Self-Hosted Developer Desktop (XFCE/Wayland QEMU image,
  Ubuntu 22.04/24.04 host) preloaded with Python, gcc, clang, git —
  native builds on QNX, no cross-compilation. Raspberry Pi 4 image
  exists; Pi 5 in development.
- **QNX-specific tech (for the $3,500 bonus + the port's real win):**
  Adaptive Partitioning (APS) — `ap`/`aps` utilities, `on -Xaps`
  launch option, scheduler budgets + `recommended` security policy;
  procmgr abilities (least-privilege instead of all-powerful root,
  incl. dropping the ability to create executable mappings);
  POSIX rlimits supported on QNX Neutrino. All confirmed from QNX
  docs (security features overview; `ap`/`aps` utility references).
- **Python on QNX:** present in the Developer Desktop and as a QNX
  open-source port (oss.qnx.com, 1,400+ ports / 600+ unique). Exact
  Python version in the SDP 8.0 QEMU image: UNVERIFIED (check on
  first boot).

## 4. Upstream baseline (verified in this sandbox, 5 Nov 2026)

- CageCheck: https://github.com/MSAbhishek22/cagecheck, public,
  commit a5588ef. Upstream test suite: **10/10 PASS** (unittest,
  0.24 s, Python 3.12.3, Linux). Modules: policy.py (106 lines,
  pure `ast`), cage.py (117, subprocess+resource+tempfile), server.py
  (134, http.server), receipts.py (61, datetime/json/os/re/uuid),
  llm.py (42, urllib.request — local mock without keys).
- Portability verdict per module (by reading the source):
  policy.py — portable as-is (pure stdlib `ast`).
  receipts.py — portable as-is (stdlib only).
  llm.py — portable as-is; stays local-mock on the target (no keys,
  no outbound call).
  server.py — portable; needs HOST=0.0.0.0 on QEMU (patch 002).
  cage.py — needs patch 001 (`resource` import guard, APS launch
  prefix). `subprocess`/`tempfile`/`os` are POSIX and expected fine;
  `preexec_fn` (fork-based) behaviour on the QNX Python port is
  UNVERIFIED.

## 5. Open questions (verify on first QNX boot — do not assume)

1. `sys.platform` value on the QNX Python port (detection uses
   `os.uname().sysname == "QNX"` as primary, so this is low-risk).
2. Python version in the SDP 8.0 QEMU image / Developer Desktop.
3. `resource` module present in the QNX Python port?
4. `subprocess` + `preexec_fn` (fork) behaviour on QNX Python.
5. `ap`/`aps`/`on -Xaps` exact flags on SDP 8.0 (docs fetched are
   6.4.1/7.1-era; APS itself is confirmed in 8.0 docs).
6. mkifs buildfile: exact startup binary + driver set for SDP 8.0
   x86_64 QEMU (qnx/cagecheck-qnx.build is a DRAFT).
7. QEMU networking mode that lets the host browser reach guest :8766.
8. Whether the QNX Python port ships `ctypes` (needed only if we
   call `procmgr_ability()` directly — optional stretch).

## Sources (all fetched 5 Nov 2026)

- https://qnx.devpost.com/ (hackathon page + prizes + categories)
- https://qnx.devpost.com/rules (official rules)
- https://qnx.software/en/developers/get-started/qnx-everywhere
- https://www.qnx.com/developers/docs/qnxeverywhere/introduction.html
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.security.system/topic/manual/security_features.html
- https://www.qnx.com/developers/docs/6.4.1/neutrino/utilities/a/ap.html
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.utilities/topic/a/aps.html
- https://qnx.software/en/blog/2026/qnx-self-hosted-developer-desktop
- https://www.qnx.com/developers/docs/7.1/com.qnx.doc.adaptivepartitioning.userguide/topic/security_Base_.html
