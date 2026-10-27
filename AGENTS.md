# AGENTS.md — Operating manual

## The invariant

The truth layer is non-reciprocal (Axiom 22). The truth layer is: the kernel,
the signed charter, the frozen test sets, and the record schema. The seeking
layer is: AI proposals, hand proofs, LLM policies. Nothing in the seeking
layer may shape the truth layer.

If a proposed change would let a model or a search influence what counts as
proof, what counts as a valid record, or what the frozen tests are — stop.

## Rules

R1. Pre-register before measuring.
R2. Certify your own filters.
R3. Classify before you spend.
R4. The evaluator rule: enumerate falsifiers, not easy constructions.
R5. Records are append-only. Corrections are annotations.
R6. Report nulls. A pre-committed inconclusive result is a finding.
R7. Verify external claims. Check a tool exists before citing it.
R8. Report per-phase, not aggregate.
R9. The green check must never lie.
R10. Never soften a guard to make it pass.

## Commands

    python3 tools/doctor.py --json
    python3 tools/tag_lint.py
    python3 tools/mutation_test.py --json
    python3 tools/ledger.py verify vault/catalytic_barrier/records.jsonl
    python3 tools/charter.py verify
    python3 -m pytest tests/ -v

## Do not

- Amend the charter after seeing data from the vault it governs.
- Import a component that touches the kernel, the charter, or the records.
- Rename a null as progress.
- Claim `[t/proved]` without an `admission` clause.
- Cite a tool without checking it exists.
- Report "3 of 5 verified" without naming which three and which two.
