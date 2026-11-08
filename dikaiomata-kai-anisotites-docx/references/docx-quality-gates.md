# DOCX quality gates

Apply these gates before delivery.

1. Run `scripts/quality_gate.py self-test` at the beginning of a new unit run.
2. Render and inspect the critical-summaries DOCX before creating the argument dossier. Confirm one Heading 3 for each selected individual reading, 270–330 body words per reading, verified APA headings, and passed duplicate-paragraph, duplicate-sentence and sentence-by-sentence source-fidelity audits.
3. Before finalising the lecture, verify that lecture prose alone is 3,600–4,400 words; every source-dependent claim has a page-verified citation; the bibliography exactly matches the citations; and duplicate-prose and semantic-structure audits pass. Redesign the dossier and draft a new script if its analytical structure or word range fails.
4. At the start, initialise a unique run directory outside `[Παραδοτέα]` with `finalize_delivery.py init-run`. Write only candidates to `<run>/candidates`, and run `quality_gate.py audit-docx --directory <run>/candidates --unit <αριθμός> --title <τίτλος>`. Treat every failed check as a repair signal, never as a delivery or hand-off point. Identify the affected artifact and requirement, revise it substantively from its verified source material and, where applicable, its argument dossier, then rerun every affected gate. Repeat until every applicable check passes.
5. Render and inspect every page of both final DOCX files. Confirm the required templates, filenames, source scope and negative-construction audit.

Keep only current-run final deliverables in `[Παραδοτέα]`. Move only clearly identified temporary artifacts from the current run to the Recycle Bin.

### Required repair discipline

Repair a failed critical summary one reading at a time. Reopen that reading's complete selected material and replace its synthesis with a fresh source-bound account; then rerun the complete per-reading integrity audit. It is prohibited to append or insert a paragraph shared across summaries, including a paragraph with superficial changes to an author name, title or example. Never use boilerplate, reusable closures, automated expansion, repetition, generic transitions or any other filler to manipulate word counts.

Repair a failed lecture by returning to the argument dossier and the page-verified sources for the particular section that fails. Rebuild the relevant analytical move and rewrite the script as required by `initial-production.md`; do not patch it with generic prose, repeated exposition or a common paragraph recycled from the summaries. A document is eligible for delivery only after every applicable automated, manual source-fidelity, semantic-structure and visual-rendering gate has passed.

## Delivery receipt and response lock

After the final visual inspection, write `<run>/visual-review.json` with the run ID, `visual_inspection_passed: true` and exhaustive relative PNG page lists for both `renders/summaries` and `renders/lecture`. Do not hand-write a delivery receipt. Run:

`finalize_delivery.py finalise --run-dir <run> --deliverables <Παραδοτέα> --unit <αριθμός> --title <τίτλος>`

The command reruns the candidate audit, verifies the visual-review inventory, refuses to overwrite a different existing final file, promotes only matching candidates and creates `<run>/delivery-receipt.json` with hashes of final files and renders. Do not send a final user-facing response until this receipt exists and the following verification passes:

`finalize_delivery.py verify --receipt <run>/delivery-receipt.json --unit <αριθμός> --title <τίτλος>`

Its successful exit is necessary, but not sufficient by itself: the final response must cite the two actual promoted files and state that the final audit and visual inspection passed.
