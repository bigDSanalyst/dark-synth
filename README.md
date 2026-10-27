# Dark Synth

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PENDING.svg)](https://doi.org/10.5281/zenodo.PENDING)

A tag-audited methodology for mathematical work. Every claim carries
`[source/status]`; every correction is logged; every `[run]` claim is
kernel-accepted with a sha256; the audit trail is tested against its own
mutants.

## What it is

- **Tag taxonomy** (`docs/TAGS.md`): `[V]` classical, `[A]` architectural,
  `[P]` patch, `[t]` derived, `[run]` executed.
- **6-phase scaffold** (`SCAFFOLD.md`).
- **10 failure modes** (`FAILURE_MODES.md`).
- **Signed charter** (`charter/charter.yaml`).
- **Three record organs**: `vault/`, `audits/`, `charter/`.
- **Tool suite** (`tools/`): ledger, kernel check, witness, mutation test, doctor.

## What it is not

- Not a proof assistant. Coq and Lean do the checking; Dark Synth records
  what they accepted.
- Not an agent runtime. Proventhru, oscillate, Dharmapala, AetherShell,
  syndicate-genesis are methodology siblings, not mathematical relatives.
- Not finished. The methodology is stable; the first vault is the test case.

## Quick start

    python3 tools/doctor.py --repo .
    python3 tools/tag_lint.py
    python3 tools/mutation_test.py
    python3 -m pytest tests/ -v

## The vault

`vault/catalytic_barrier/` — a barrier on interpolation-based catalytic
algorithms (Theorem 3.6), verified by Coq for the adversary identity
(`coq/adversary.v`) and a worked example (`coq/k2m2.v`). The
`audits/catalytic_barrier/` drawer records every correction (A1-A5), with a
mutation matrix naming which corrections the test suite defends and which are
hand-audit-only.

## License

- **Code**: MIT — see `LICENSE`
- **Content** (docs, prose, paper text): CC BY 4.0 — see `LICENSE-CONTENT.md`
