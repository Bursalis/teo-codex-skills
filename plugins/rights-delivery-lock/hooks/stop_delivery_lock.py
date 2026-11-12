#!/usr/bin/env python3
"""Fail closed on Stop while an active Rights DOCX/PPTX run lacks proof."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


LOCK_RELATIVE = Path(".codex") / "rights-and-inequalities-delivery-lock.json"


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_lock(cwd: str | None) -> Path | None:
    if not cwd:
        return None
    current = Path(cwd).resolve()
    for candidate_root in (current, *current.parents):
        candidate = candidate_root / LOCK_RELATIVE
        if candidate.is_file():
            return candidate
    return None


def cwd_belongs_to_run(cwd: str | None, lock: dict[str, Any]) -> bool:
    """Scope enforcement to the exact Rights run, never to sibling tasks."""
    run_value = lock.get("run_dir")
    if not cwd or not isinstance(run_value, str) or not run_value:
        return False
    try:
        current = Path(cwd).resolve()
        run_dir = Path(run_value).resolve()
        current.relative_to(run_dir)
        return True
    except (OSError, ValueError, RuntimeError):
        return False


def receipt_is_valid(lock: dict[str, Any]) -> tuple[bool, str]:
    skill = lock.get("skill")
    if skill not in {"dikaiomata-kai-anisotites-docx", "dikaiomata-kai-anisotites-pptx"}:
        return False, "Το lock δεν ανήκει σε έγκυρο skill Δικαιωμάτων και ανισοτήτων."
    if lock.get("state") != "delivery-ready":
        return False, "Ο ενεργός Rights run δεν έχει φτάσει σε κατάσταση delivery-ready."
    receipt_value = lock.get("receipt")
    if not isinstance(receipt_value, str):
        return False, "Δεν υπάρχει διαδρομή delivery receipt στο runtime lock."
    receipt_path = Path(receipt_value)
    if not receipt_path.is_file():
        return False, "Το delivery receipt λείπει."
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, "Το delivery receipt δεν μπορεί να αναγνωστεί."
    if receipt.get("state") != "delivery-ready" or receipt.get("visual_inspection_passed") is not True:
        return False, "Το receipt δεν επιβεβαιώνει περασμένο audit και οπτικό έλεγχο."
    if receipt.get("unit") != lock.get("unit") or receipt.get("title") != lock.get("title"):
        return False, "Το receipt δεν αντιστοιχεί στον κλειδωμένο run."
    deliverables = receipt.get("deliverables")
    expected = {"summaries", "lecture"} if skill.endswith("-docx") else {"pptx"}
    if not isinstance(deliverables, dict) or set(deliverables) != expected:
        return False, "Το receipt δεν περιέχει τα απαιτούμενα παραδοτέα του τρέχοντος skill."
    for item in deliverables.values():
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            return False, "Το receipt περιέχει μη έγκυρη εγγραφή παραδοτέου."
        path = Path(item["path"])
        if not path.is_file() or sha256(path) != item.get("sha256"):
            return False, "Ένα τελικό DOCX λείπει ή άλλαξε μετά το receipt."
    audit = receipt.get("audit")
    if not isinstance(audit, list) or not audit or not all(isinstance(check, dict) and check.get("pass") is True for check in audit):
        return False, "Το receipt δεν περιέχει αποκλειστικά επιτυχημένα quality gates."
    return True, ""


def main() -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        emit({})
        return 0
    lock_path = find_lock(event.get("cwd"))
    if lock_path is None:
        emit({})
        return 0
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        if not cwd_belongs_to_run(event.get("cwd"), lock):
            emit({})
            return 0
        valid, reason = receipt_is_valid(lock)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        valid, reason = False, f"Το runtime lock δεν μπορεί να επαληθευτεί: {exc}"
    if valid:
        emit({})
        return 0
    emit({
        "decision": "block",
        "reason": (
            "Η ολοκλήρωση μπλοκαρίστηκε από το Rights Delivery Lock. "
            f"{reason} Συνέχισε τον τρέχοντα run, διόρθωσε το σχετικό στάδιο, "
            "τρέξε finalise και verify, και μόνο τότε ολοκλήρωσε."
        ),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
