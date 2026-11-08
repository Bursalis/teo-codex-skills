---
name: dikaiomata-kai-anisotites-docx
description: Create or revise the two source-grounded written deliverables—critical summaries and Greek lecture script—for one Rights and Inequalities unit. Use before, never during, the separately authorised PPTX phase.
---

# Δικαιώματα και ανισότητες — γραπτά παραδοτέα

Use this skill for a new unit or a targeted revision of a named written deliverable. It produces only the critical-summaries DOCX and lecture-script DOCX. Route an explicitly approved presentation request to `dikaiomata-kai-anisotites-pptx`.

## Package installation

This skill requires the sibling folder `rights-and-inequalities-common`. Install the package with `install-rights-skills.ps1`, which copies both skills and that common folder together. Before acting, verify that `../rights-and-inequalities-common/core-and-evidence.md` exists; if it does not, report the incomplete installation.

## Mandatory reading order

Before acting, read these instructions in order:

1. [`../rights-and-inequalities-common/core-and-evidence.md`](../rights-and-inequalities-common/core-and-evidence.md) for the project root, authoritative inputs, provenance, evidence boundary, Notion recovery, writing authority and negative-construction gate.
2. [`references/initial-production.md`](references/initial-production.md) for the research, summary, dossier, pedagogical-design and script requirements.
3. [`references/docx-quality-gates.md`](references/docx-quality-gates.md) before finalising or delivering any file.

Read `critical-paper-summary` before drafting a selected reading, `teo-writing-academic` before writing or revising prose, and `documents` before authoring or rendering a DOCX. Those skills govern their respective work; this skill supplies the course-specific constraints.

## Routing

- **New unit:** follow every stage in `initial-production.md` in order. Deliver only the two validated DOCX files, then stop for the user's review.
- **Targeted written revision:** open only the named artifact, the directly relevant bibliography-selected sources, and the applicable parts of the references. Regenerate a downstream written file only when the user explicitly requests it; otherwise state the resulting consistency implication.
- **Missing source, template, active root or usable Notion access:** use the recovery process in the common reference. Report the precise blocker only after it fails; never substitute a prior deliverable, memory or unapproved source.

## Completion boundary

For a new unit, create a unique run directory outside `[Παραδοτέα]`. Initialise it with `scripts/finalize_delivery.py init-run` and `--lock-state <working-root>/.codex/rights-and-inequalities-delivery-lock.json`; this activates the runtime delivery lock. Write candidates only to its `candidates/` folder. Rendered pages and the visual-review record also belong only in that run directory. `[Παραδοτέα]` receives the two DOCX files only when `scripts/finalize_delivery.py finalise` promotes candidates after all checks pass; pass the same `--lock-state` path to that command. Retain no temporary artifacts in `[Παραδοτέα]`.

## Non-negotiable repair loop

A failed quality gate is never a delivery point, a hand-off point, or a reason to ask the user whether to continue. It is a repair signal: identify the failing artifact and criterion, return to the applicable verified source material and internal plan, make the required substantive correction, and rerun every affected gate. Repeat until all applicable gates pass before describing any file as final or asking for review.

Revise each failed summary, section or script as its own source-bound case. It is prohibited to add a shared paragraph, lightly varied boilerplate, template expansion, automated loop, repeated transition or other reusable prose across readings to raise word counts. Added prose is permissible only when it makes a distinct, verified analytical contribution to that specific reading or argument-dossier move. Do not treat the completion rule as overriding system safety, user authorisation, or a genuine absence of required source material; those constraints remain binding.

## Delivery lock for a new-unit run

For a new unit, a final user-facing response is permitted only after the run reaches the `delivery-ready` state below. Commentary may report meaningful progress, but it must never be used as a substitute for delivery and the final response must never contain a progress report, a plan, an invitation to continue, or a statement that the deliverables remain incomplete.

`research → validated summaries → evidence map → argument dossier → pedagogical design → validated script → rendered DOCX files → delivery-ready`

The run reaches `delivery-ready` only when `scripts/finalize_delivery.py finalise` creates `delivery-receipt.json` for the current run and changes its matching runtime lock to `delivery-ready`. That command succeeds only when all of the following are true:

1. the two required DOCX candidates exist in the current run's staging folder;
2. the candidate `audit-docx` has passed every applicable check;
3. every rendered page is present under the current run's render folders and an associated visual-review record identifies them;
4. the visual-review record confirms every page was inspected and passed; and
5. the promoted final files, their hashes, audit output and render hashes are written to the current run's receipt.

Immediately before the final user-facing response, run `scripts/finalize_delivery.py verify` against that receipt. If any item is absent or fails, continue the current run from the affected stage. Do not emit a final response. The sole exception is an actual system-safety, authorisation or external-state constraint that makes further work impossible; report that precise constraint rather than describing the run as complete.

When the companion `rights-delivery-lock` plugin is installed and trusted, its Codex `Stop` hook enforces this boundary at runtime: an active or invalid lock blocks the turn and continues the run. Do not delete, move or manually edit the lock-state file. A user who explicitly abandons a run may remove the state file themselves; this skill does not provide an automated bypass.
