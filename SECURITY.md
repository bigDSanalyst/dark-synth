# Security Policy

## Threat model

1. **Owner key compromise.** The charter's Ed25519 key binds every admission
   decision. Mitigation: hardware custody; yearly re-sign; record signing
   events in charter/charter_history.jsonl.

2. **Compiler compromise.** A [run] claim rests on Coq/Lean accepting the
   file. Mitigation: pin versions; record binary hashes; cross-verify where
   load-bearing.

3. **Record-chain tampering.** The prev-hash chain is forward-consistent.
   Mitigation: git commit signing; branch protection; OTS on the chain head.

4. **Charter signer drift.** Mitigation: the signers list is itself signed.

5. **Paste artifact injection** (Axiom 8). Mitigation: tools read files,
   not rendered messages.

6. **Downstream consumer compromise.** Out of scope.

## Cryptographic inventory

- Records hash chain: SHA-256 (safe)
- Coq file hashes: SHA-256 (safe)
- Charter signing: Ed25519 (quantum-vulnerable; upgrade path required)
- Chain-head timestamping: OTS (SHA-256 + Bitcoin ECDSA)

## The owner fingerprint (external pin, Axiom 23)

The charter's signing fingerprint must appear here, not only in the charter:

    fcaeefdf692d364c6d060a063d5794d1bece860350f17e00dfa1bdfe103f6f57

If the fingerprint in charter/charter.yaml diverges from this one, the charter
has been re-signed with a different key and the divergence is a finding.

## The security guarantee

Axiom 22 (non-reciprocity) is the security property. A compromised seeking
layer can propose, but cannot admit.

## Reporting

Report vulnerabilities via GitHub security advisories, or contact the
maintainer directly. Do not open public issues for vulnerabilities.
