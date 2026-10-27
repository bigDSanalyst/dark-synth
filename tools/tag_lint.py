"""Enforce two-axis tags on every *claim* line in a vault record.

A claim line is a table row whose first cell names a specific theorem (e.g.
"Theorem 3.1"), not the table header "Theorem". Header rows are skipped."""
import argparse
import re
import sys
from pathlib import Path

# Require a designation after the keyword: "Theorem 3.1", "Lemma 3.6a",
# "Corollary A". Bare "Theorem" is a header, not a claim.
CLAIM_RE = re.compile(
    r"^\|\s*(?:Theorem|Lemma|Corollary|Proposition)\s+\S",
    re.IGNORECASE,
)
TAG_RE = re.compile(r"\[(V|A|P|t|run)/(proved|open|accepted|superseded|framing)\]")
ADMISSION_RE = re.compile(
    r"admission[:\s=]+(V-proved|kernel-proved|hand-proved-charter-v1)",
    re.IGNORECASE,
)


def lint(path):
    defects = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not CLAIM_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        claim = cells[0] if cells else "?"
        # Defense in depth: skip anything whose second cell is the word "Status".
        if len(cells) > 1 and cells[1].lower() == "status":
            continue
        tags = TAG_RE.findall(line)
        if not tags:
            defects.append((n, claim, "no [source/status] tag"))
            continue
        if any(src == "t" and status == "proved" for src, status in tags):
            if not ADMISSION_RE.search(line):
                defects.append((n, claim,
                                "[t/proved] without admission clause (Axiom 22)"))
    return defects


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="vault/catalytic_barrier/VAULT.md")
    a = ap.parse_args(argv)
    path = Path(a.path)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    defects = lint(path)
    if not defects:
        print(f"ok: {path} — every claim carries a valid tag")
        return 0
    for n, claim, defect in defects:
        print(f"  line {n}: {claim}: {defect}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    _argv = sys.argv[1:] if sys.argv and sys.argv[0].endswith(".py") else []
    sys.exit(main(_argv))
