"""Append, verify, tamper, refuse."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import record as R
import ledger as L
import witness as W


def _tmp():
    return Path(tempfile.mkdtemp(prefix="ds-test-")) / "records.jsonl"


class TestLedger(unittest.TestCase):
    def test_append(self):
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        L.append(p, "claim", {"claim_id": "c1"})
        self.assertEqual(L.verify(p), 2)

    def test_edit_breaks_chain(self):
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        L.append(p, "claim", {"claim_id": "c1"})
        p.write_text(p.read_text().replace('"c1"', '"c2"'))
        with self.assertRaises(L.ChainBroken):
            L.verify(p)

    def test_annotation(self):
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        L.append(p, "claim", {"claim_id": "c1"})
        L.annotate(p, 1, "unsound", "kernel bug", "owner")
        entries = [json.loads(l) for l in p.read_text().splitlines()]
        self.assertEqual(entries[-1]["kind"], "annotation")
        self.assertEqual(entries[-1]["data"]["target"]["seq"], 1)

    def test_forged_detected(self):
        """A single-entry chain cannot detect a rewrite of itself (no anchor).
        With two entries, rewriting the first breaks the second's prev hash.
        This is what Axiom 18 (external binding) exists for: the chain alone
        is only forward-consistent, not anchor-consistent."""
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        L.append(p, "claim", {"claim_id": "c1"})
        lines = p.read_text().splitlines()
        real = json.loads(lines[0])
        forged = dict(real)
        forged["data"]["vault_id"] = "forged"
        forged["hash"] = R.sha256_hex(R.canonical({k: v for k, v in forged.items() if k != "hash"}))
        lines[0] = json.dumps(forged, sort_keys=True, separators=(",", ":"))
        p.write_text("\n".join(lines) + "\n")
        # Entry 1's prev still points to the *original* hash of entry 0,
        # which no longer matches the rewritten entry 0.
        with self.assertRaises(L.ChainBroken):
            L.verify(p)


class TestWitness(unittest.TestCase):
    def test_witness_agrees(self):
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        primary = {"size": L.verify(p), "head": L.head(p)[1]}
        w = W.verify_chain(p)
        self.assertTrue(W.compare_with_primary(primary, w)["agrees_with_primary"])

    def test_tampered_refused(self):
        p = _tmp()
        L.append(p, "vault", {"vault_id": "v1"})
        p.write_text(p.read_text().replace('"v1"', '"v2"'))
        with self.assertRaises(W.Unreadable):
            W.verify_chain(p)


if __name__ == "__main__":
    unittest.main()
