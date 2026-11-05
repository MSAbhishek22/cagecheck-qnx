"""Port tests for CageCheck-on-QNX. Run from the qnx/ scaffold root:

    python3 -m unittest discover -s tests -v

What is tested here (all runnable in this Linux sandbox):
- platform detection (Linux here; QNX branch is data, not execution)
- APS command builders (exact argv — these are the commands that will
  run on the QNX target)
- Linux rlimit backend (real enforcement in a child process)
- QNX backend refuses to run off-target (no fake enforcement)
- the three patches apply cleanly to a fresh copy of upstream and
  the upstream suite still passes 10/10 afterwards
- the QNX buildfile / Makefile contain the required sections

What is NOT tested here (needs the QNX 8.0 QEMU target):
- anything that executes on QNX: `ap`/`aps`/`on -Xaps`, the
  `resource` module on the QNX Python port, mkifs/mkqnximage builds.
  Those are VERIFY-ON-TARGET items, listed in BUILD_PLAN.md.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from qnx_cage import aps, platform_detect, qnx_limits  # noqa: E402

UPSTREAM = os.path.expanduser("~/workspace/hackathons/cagecheck")


class TestPlatformDetect(unittest.TestCase):
    def test_not_qnx_here(self):
        self.assertFalse(platform_detect.is_qnx())

    def test_summary_shape(self):
        s = platform_detect.platform_summary()
        self.assertEqual(s["sysname"], "Linux")
        self.assertFalse(s["is_qnx"])
        self.assertTrue(s["python"].startswith("3."))


class TestApsCommands(unittest.TestCase):
    def test_setup_commands(self):
        cmds = aps.setup_commands()
        self.assertEqual(cmds[0], ["aps", "modify", "-s", "recommended"])
        self.assertEqual(cmds[1],
                         ["ap", "create", "-b", "5", "-B", "0", "cagecheck_snippet"])

    def test_launch_prefix(self):
        self.assertEqual(aps.launch_prefix(), ["on", "-Xaps=cagecheck_snippet"])

    def test_show_and_teardown(self):
        self.assertEqual(aps.show_command(), ["ap", "show", "cagecheck_snippet"])
        self.assertEqual(aps.teardown_command(), ["ap", "destroy", "cagecheck_snippet"])


class TestLinuxRlimitBackend(unittest.TestCase):
    def test_preexec_applies_rlimits_in_child(self):
        backend = qnx_limits.LinuxRlimitBackend()
        preexec = backend.preexec_fn()
        self.assertIsNotNone(preexec)
        code = (
            "import resource, json;"
            "print(json.dumps({"
            "'cpu': resource.getrlimit(resource.RLIMIT_CPU),"
            "'as': resource.getrlimit(resource.RLIMIT_AS),"
            "'fsize': resource.getrlimit(resource.RLIMIT_FSIZE)}))"
        )
        proc = subprocess.run([sys.executable, "-c", code],
                              capture_output=True, text=True,
                              preexec_fn=preexec, timeout=10)
        import json as _json
        limits = _json.loads(proc.stdout.strip())
        self.assertEqual(limits["cpu"], [5, 5])
        self.assertEqual(limits["as"], [256 * 1024 * 1024, 256 * 1024 * 1024])
        self.assertEqual(limits["fsize"], [1024 * 1024, 1024 * 1024])

    def test_launch_prefix_empty_on_linux(self):
        self.assertEqual(qnx_limits.LinuxRlimitBackend().launch_prefix(), [])


class TestQnxBackendRefusesOffTarget(unittest.TestCase):
    def test_launch_prefix_raises_on_linux(self):
        with self.assertRaises(RuntimeError):
            qnx_limits.QnxApsBackend().launch_prefix()

    def test_default_backend_is_linux_here(self):
        self.assertIsInstance(qnx_limits.default_backend(),
                              qnx_limits.LinuxRlimitBackend)

    def test_setup_commands_are_data_not_execution(self):
        cmds = qnx_limits.QnxApsBackend().setup_commands()
        self.assertEqual(len(cmds), 2)
        self.assertEqual(cmds[0][0], "aps")


class TestPatchesApplyAndPass(unittest.TestCase):
    def test_patches_apply_and_upstream_suite_passes(self):
        tmp = tempfile.mkdtemp(prefix="qnx-patch-check-")
        try:
            shutil.copytree(UPSTREAM, os.path.join(tmp, "cagecheck"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            tree = os.path.join(tmp, "cagecheck")
            for name in sorted(os.listdir(os.path.join(ROOT, "patches"))):
                if not name.endswith(".patch"):
                    continue
                path = os.path.join(ROOT, "patches", name)
                with open(path, "rb") as f:
                    r = subprocess.run(["patch", "-p1", "--silent"],
                                       stdin=f, cwd=tree,
                                       capture_output=True)
                self.assertEqual(r.returncode, 0, f"patch failed: {name}: {r.stderr!r}")
            r = subprocess.run([sys.executable, "-m", "unittest", "discover",
                                "-s", "tests"], cwd=tree,
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr[-2000:])
            self.assertIn("OK", r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestQnxBuildFiles(unittest.TestCase):
    def test_buildfile_sections(self):
        path = os.path.join(ROOT, "qnx", "cagecheck-qnx.build")
        with open(path) as f:
            text = f.read()
        for needle in (".bootstrap", "[+script]", "procnto", "python",
                       "cagecheck", "[data=copy]"):
            self.assertIn(needle, text, f"buildfile missing: {needle}")

    def test_makefile_has_install_and_check(self):
        with open(os.path.join(ROOT, "qnx", "Makefile")) as f:
            text = f.read()
        self.assertIn("install:", text)
        self.assertIn("check:", text)


if __name__ == "__main__":
    unittest.main()
