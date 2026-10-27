#!/usr/bin/env python3
"""Where is this vault? Computes; never writes."""
import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import manifest as M
import kernel_check as KC
import witness as W

OK, LOOK, WARN, DECIDE, DEGRADED, SKIPPED, DRIFT, BLOCK = (
    "ok", "LOOK", "WARN", "DECIDE", "DEGRADED", "SKIPPED", "DRIFT", "BLOCK"
)


@dataclass(frozen=True)
class Finding:
    level: str
    name: str
    reason: str
    next_step: str = ""


def check_charter(repo):
    p = repo / "charter" / "charter.yaml"
    if not p.exists():
        return [Finding(BLOCK, "charter", "charter/charter.yaml is missing")]
    cfg = M.load(p)
    out = []
    ok, msg = M.formation_ok(cfg)
    out.append(Finding(OK, "formation", msg) if ok else Finding(BLOCK, "formation", msg))
    import charter as CH
    sig_ok, sig_msg = CH.verify(p)
    if sig_ok:
        out.append(Finding(OK, "charter_signature", sig_msg))
    else:
        out.append(Finding(BLOCK, "charter_signature", sig_msg))
    if not (cfg.get("admissions") or {}).get("hand_proofs"):
        out.append(Finding(DECIDE, "hand_proof_admission",
                          "hand-proved claims cannot be admitted",
                          "add admissions.hand_proofs: [hand-proved-charter-v1]"))
    return out


def check_kernel(repo):
    b = KC.backends()
    if b["coqc"]["available"]:
        return [Finding(OK, "kernel", f"Coq: {b['coqc']['status']}")]
    return [Finding(DEGRADED, "kernel", "no Coq toolchain on PATH", "apt-get install coq")]


def check_ledger(repo):
    p = repo / "vault" / "catalytic_barrier" / "records.jsonl"
    if not p.exists():
        return [Finding(DECIDE, "ledger", "no ledger yet",
                        "tools/ledger.py append ...")]
    import ledger as L
    try:
        n = L.verify(p)
        return [Finding(OK, "ledger", f"{n} entries, chain intact")]
    except L.ChainBroken as e:
        return [Finding(BLOCK, "ledger_chain", str(e))]


def check_witness(repo):
    p = repo / "vault" / "catalytic_barrier" / "records.jsonl"
    if not p.exists():
        return [Finding(OK, "witness", "no ledger yet")]
    try:
        w = W.verify_chain(p)
        return [Finding(OK, "witness", f"independent verifier agrees: {w['size']} entries")]
    except W.Unreadable as e:
        return [Finding(BLOCK, "witness", str(e))]


def check_coq_files(repo):
    out = []
    for f in ("adversary.v", "k2m2.v"):
        p = repo / "vault" / "catalytic_barrier" / "coq" / f
        if not p.exists():
            out.append(Finding(BLOCK, f"coq.{f}", f"missing {f}"))
            continue
        cert = KC.certify(p.read_text())
        if cert.ok:
            out.append(Finding(OK, f"coq.{f}", f"accepted ({cert.sha256[:16]}...)"))
        elif cert.verdict == "not_checked":
            out.append(Finding(DEGRADED, f"coq.{f}", cert.detail))
        else:
            out.append(Finding(BLOCK, f"coq.{f}", cert.detail[:200]))
    return out


def check_audits(repo):
    d = repo / "audits" / "catalytic_barrier"
    if not d.is_dir():
        return [Finding(DECIDE, "audits", "no audit drawer yet",
                        "mkdir -p audits/catalytic_barrier")]
    expected = ["A1", "A2", "A3", "A4", "A5"]
    present = sorted(p.stem for p in d.glob("A*.md"))
    missing = [e for e in expected if e not in present]
    if missing:
        return [Finding(WARN, "audits", f"missing {missing}")]
    return [Finding(OK, "audits", f"{len(present)} audit file(s)")]



def check_anchors(repo):
    """Axiom 18: the .ots must be on the current ledger digest."""
    import hashlib, json
    p_ots = repo / "vault" / "catalytic_barrier" / "records.jsonl.ots"
    p_ledger = repo / "vault" / "catalytic_barrier" / "records.jsonl"
    p_manifest = repo / "vault" / "catalytic_barrier" / "anchor_manifest.jsonl"
    if not p_ots.exists():
        return [Finding(DECIDE, "anchors", "ledger not OTS-stamped",
                        "tools/anchor.py stamp vault/catalytic_barrier/records.jsonl")]
    if not p_manifest.exists():
        return [Finding(WARN, "anchors", ".ots exists but anchor_manifest.jsonl missing")]
    try:
        stamped = json.loads(p_manifest.read_text().strip().split("\n")[-1]).get("ledger_sha256", "")
    except (json.JSONDecodeError, IndexError):
        return [Finding(WARN, "anchors", "anchor_manifest.jsonl is corrupt")]
    current = hashlib.sha256(p_ledger.read_bytes()).hexdigest()
    if stamped != current:
        return [Finding(WARN, "anchors",
                        f"ledger changed since stamping ({stamped[:8]} -> {current[:8]})",
                        "re-run tools/anchor.py stamp after all appends are done")]
    if "BitcoinBlockHeaderAttestation" in p_ots.read_text(errors="replace"):
        return [Finding(OK, "anchors",
                        f"stamped and Bitcoin-confirmed (digest {current[:8]})")]
    return [Finding(LOOK, "anchors",
                    f"stamped, confirmation pending (digest {current[:8]})",
                    "run tools/anchor.py upgrade in ~24h")]



def check_security_pin(repo):
    """Axiom 23: fingerprint must be pinned outside the charter file."""
    cfg_path = repo / "charter" / "charter.yaml"
    sec_path = repo / "SECURITY.md"
    if not cfg_path.exists() or not sec_path.exists():
        return [Finding(DECIDE, "security_pin", "charter or SECURITY.md missing")]
    cfg = M.load(cfg_path)
    fp = cfg.get("signer_fingerprint", "")
    if not fp or fp == "PENDING":
        return [Finding(BLOCK, "security_pin", "charter has no fingerprint")]
    if fp in sec_path.read_text():
        return [Finding(OK, "security_pin",
                        f"fingerprint {fp[:16]}... cross-pinned in SECURITY.md")]
    return [Finding(BLOCK, "security_pin",
                    f"fingerprint {fp[:16]}... NOT in SECURITY.md (Axiom 23)",
                    f"add {fp} to SECURITY.md")]



def check_witness_coq(repo):
    """Independent witness: Coq files must match ledger attempts."""
    try:
        found = W.verify_coq_hashes(
            repo / "vault" / "catalytic_barrier" / "records.jsonl",
            repo / "vault" / "catalytic_barrier" / "coq",
        )
    except W.Unreadable as e:
        return [Finding(BLOCK, "witness_coq", str(e))]
    unmatched = [f for f in found if f["status"] == "unmatched"]
    if unmatched:
        return [Finding(BLOCK, "witness_coq",
                        f"{len(unmatched)} Coq file(s) unmatched: {[f['file'] for f in unmatched]}",
                        "append an attempt entry with the current sha256, or restore the file")]
    return [Finding(OK, "witness_coq",
                    f"{len(found)} Coq file(s) independently matched to ledger")]


def run(repo):
    findings = []
    findings.extend(check_charter(repo))
    findings.extend(check_security_pin(repo))
    findings.extend(check_kernel(repo))
    findings.extend(check_ledger(repo))
    findings.extend(check_witness(repo))
    findings.extend(check_witness_coq(repo))
    findings.extend(check_coq_files(repo))
    findings.extend(check_audits(repo))
    findings.extend(check_anchors(repo))
    return findings


def render(findings):
    return "\n".join(
        f"  {f.level:9s} {f.name}: {f.reason}"
        + (f"\n{'':12s}-> {f.next_step}" if f.next_step else "")
        for f in findings
    )


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    findings = run(repo)
    blocked = [f for f in findings if f.level == BLOCK]
    if a.json:
        print(json.dumps({
            "blocked": len(blocked),
            "checks": [{"level": f.level, "name": f.name, "reason": f.reason,
                        "next": f.next_step} for f in findings],
        }, indent=2))
        return 1 if blocked else 0
    print(render(findings))
    return 1 if blocked else 0


if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
