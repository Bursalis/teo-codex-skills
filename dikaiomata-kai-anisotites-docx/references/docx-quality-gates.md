# DOCX quality gates

Apply the following gates in addition to the detailed production requirements.

1. At the beginning of a new unit run, run `scripts/quality_gate.py self-test`.
2. Before the argument dossier, render and inspect the critical-summaries DOCX; verify one Heading 3 per selected individual reading, 270–330 body words each, verified APA headings, and passed deterministic duplicate paragraph/sentence and manual sentence-by-sentence source-fidelity audits.
3. Before the outline, verify the lecture prose alone is 3,600–4,400 words, every source-dependent claim has a page-verified citation, bibliography entries are complete and exactly match citations, and duplicate-prose plus semantic-structure audits pass. If it is out of range or structurally weak, redesign the dossier and write a new script; never patch it with filler or arbitrary cuts.
4. Before delivery, render and inspect every page of all three DOCX files. Confirm template styles, headings, filenames, source scope, the negative-construction audit and the outline's faithful condensation of the final script.
5. Run `quality_gate.py audit` only for the initial three artifacts; do not create a PPTX or run a four-artifact audit in this phase. Treat a failure as a repair signal and return to the earliest responsible stage.

Keep only final current-run deliverables in `[Παραδοτέα]`. Move only clearly identified temporary artifacts from the current run to the Recycle Bin; never delete user-authored or unclear material.
