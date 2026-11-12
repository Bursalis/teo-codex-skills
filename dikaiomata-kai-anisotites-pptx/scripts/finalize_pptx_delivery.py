#!/usr/bin/env python3
"""Run-bound finalisation and receipt verification for the Rights PPTX skill."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lock(lock_state: Path, state: str, run_dir: Path, unit: str, title: str, receipt: Path | None = None) -> None:
    value: dict[str, Any] = {
        "schema_version": 1,
        "skill": "dikaiomata-kai-anisotites-pptx",
        "state": state,
        "run_dir": str(run_dir.resolve()),
        "unit": str(unit),
        "title": title,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if receipt is not None:
        value["receipt"] = str(receipt.resolve())
    write_json(lock_state.resolve(), value)


def require_active(lock_state: Path, run_dir: Path, unit: str, title: str) -> None:
    value = json.loads(lock_state.resolve().read_text(encoding="utf-8"))
    if value.get("skill") != "dikaiomata-kai-anisotites-pptx" or value.get("state") != "active":
        raise ValueError("Το ενεργό PPTX delivery lock λείπει ή δεν είναι ενεργό.")
    if Path(value.get("run_dir", "")).resolve() != run_dir.resolve() or value.get("unit") != str(unit) or value.get("title") != title:
        raise ValueError("Το ενεργό PPTX delivery lock δεν αντιστοιχεί στον τρέχοντα run.")


def init_run(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        raise ValueError(f"Το run directory δεν είναι κενό: {run_dir}")
    (run_dir / "candidates").mkdir(parents=True, exist_ok=False)
    (run_dir / "renders").mkdir()
    manifest = {"run_id": str(uuid.uuid4()), "unit": str(args.unit), "title": args.title, "state": "staging", "started_at": datetime.now(timezone.utc).isoformat()}
    write_json(run_dir / "run.json", manifest)
    lock(args.lock_state, "active", run_dir, args.unit, args.title)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def finalise(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    if run.get("unit") != str(args.unit) or run.get("title") != args.title:
        raise ValueError("Το run.json δεν αντιστοιχεί στην ενότητα ή στον τίτλο.")
    require_active(args.lock_state, run_dir, args.unit, args.title)
    candidate = args.candidate.resolve()
    if not candidate.is_file() or run_dir not in candidate.parents:
        raise ValueError("Το PPTX candidate πρέπει να βρίσκεται μέσα στο τρέχον run.")
    audit = json.loads(args.audit.resolve().read_text(encoding="utf-8"))
    if not isinstance(audit, list) or not audit or not all(item.get("pass") is True for item in audit if isinstance(item, dict)):
        raise ValueError("Το PPTX audit δεν επιβεβαιώνει ότι όλοι οι έλεγχοι πέρασαν.")
    visual = json.loads(args.visual_review.resolve().read_text(encoding="utf-8"))
    if visual.get("run_id") != run["run_id"] or visual.get("visual_inspection_passed") is not True:
        raise ValueError("Το visual review δεν επιβεβαιώνει τον τρέχοντα run.")
    target = args.deliverables.resolve() / args.filename
    args.deliverables.mkdir(parents=True, exist_ok=True)
    if target.exists() and sha256(target) != sha256(candidate):
        raise ValueError(f"Υπάρχει διαφορετικό τελικό PPTX και δεν θα αντικατασταθεί: {target}")
    if not target.exists():
        shutil.copy2(candidate, target)
    receipt = {"run_id": run["run_id"], "unit": str(args.unit), "title": args.title, "state": "delivery-ready", "completed_at": datetime.now(timezone.utc).isoformat(), "deliverables": {"pptx": {"path": str(target), "sha256": sha256(target)}}, "audit": audit, "visual_inspection_passed": True}
    receipt_path = run_dir / "delivery-receipt.json"
    write_json(receipt_path, receipt)
    run["state"] = "delivery-ready"
    write_json(run_dir / "run.json", run)
    lock(args.lock_state, "delivery-ready", run_dir, args.unit, args.title, receipt_path)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


def verify(args: argparse.Namespace) -> int:
    receipt = json.loads(args.receipt.resolve().read_text(encoding="utf-8"))
    if receipt.get("state") != "delivery-ready" or receipt.get("visual_inspection_passed") is not True or set(receipt.get("deliverables", {})) != {"pptx"}:
        raise ValueError("Το PPTX receipt δεν είναι έγκυρο.")
    if receipt.get("unit") != str(args.unit) or receipt.get("title") != args.title:
        raise ValueError("Το PPTX receipt δεν αντιστοιχεί στον τρέχοντα τίτλο ή unit.")
    item = receipt["deliverables"]["pptx"]
    path = Path(item["path"])
    if not path.is_file() or sha256(path) != item.get("sha256"):
        raise ValueError("Το τελικό PPTX λείπει ή άλλαξε μετά το receipt.")
    if not receipt.get("audit") or not all(check.get("pass") is True for check in receipt["audit"]):
        raise ValueError("Το PPTX receipt περιέχει αποτυχημένο quality gate.")
    print(json.dumps({"pass": True, "receipt": str(args.receipt.resolve()), "run_id": receipt["run_id"]}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init-run")
    init.add_argument("--run-dir", required=True, type=Path); init.add_argument("--unit", required=True); init.add_argument("--title", required=True); init.add_argument("--lock-state", required=True, type=Path)
    finish = sub.add_parser("finalise")
    finish.add_argument("--run-dir", required=True, type=Path); finish.add_argument("--candidate", required=True, type=Path); finish.add_argument("--deliverables", required=True, type=Path); finish.add_argument("--filename", required=True); finish.add_argument("--audit", required=True, type=Path); finish.add_argument("--visual-review", required=True, type=Path); finish.add_argument("--unit", required=True); finish.add_argument("--title", required=True); finish.add_argument("--lock-state", required=True, type=Path)
    check = sub.add_parser("verify")
    check.add_argument("--receipt", required=True, type=Path); check.add_argument("--unit", required=True); check.add_argument("--title", required=True)
    args = parser.parse_args()
    try:
        return {"init-run": init_run, "finalise": finalise, "verify": verify}[args.command](args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
