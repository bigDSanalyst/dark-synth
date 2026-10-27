"""Append, verify, head, annotate. Append-only, never rewritten."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import record


class ChainBroken(Exception):
    pass


def verify(path):
    prev = record.ZERO_HASH
    n = 0
    if not path.exists():
        return 0
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            raise ChainBroken(f"line {line_no}: not JSON ({e})")
        try:
            record.verify_entry(entry, expected_seq=n, expected_prev=prev)
        except ValueError as e:
            raise ChainBroken(f"line {line_no}: {e}")
        prev = entry["hash"]
        n += 1
    return n


def append(path, kind, data):
    if path.exists():
        verify(path)
        n, prev = record.head(path)
    else:
        n, prev = 0, record.ZERO_HASH
    entry = record.build(kind, data, seq=n, prev=prev)
    with path.open("a", encoding="utf-8") as f:
        f.write(record.canonical(entry) + "\n")
    return entry


def head(path):
    return record.head(path)


def annotate(path, target_seq, label, reason, by):
    verify(path)
    target_hash = None
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry["seq"] == target_seq:
            target_hash = entry["hash"]
            break
    if target_hash is None:
        raise ValueError(f"no entry at seq {target_seq}")
    if label not in {"unsound", "superseded", "retracted", "note"}:
        raise ValueError(f"unknown label {label!r}")
    return append(path, "annotation", {
        "target": {"seq": target_seq, "hash": target_hash},
        "label": label, "reason": reason, "by": by,
    })


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: ledger.py verify|head|annotate <path> [...]")
        return 0
    cmd, path = argv[0], Path(argv[1])
    if cmd == "verify":
        try:
            n = verify(path)
            print(f"ok: {n} entries, chain intact")
            return 0
        except ChainBroken as e:
            print(f"BROKEN: {e}", file=sys.stderr)
            return 1
    elif cmd == "head":
        n, h = head(path)
        print(json.dumps({"size": n, "last_hash": h}))
        return 0
    return 2


if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
