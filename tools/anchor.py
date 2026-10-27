"""Stamp and upgrade the vault's record chain with OpenTimestamps."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _probe_ots():
    path = shutil.which("ots")
    if path is None:
        return None, "ots CLI not installed (pip install opentimestamps-client)"
    try:
        r = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            return None, f"ots at {path} returned {r.returncode}"
        return path, (r.stdout or r.stderr or "").strip().split("\n")[0]
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"ots could not run: {e}"


def stamp(ledger):
    ots, why = _probe_ots()
    if ots is None:
        print(f"cannot stamp: {why}", file=sys.stderr)
        return 1
    if not ledger.exists():
        print(f"no ledger at {ledger}", file=sys.stderr)
        return 1
    target = ledger.with_suffix(ledger.suffix + ".ots")
    if target.exists():
        print(f"already stamped: {target}")
        return 0
    r = subprocess.run([ots, "stamp", str(ledger)], capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not target.exists():
        print(f"stamp failed: {r.stderr[-300:]}", file=sys.stderr)
        return 1
    record = {
        "ledger_sha256": _sha256_file(ledger),
        "stamped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ots_file": target.name,
    }
    manifest = ledger.parent / "anchor_manifest.jsonl"
    with manifest.open("a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
    print(f"stamped: {target} (sha256 {record['ledger_sha256'][:16]}...)")
    return 0


def upgrade(ledger):
    ots, why = _probe_ots()
    if ots is None:
        print(f"cannot upgrade: {why}", file=sys.stderr)
        return 1
    target = ledger.with_suffix(ledger.suffix + ".ots")
    if not target.exists():
        print(f"nothing to upgrade: {target}", file=sys.stderr)
        return 1
    r = subprocess.run([ots, "upgrade", str(target)], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print(f"upgrade failed: {r.stderr[-300:]}", file=sys.stderr)
        return 2
    print(f"upgraded: {target}")
    return 0


def verify(ledger):
    ots, why = _probe_ots()
    if ots is None:
        print(f"cannot verify: {why}", file=sys.stderr)
        return 1
    target = ledger.with_suffix(ledger.suffix + ".ots")
    if not target.exists():
        print(f"not stamped: {target}", file=sys.stderr)
        return 1
    r = subprocess.run([ots, "verify", str(target)], capture_output=True, text=True, timeout=60)
    print(r.stdout + r.stderr)
    return 0 if r.returncode == 0 else 1


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("stamp", "upgrade", "verify"):
        s = sub.add_parser(name)
        s.add_argument("ledger", nargs="?", default="vault/catalytic_barrier/records.jsonl")
    a = ap.parse_args(argv)
    ledger = Path(a.ledger)
    return {"stamp": stamp, "upgrade": upgrade, "verify": verify}[a.cmd](ledger)


if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
