# Failure Modes — FM1-FM10

**FM1 — Homonym trap.** Shared word, different object. Check: for every
imported term, name its home field and its field here.

**FM2 — Attribution inflation.** Classical result presented as one's own.
Check: name the source. If it predates you, tag [V/proved].

**FM3 — Triviality disguised as depth.** Check: what is the interesting case?

**FM4 — Residual case overlooked.** Check: enumerate boundary cases.

**FM5 — Paste artifact.** Check: grep the source file.

**FM6 — Forced unification.** Check: if four candidates fail, name the
partition, not the spectrum.

**FM7 — AI hallucination.** Check: for every sentence, ask "would this
survive audit?"

**FM8 — Decontextualized quotation.** Check: state a citation's hypotheses in
the same sentence as its result.

**FM9 — Silent pass on partial coverage.** Check: integrity_report() must
agree with doctor.

**FM10 — Unbound verdict.** Check: every verdict states artifact (A18).

## FM12 — Untracked Build Artifacts

A `.gitignore` that catches some patterns but not others creates the illusion
that the boundary is enforced. Coq's `.aux`, `.glob`, `.vo`, `.vos`, `.vok`,
`.vio` files are build artifacts. The `.aux` format embeds the absolute path
of the source file (`/content/dark-synth/...` on one machine, `/home/...` on
another), so committing it leaks environment paths.

**The critical gotcha:** `.gitignore` only prevents *new* files from being
added. Files already in the index stay tracked until removed with
`git rm --cached`. Adding `*.aux` to `.gitignore` after the fact is a
half-fix — it stops future `.aux` files, but the ones in `git ls-files`
remain.

**Check:** after extending `.gitignore`, run `git ls-files <dir>` and confirm
only source files remain. Anything that's a build artifact requires
`git rm --cached`.

**Why it matters:** `git add .` is the seeking layer. It doesn't know what
a build artifact is. `.gitignore` is the truth layer — it defines what may
enter. A `.gitignore` with gaps is a false boundary (FM11 extended to the
filesystem). And a `.gitignore` without `git rm --cached` is a boundary that
only applies going forward.
