import shutil, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import mutation_test as MT

@unittest.skipUnless(shutil.which("coqc"), "needs coqc")
class TestAuditTrail(unittest.TestCase):
    def test_mutants_caught_or_declared(self):
        ok, results = MT.run(ROOT / "vault" / "catalytic_barrier")
        for r in results:
            self.assertIn(r["status"], ("caught", "equivalent", "untested"),
                         msg=f"{r['mutant']}: {r.get('why', '')}")
        self.assertTrue(ok)

    def test_baseline_compiles(self):
        p = ROOT / "vault" / "catalytic_barrier" / "coq" / "adversary.v"
        r = subprocess.run(["coqc", str(p)], capture_output=True, text=True, timeout=180)
        self.assertEqual(r.returncode, 0, r.stderr[-500:])

if __name__ == "__main__":
    unittest.main()
