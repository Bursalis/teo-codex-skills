#!/usr/bin/env python3
"""Create and verify a run-bound receipt before promoting DOCX candidates.

Candidates stay in <run-dir>/candidates until this script verifies the DOCX
quality audit and the reviewed render inventory. Only then are they copied to
the final deliverables directory and recorded in delivery-receipt.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import quality_gate


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_files(directory: Path, unit: str, title: str) -> dict[str, Path]:
    stem = f"ΔΑ - {unit} - {quality_gate.safe_title(title)}"
    return {
        "summaries": directory / f"{stem} - Κριτικές περιλήψεις βιβλιογραφίας.docx",
        "lecture": directory / f"{stem}.docx",
    }


def write_lock_state(lock_state: Path, *, state: str, run_dir: Path, unit: str, title: str,
                     receipt: Path | None = None) -> None:
    value: dict[str, Any] = {
        "schema_version": 1,
        "skill": "dikaiomata-kai-anisotites-docx",
        "state": state,
        "run_dir": str(run_dir.resolve()),
        "unit": str(unit),
        "title": title,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if receipt is not None:
        value["receipt"] = str(receipt.resolve())
    write_json(lock_state.resolve(), value)


def require_active_lock(lock_state: Path, run_dir: Path, unit: str, title: str) -> None:
    state = json.loads(lock_state.resolve().read_text(encoding="utf-8"))
    if (
        state.get("skill") != "dikaiomata-kai-anisotites-docx"
        or state.get("state") != "active"
        or Path(state.get("run_dir", "")).resolve() != run_dir.resolve()
        or state.get("unit") != str(unit)
        or state.get("title") != title
    ):
        raise ValueError("Το ενεργό delivery lock δεν αντιστοιχεί στον τρέχοντα run.")


def init_run(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        raise ValueError(f"Το run directory δεν είναι κενό: {run_dir}")
    (run_dir / "candidates").mkdir(parents=True, exist_ok=False)
    (run_dir / "renders" / "summaries").mkdir(parents=True)
    (run_dir / "renders" / "lecture").mkdir(parents=True)
    manifest = {
        "run_id": str(uuid.uuid4()),
        "unit": str(args.unit),
        "title": args.title,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "state": "staging",
    }
    write_json(run_dir / "run.json", manifest)
    write_lock_state(args.lock_state, state="active", run_dir=run_dir, unit=args.unit, title=args.title)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def reviewed_render_inventory(run_dir: Path, run: dict[str, Any]) -> dict[str, list[Path]]:
    review_path = run_dir / "visual-review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("run_id") != run["run_id"] or review.get("visual_inspection_passed") is not True:
        raise ValueError("Το visual-review.json δεν επιβεβαιώνει τον τρέχοντα run ή τον οπτικό έλεγχο.")
    inventory: dict[str, list[Path]] = {}
    for kind in ("summaries", "lecture"):
        listed = review.get(f"{kind}_pages")
        if not isinstance(listed, list) or not listed:
            raise ValueError(f"Λείπει η λίστα σελίδων rendering για {kind}.")
        paths = [(run_dir / item).resolve() for item in listed]
        root = (run_dir / "renders" / kind).resolve()
        if any(not path.is_file() or root not in path.parents for path in paths):
            raise ValueError(f"Μη έγκυρο ή απόν render output για {kind}.")
        inventory[kind] = paths
    return inventory


def finalise(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    run_path = run_dir / "run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    if run.get("unit") != str(args.unit) or run.get("title") != args.title:
        raise ValueError("Το run.json δεν αντιστοιχεί στην ενότητα ή στον τίτλο της εντολής.")
    require_active_lock(args.lock_state, run_dir, args.unit, args.title)
    candidates = expected_files(run_dir / "candidates", args.unit, args.title)
    if not all(path.is_file() for path in candidates.values()):
        raise ValueError("Λείπει υποψήφιο DOCX από το staging directory.")
    audit = quality_gate.audit_docx_package(run_dir / "candidates", args.unit, args.title)
    if not all(check.get("pass", False) for check in audit):
        print(json.dumps({"pass": False, "audit": audit}, ensure_ascii=False, indent=2))
        return 1
    renders = reviewed_render_inventory(run_dir, run)
    final_paths = expected_files(args.deliverables.resolve(), args.unit, args.title)
    args.deliverables.mkdir(parents=True, exist_ok=True)
    for kind, target in final_paths.items():
        if target.exists() and sha256(target) != sha256(candidates[kind]):
            raise ValueError(f"Υπάρχει διαφορετικό τελικό αρχείο και δεν θα αντικατασταθεί: {target}")
    for kind, target in final_paths.items():
        if not target.exists():
            shutil.copy2(candidates[kind], target)
    final_audit = quality_gate.audit_docx_package(args.deliverables, args.unit, args.title)
    if not all(check.get("pass", False) for check in final_audit):
        raise ValueError("Ο τελικός audit μετά την προαγωγή απέτυχε.")
    receipt = {
        "run_id": run["run_id"],
        "unit": str(args.unit),
        "title": args.title,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "state": "delivery-ready",
        "deliverables": {kind: {"path": str(path), "sha256": sha256(path)} for kind, path in final_paths.items()},
        "audit": final_audit,
        "renders": {kind: [{"path": str(path), "sha256": sha256(path)} for path in paths] for kind, paths in renders.items()},
        "visual_inspection_passed": True,
    }
    receipt_path = run_dir / "delivery-receipt.json"
    write_json(receipt_path, receipt)
    run["state"] = "delivery-ready"
    run["completed_at"] = receipt["completed_at"]
    write_json(run_path, run)
    write_lock_state(
        args.lock_state,
        state="delivery-ready",
        run_dir=run_dir,
        unit=args.unit,
        title=args.title,
        receipt=receipt_path,
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


def verify(args: argparse.Namespace) -> int:
    receipt_path = args.receipt.resolve()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("state") != "delivery-ready" or receipt.get("visual_inspection_passed") is not True:
        raise ValueError("Το receipt δεν δηλώνει delivery-ready με ολοκληρωμένο οπτικό έλεγχο.")
    if receipt.get("unit") != str(args.unit) or receipt.get("title") != args.title:
        raise ValueError("Το receipt δεν αντιστοιχεί στην αιτούμενη ενότητα.")
    for item in receipt.get("deliverables", {}).values():
        path = Path(item["path"])
        if not path.is_file() or sha256(path) != item.get("sha256"):
            raise ValueError("Ένα τελικό DOCX λείπει ή άλλαξε μετά το receipt.")
    if len(receipt.get("deliverables", {})) != 2:
        raise ValueError("Το receipt δεν περιέχει ακριβώς δύο DOCX παραδοτέα.")
    if not all(check.get("pass", False) for check in receipt.get("audit", [])):
        raise ValueError("Το receipt περιέχει αποτυχημένο quality check.")
    print(json.dumps({"pass": True, "receipt": str(receipt_path), "run_id": receipt["run_id"]}, ensure_ascii=False))
    return 0


def main() -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init-run")
    init.add_argument("--run-dir", required=True, type=Path)
    init.add_argument("--unit", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--lock-state", required=True, type=Path)
    finish = sub.add_parser("finalise")
    finish.add_argument("--run-dir", required=True, type=Path)
    finish.add_argument("--deliverables", required=True, type=Path)
    finish.add_argument("--unit", required=True)
    finish.add_argument("--title", required=True)
    finish.add_argument("--lock-state", required=True, type=Path)
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--receipt", required=True, type=Path)
    verify_parser.add_argument("--unit", required=True)
    verify_parser.add_argument("--title", required=True)
    args = parser.parse_args()
    try:
        return {"init-run": init_run, "finalise": finalise, "verify": verify}[args.command](args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
