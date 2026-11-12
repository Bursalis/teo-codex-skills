# Local runtime preflight and per-run lock

This procedure is mandatory before every execution of the DOCX or PPTX skill. It replaces the former external Stop-hook and canary dependency. The internal run-bound lock, candidate audit, finalise step and receipt verification remain mandatory.

## Mandatory preflight on every run

Before reading sources or creating any candidate:

1. Verify that the active project root exists and contains the required `[Πηγές]`, `[Templates]` and `[Παραδοτέα]` directories.
2. Verify that the required local skill scripts, templates and references are available from the installed package.
3. Create a unique isolated run directory outside `[Παραδοτέα]`.
4. Initialise the matching internal run lock before production: use `finalize_delivery.py init-run` for DOCX runs and `finalize_pptx_delivery.py init-run` for PPTX runs, always with `--lock-state <working-root>/.codex/rights-and-inequalities-delivery-lock.json`.
5. Keep candidates, renders, audit outputs and visual-review records inside that run directory. Do not place intermediate files in `[Παραδοτέα]`.

An external plugin, Stop hook, trust setting or live canary is optional and must not be treated as a prerequisite or as evidence required to begin production.

## Failure handling

If the active root, required package resource or internal run-lock initialisation fails, do not begin production. Report the precise local blocker and resolve it before creating candidates. Once the internal lock is active, a failed content, audit or visual gate is a repair signal: repair the responsible stage, rerun every affected check, then use `finalise` and `verify` to establish `delivery-ready`.

The internal receipt is the completion boundary. A final response is permitted only after the current run has a valid delivery receipt, all required audit checks pass, all required renders have been inspected and the matching internal lock is `delivery-ready`.
