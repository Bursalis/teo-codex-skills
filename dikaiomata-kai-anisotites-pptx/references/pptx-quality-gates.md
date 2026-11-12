# PPTX quality gates

Before final delivery, perform all of the following without waivers:

0. Complete the runtime activation gate and initialise the PPTX run lock before building.
1. Run the template/build-contract feasibility checks and preserve only approved layouts and verified native placeholders.
2. Inspect the exported package: recorded slide total; no substantive speaker notes; approved layouts only; complete APA footer in the dedicated text box; deliberately empty picture placeholders; correct substantive-slide picture-layout ratio; and one alphabetised complete bibliography slide.
3. Run the PPTX audit in the current DOCX skill's `scripts/quality_gate.py` against the current template and expected slide total. A successful deterministic audit does not replace evidence, typography, source-fidelity or visual checks.
4. Render every slide and inspect each at full size. Repair clipping, overlap, broken Greek, unwanted tonos in all-caps text, unreadable type, wrong footer placement, altered template styling, non-empty picture areas, incomplete references and slide/script divergence at the responsible stage, then rerun the affected audit.
5. Write a passing `pptx-audit.json` and exhaustive `visual-review.json` in the run directory. Use `finalize_pptx_delivery.py finalise`, then `verify`; a failed check is a repair signal, never a delivery point.
6. Clean only current-run drafts, render folders, converted templates and test artifacts after a successful final export; preserve sources, templates and final deliverables.

Do not deliver the PPTX until all gates pass.
