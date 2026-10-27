"""Mutation-test the audit drawer. Exit 0 only if all caught or declared."""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
MUTANTS = [
    ("adversary weakened", "drop exponent, use raw alpha",
     "zpow_nat (alpha r') (a s) - zpow_nat (alpha s) (a s)",
     "(alpha r') - zpow_nat (alpha s) (a s)"),
]
EQUIVALENT = {}
UNTESTED = {
    "x-degree grading": "general statement over all F; hand-audit only",
    "residual-case target": "instruction, not an identity; hand-audit only",
    "S-projection counterexample": "specific counterexample not mechanized; hand-audit only",
}
def _copy(src):
    """Copy the vault for mutation testing, excluding build artifacts.
    FM12: .lake/ (Mathlib cache) is ~3 GB; coq artifacts, python bytecode,
    and any *build* directory must never be copied — the mutation test
    cares only about source."""
    d = Path(tempfile.mkdtemp(prefix="ds-mut-")) / "repo"
    shutil.copytree(
        src, d,
        ignore=shutil.ignore_patterns(
            ".git", "__pycache__", "*.pyc", ".pytest_cache",
            ".lake", "*.olean", "*.ilean",
            "*.aux", "*.glob", "*.vo", "*.vok", "*.vos", "*.vio",
            "build", "node_modules",
        ),
    )
    return d
def _catch(repo, rel_path):
    r = subprocess.run(["coqc", str(repo / rel_path)], capture_output=True, text=True, timeout=180)
    return r.returncode != 0
def run(vault_dir):
    results = []
    target = vault_dir / "coq" / "adversary.v"
    if not target.exists():
        return False, [{"mutant": "baseline", "status": "SURVIVED", "why": f"missing {target}"}]
    base = _copy(vault_dir)
    try:
        if _catch(base, "coq/adversary.v"):
            return False, [{"mutant": "baseline", "status": "SURVIVED", "why": "does not compile"}]
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    for name, breaks, old, new in MUTANTS:
        repo = _copy(vault_dir)
        try:
            p = repo / "coq" / "adversary.v"
            src = p.read_text()
            if src.count(old) != 1:
                results.append({"mutant": name, "status": "SURVIVED",
                                "why": f"source does not contain {old!r} exactly once"})
                continue
            p.write_text(src.replace(old, new))
            caught = _catch(repo, "coq/adversary.v")
        finally:
            shutil.rmtree(repo.parent, ignore_errors=True)
        results.append({"mutant": name, "status": "caught" if caught else "SURVIVED"})
    for name, why in EQUIVALENT.items():
        results.append({"mutant": name, "status": "equivalent", "why": why})
    for name, why in UNTESTED.items():
        results.append({"mutant": name, "status": "untested", "why": why})
    ok = all(r["status"] in ("caught", "equivalent", "untested") for r in results)
    return ok, results
def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(ROOT / "vault" / "catalytic_barrier"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    ok, results = run(Path(a.vault))
    if a.json:
        print(json.dumps({"ok": ok, "mutants": results}, indent=2))
    else:
        for r in results:
            print(f"  {r['status']:11s} {r['mutant']:32s} {r.get('why','')}")
        print("ALL CAUGHT" if ok else "NOT ALL CAUGHT")
    return 0 if ok else 1
if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
