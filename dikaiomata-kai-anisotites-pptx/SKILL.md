---
name: dikaiomata-kai-anisotites-pptx
description: Build and validate the final Rights and Inequalities PowerPoint only after the user has reviewed and explicitly authorised it from the critical summaries and lecture script of the current unit run.
---

# Δικαιώματα και ανισότητες — PPTX

Use this skill only when the user explicitly asks for the PowerPoint after reviewing the two written deliverables from the current run. It creates only the editable PPTX. It does not recreate, revise or silently replace the summaries or script.

## Package installation

This skill requires the sibling folder `rights-and-inequalities-common`. Install the package with `install-rights-skills.ps1`, which copies both skills and that common folder together. Before acting, verify that `../rights-and-inequalities-common/core-and-evidence.md` exists; if it does not, report the incomplete installation.

## Mandatory reading order

Before acting, read:

1. [`../rights-and-inequalities-common/core-and-evidence.md`](../rights-and-inequalities-common/core-and-evidence.md) for project-root verification, authoritative inputs, evidence boundaries, provenance and academic-writing rules.
2. [`references/pptx-production.md`](references/pptx-production.md) for the reviewed-input gate, fresh slide plan, template contracts and construction rules.
3. [`references/pptx-quality-gates.md`](references/pptx-quality-gates.md) before export or delivery.
4. [`../dikaiomata-kai-anisotites-docx/references/runtime-activation.md`](../dikaiomata-kai-anisotites-docx/references/runtime-activation.md) before every PPTX run. Apply its runtime activation and scoped delivery-lock rules to this skill as well.

Read `teo-writing-academic` before preparing slide text and `presentations` before inspecting or building the deck. The current reviewed final script is the sole source of slide claims and wording; the summaries check analytical fidelity only.

## Routing

- Confirm the exact reviewed versions of the two written deliverables and record them internally before slide planning.
- If the user asks to change a written deliverable instead, route the change to `dikaiomata-kai-anisotites-docx`; do not make the PPTX from inconsistent inputs.
- If an essential template, source verification or build-contract check fails, repair the earliest responsible stage. Never reuse an earlier deck as a shortcut.

## Completion boundary

Before building, initialise a PPTX run-bound lock with `scripts/finalize_pptx_delivery.py init-run --lock-state <working-root>/.codex/rights-and-inequalities-delivery-lock.json`. Write the candidate deck, audit report and visual-review record only inside that run. Export only the validated PPTX to `[Παραδοτέα]` through `finalize_pptx_delivery.py finalise`; then run `verify` against the receipt. Do not provide a final response until the receipt is valid and the lock is `delivery-ready`. Never create notes, search for or add images, alter picture-placeholder geometry, or expose intermediate decks.
