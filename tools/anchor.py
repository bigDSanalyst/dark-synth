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
    """Fully-offline content-binding verify.

    Uses `ots info` to extract (a) the file digest baked into the OTS proof
    and (b) the confirmed Bitcoin block height. Compares the proof's digest
    to sha256(current ledger) and cross-checks anchor_manifest.jsonl.

    Return codes:
      0 — proof valid, digest matches, manifest matches
      1 — infrastructure (no ots CLI, missing proof file)
      2 — content mismatch (proof digest stale, or manifest stale, or
          proof has no confirmed attestation)
    """
    import hashlib, json, re
    ots, why = _probe_ots()
    if ots is None:
        print(f"cannot verify: {why}", file=sys.stderr)
        return 1
    proof = ledger.with_suffix(ledger.suffix + ".ots")
    if not proof.exists():
        print(f"not stamped: {proof}", file=sys.stderr)
        return 1

    # 1. Parse the proof offline via `ots info` (does not touch the network).
    try:
        r = subprocess.run([ots, "info", str(proof)],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"ots info failed to run: {e}", file=sys.stderr)
        return 1
    info = r.stdout + r.stderr

    # 2. Extract the confirmed block height.
    height_match = re.search(r"BitcoinBlockHeaderAttestation\((\d+)\)", info)
    if not height_match:
        print("no Bitcoin block attestation in proof (pending or unconfirmed):", file=sys.stderr)
        print(info[-300:], file=sys.stderr)
        return 2
    height = height_match.group(1)

    # 3. Extract the digest the proof was made over.
    digest_match = re.search(r"File sha256 hash:\s*([0-9a-f]{64})", info)
    if not digest_match:
        print("could not extract proof digest from `ots info` output", file=sys.stderr)
        return 2
    proof_digest = digest_match.group(1)

    # 4. Content binding #1: proof digest vs current ledger bytes.
    actual = hashlib.sha256(ledger.read_bytes()).hexdigest()
    if proof_digest != actual:
        print(f"proof digest mismatch: proof says {proof_digest[:16]}, "
              f"ledger is {actual[:16]}", file=sys.stderr)
        return 2

    # 5. Content binding #2 (defense in depth): anchor manifest.
    mf = ledger.parent / "anchor_manifest.jsonl"
    if not mf.exists():
        print("anchor_manifest.jsonl missing — no content binding", file=sys.stderr)
        return 2
    try:
        last = json.loads(mf.read_text().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        print("anchor_manifest.jsonl corrupt or empty", file=sys.stderr)
        return 2
    expected = last.get("ledger_sha256", "")
    if expected != actual:
        print(f"manifest mismatch: expected {expected[:16]}, actual {actual[:16]}", file=sys.stderr)
        return 2

    print(f"anchor ok: block {height}, digest {actual[:16]} matches proof + manifest")
    return 0


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
