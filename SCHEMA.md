# Record Format — dark-synth-record/v1

One JSON object per line, canonical form (sorted keys, no whitespace, UTF-8).

## Envelope

| field | meaning |
|---|---|
| format | always `dark-synth-record/v1` |
| seq | position from 0, no gaps |
| kind | vault, claim, attempt, verdict, annotation |
| at | UTC, YYYY-MM-DDTHH:MM:SSZ |
| data | kind-specific fields |
| prev | hash of the entry before |
| hash | sha256 of canonical entry without hash |

`hash` covers `prev`. Editing, deleting, or reordering any entry breaks every
hash after it.

## Kinds

- **vault**: vault_id, domain, charter_version
- **claim**: vault_id, claim_id, source, status, artifact, track, scope,
  admission (required for [t/proved]), statement, provenance
- **attempt**: vault_id, claim_id, method, input_sha256, result, signal
- **verdict**: vault_id, claim_id, verdict, code (PQV000-PQV103), binding,
  scope, source_of_verdict
- **annotation**: target {seq, hash}, label (unsound/superseded/retracted/note),
  reason, by

## Verify

Envelope present. seq runs 0..n-1. prev matches. hash matches. claim names a
vault. attempt and verdict name a claim of the same vault. [t/proved] claims
carry admission. annotation targets an earlier entry by exact hash.
Verification is linear in record length.
