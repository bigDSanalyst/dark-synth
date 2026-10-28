# Dark Synth

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23689103.svg)](https://doi.org/10.5281/zenodo.23689103)

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


### Known local states (`doctor.py`)

- `DEGRADED kernel: no Coq toolchain on PATH` and `DEGRADED coq.*`
  This is not a defect in the repo. It means the local machine does not have
  `coqc` installed. The Coq proofs were verified and recorded in the ledger
  at the time of commit. To flip these to `ok` locally, run
  `apt-get install coq` (or equivalent) and re-run `tools/doctor.py`.
- `LOOK witness_coq_attempts: ['adversary_ring.v']`
  This is an honest record of a tooling limitation: Coq 8.18's abstract
  `ring_theory` omits `x * 0 = 0`, blocking the commutative-ring proof. The
  same theorem is kernel-verified in Lean 4 (`lean/AdversaryRing.lean`).

## License

- **Code**: MIT — see `LICENSE`
- **Content** (docs, prose, paper text): CC BY 4.0 — see `LICENSE-CONTENT.md`
