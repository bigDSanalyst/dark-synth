# Dark Synth Charter — Version 7.1

Signed by the owner's Ed25519 key. A change requires a signed bump.

## The Twenty-Four Axioms

### Epistemic (A1-A9)

A1. Nothing is a theorem until it is proved.
A2. Every bridge is a conjecture until it carries weight. Homonyms are not isomorphisms.
A3. The audit is the work. 10x the generation cost, minimum.
A4. Every claim carries a tag. Two-axis: `[source/status]`.
A5. Attribution is non-negotiable. Citation is not discovery.
A6. An adversary closes every residual case.
A7. Don't force unification. When four formulas fail, name the dichotomy.
A8. Audit the source, not the paste.
A9. Verify external claims before merging. Recompile from scratch.

### Procedural (A10-A17)

A10. The Highlander protocol: publish and stop.
A11. The AI proposes; the auditor disposes.
A12. The frontier is the honest output.
A13. Mutation-test the audit trail.
A14. A green check must never lie.
A15. Never soften a guard to make it pass.
A16. Scope the claim to what was measured.
A17. Pre-register before execution.

### Binding and Coverage (A18-A21)

A18. Binding is recorded independently of the verdict. Modes:
     `artifact: none`, `artifact: prose`, `artifact: sha256 <hash>`.
A19. Scope is part of the claim. Every verdict carries a `track`.
A20. Coverage is a field, not a caveat.
A21. A run that did not verify does not pass the gate.

### Non-Reciprocity and Verification (A22-A24)

A22. The truth layer is non-reciprocal. A hand proof is a *proposal* until
     kernel-accepted or admitted by a signed clause of this charter.
A23. A signature verified only against its own file is not verified.
     Verification requires a pin held outside the verified artifact.
A24. Coverage drift is a signal.

## Hand-proof Admission v1

A claim with `source: t`, `status: proved`, `artifact: prose` is admitted as
truth only if it carries `admission: hand-proved-charter-v1` and:

1. Scope is stated (A19).
2. Every supporting lemma has a mutation test or `[hand-audit-only]` reason (A13).
3. Kernel-accepted contradictions take priority (A22).

## Version History

v1-v6 (see git log).
v7 - A22 (non-reciprocity); Hand-proof Admission v1.
v7.1 - A23 (external pin); A24 (coverage drift).
