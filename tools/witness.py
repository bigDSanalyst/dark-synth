"""Independent verifier. Shares no code with ledger.py."""
import hashlib
import json


class Unreadable(Exception):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_chain(path, expected_head=None):
    if not path.exists():
        raise Unreadable(f"no ledger at {path}")
    prev = "0" * 64
    n = 0
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            raise Unreadable(f"line {line_no}: not JSON: {e}")
        if entry.get("seq") != n:
            raise Unreadable(f"line {line_no}: seq mismatch")
        if entry.get("prev") != prev:
            raise Unreadable(f"line {line_no}: prev mismatch")
        body = {k: v for k, v in entry.items() if k != "hash"}
        if entry.get("hash") != sha256_hex(canonical(body)):
            raise Unreadable(f"line {line_no}: hash mismatch")
        prev = entry["hash"]
        n += 1
    if expected_head is not None and prev != expected_head:
        raise Unreadable(f"head mismatch")
    return {"size": n, "head": prev}


def compare_with_primary(primary, witness):
    pairs = [
        ("size", primary.get("size"), witness.get("size")),
        ("head", primary.get("head"), witness.get("head")),
    ]
    disagreements = [f"{name}: primary={a!r} witness={b!r}"
                     for name, a, b in pairs if a != b]
    return {"agrees_with_primary": not disagreements, "disagreements": disagreements}
