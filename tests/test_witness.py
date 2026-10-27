import sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import ledger as L, witness as W

class TestWitness(unittest.TestCase):
    def test_honest_agrees(self):
        p = Path(tempfile.mkdtemp()) / "r.jsonl"
        for i in range(5):
            L.append(p, "claim", {"claim_id": f"c{i}"})
        primary = {"size": L.verify(p), "head": L.head(p)[1]}
        w = W.verify_chain(p)
        self.assertEqual(primary, w)

    def test_tampered_refused(self):
        p = Path(tempfile.mkdtemp()) / "r.jsonl"
        L.append(p, "vault", {"vault_id": "v1"})
        p.write_text(p.read_text().replace('"v1"', '"v2"'))
        with self.assertRaises(W.Unreadable):
            W.verify_chain(p)

if __name__ == "__main__":
    unittest.main()
