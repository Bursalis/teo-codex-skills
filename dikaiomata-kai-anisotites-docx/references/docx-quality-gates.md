# DOCX quality gates

Apply these gates before delivery.

1. Run `scripts/quality_gate.py self-test` at the beginning of a new unit run.
2. Render and inspect the critical-summaries DOCX before creating the argument dossier. Confirm one Heading 3 for each selected individual reading, 270–330 body words per reading, verified APA headings, and passed duplicate-paragraph, duplicate-sentence and sentence-by-sentence source-fidelity audits.
3. Before finalising the lecture, verify that lecture prose alone is 3,600–4,400 words; every source-dependent claim has a page-verified citation; the bibliography exactly matches the citations; and duplicate-prose and semantic-structure audits pass. Redesign the dossier and draft a new script if its analytical structure or word range fails.
4. Run `quality_gate.py audit-docx --directory <Παραδοτέα> --unit <αριθμός> --title <τίτλος>` after both DOCX files exist. Treat every failed check as a repair signal.
5. Render and inspect every page of both final DOCX files. Confirm the required templates, filenames, source scope and negative-construction audit.

Keep only current-run final deliverables in `[Παραδοτέα]`. Move only clearly identified temporary artifacts from the current run to the Recycle Bin.
