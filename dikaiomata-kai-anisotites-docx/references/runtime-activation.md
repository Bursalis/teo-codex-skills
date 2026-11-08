# Runtime activation and per-run preflight

This procedure is mandatory before every execution of the DOCX skill. It is separate from the content quality gates. Its purpose is to prove that the runtime can block completion before production begins.

## One-time installation and trust

The operator must complete these steps after installing or updating the skill, and whenever the Codex application or configuration is reset:

1. Confirm that the `rights-delivery-lock` plugin is installed and enabled from the trusted repository.
2. Confirm that `C:\Users\tkary\.codex\hooks.json` exists and contains the user-level `Stop` hook, or that an equivalent managed hook is active.
3. Fully quit and reopen Codex. Opening a new chat without restarting after a hook or plugin change is not sufficient evidence that the runtime loaded the new definition.
4. In the new local Codex session, open Settings → Hooks or run `/hooks`. Confirm that the Rights delivery-lock `Stop` hook is listed and marked trusted/enabled.
5. Run a harmless canary with an active lock and no delivery receipt. The session must be blocked from ending and must continue the run. A terminal-only invocation of the Python hook is not enough: the canary must pass through the Codex runtime.

If Settings → Hooks reports `No hooks found`, if the hook is untrusted, or if the canary is not observed, activation has failed. Do not initialise a production run. Do not create candidates or provide a progress-style final response. Resolve the runtime configuration and repeat this procedure.

## Mandatory preflight on every run

At the beginning of every new-unit run and every targeted revision:

1. Verify that the current session is local Codex, not a cloud-orchestrated environment where plugin hooks are unavailable.
2. Verify that the trusted/enabled Stop hook is visible in the current session. Do not infer this from the existence of a file on disk.
3. Verify that the current working root contains the expected `.codex` location for the delivery-lock state.
4. Only after the three checks pass, create the isolated run directory and execute `finalize_delivery.py init-run --lock-state <working-root>/.codex/rights-and-inequalities-delivery-lock.json`.

The model must treat the live hook listing and canary result as runtime evidence. A static configuration file, a successfully imported Python module, or a manually executed hook script cannot substitute for that evidence.

## Failure handling

Activation failure is the only pre-production stop condition in this procedure. It does not authorise a partial production run, a provisional DOCX, or a claim that the skill completed. Once the gate passes, the ordinary repair loop applies: a failed content or visual quality gate requires substantive repair and repetition until every gate passes, followed by `finalise` and `verify`.

For a true hard guarantee across sessions and users, an administrator must deploy the hook as a managed hook through the applicable Codex policy/MDM configuration. A user-level hook is enforceable only after it is loaded, trusted and verified by the live canary.
