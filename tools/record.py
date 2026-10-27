"""One record entry. Envelope + canonical JSON + hash. No append here."""
import hashlib
import json
from datetime import datetime, timezone

FORMAT = "dark-synth-record/v1"
ZERO_HASH = "0" * 64
KINDS = {"vault", "claim", "attempt", "verdict", "annotation"}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build(kind, data, *, seq, prev, at=None):
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    if at is None:
        at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = {
        "format": FORMAT, "seq": seq, "kind": kind, "at": at,
        "data": data, "prev": prev,
    }
    entry["hash"] = sha256_hex(canonical(entry))
    return entry


def verify_entry(entry, *, expected_seq, expected_prev):
    if entry.get("format") != FORMAT:
        raise ValueError(f"wrong format: {entry.get('format')!r}")
    if entry.get("seq") != expected_seq:
        raise ValueError(f"seq mismatch: {entry.get('seq')} vs {expected_seq}")
    if entry.get("prev") != expected_prev:
        raise ValueError(f"prev mismatch at seq {expected_seq}")
    if entry.get("kind") not in KINDS:
        raise ValueError(f"unknown kind {entry.get('kind')!r}")
    body = {k: v for k, v in entry.items() if k != "hash"}
    if entry.get("hash") != sha256_hex(canonical(body)):
        raise ValueError(f"hash mismatch at seq {expected_seq}")


def head(path):
    last_hash, n = ZERO_HASH, 0
    if not path.exists():
        return n, last_hash
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        last_hash = entry["hash"]
        n += 1
    return n, last_hash
