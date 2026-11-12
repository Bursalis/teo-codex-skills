#!/usr/bin/env python3
"""Dependency-free quality checks for Rights and Inequalities deliverables.

Reads DOCX/PPTX OOXML packages with Python's standard library. It does not
replace source verification, template rendering, or visual inspection.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W, "p": P, "a": A, "rel": REL, "r": R}
VOWELS = set("αεηιουωΑΕΗΙΟΥΩ")
WORDS = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
LAYOUTS = {
    "Title", "Section Header", "Content", "Content with Picture 3",
    "Content with Picture 4", "Content with Picture 12",
}
PICTURE_LAYOUTS = {"Content with Picture 3", "Content with Picture 4",
                   "Content with Picture 12"}
BIBLIOGRAPHIC_NOTE_MARKER = re.compile(
    r"(?:Τεκμηρίωση\s*:|\bAPA\b|\b(?:σσ?|σελ(?:\.|ίδα|ίδες)?)\s*\.?\s*\d|\bpp?\.?\s*\d|\([^()]{1,80},\s*(?:19|20)\d{2}[a-z]?\))",
    re.IGNORECASE,
)
PICTURE_BRIEF_TYPES = ("φωτογραφ", "χαρτ", "διαγραμμ", "γραφημ", "σχημα",
                       "σχεδιαγραμμ", "εικονο", "αεροφωτογραφ", "οπτικοποι")
PICTURE_BRIEF_RELATIONS = ("δειχν", "αναδεικν", "απεικον", "συγκρ", "συνδε",
                           "εξηγ", "χαρτογραφ", "διακριν", "οπτικοποι")
GENERIC_PICTURE_BRIEF_PHRASES = ("παραμενει κεν", "δεν υπαρχει", "δεν παρεχ",
                                 "δεν βρεθ", "δεν διαθετ", "χωρις εικον")
def q(local: str, ns: str) -> str:
    return f"{{{ns}}}{local}"


def xml_part(z: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(z.read(name))
    except (KeyError, ET.ParseError):
        return None


def text_of(node: ET.Element, tag: str) -> str:
    return "".join(el.text or "" for el in node.iter(tag))


def word_count(text: str) -> int:
    return len(WORDS.findall(text))


def normalise_prose_paragraph(text: str) -> str:
    """Normalise substantive prose for exact duplicate detection."""
    text = unicodedata.normalize("NFC", text).casefold()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def substantive_sentences(text: str) -> list[str]:
    """Return normalised non-trivial sentences for summary-integrity checks."""
    parts = re.split(r"(?<=[.!?;])\s+", text)
    return [normalise_prose_paragraph(part) for part in parts
            if word_count(normalise_prose_paragraph(part)) >= 12]


NEGATIVE_CONSTRUCTION = re.compile(
    r"\b(?:δεν\s+(?:είναι|σημαίνει|δηλώνει|ζητ(?:ά|ουν)|αρκεί|βρίσκεται|παρουσιάζεται|αποτελεί)|"
    r"το\s+πρόβλημα\s+δεν\s+είναι|όχι\s+μόνο|δεν\s+[^.?!;]{1,80}\s+αλλά)\b",
    flags=re.IGNORECASE,
)


def negative_construction_candidates(paragraphs: list[tuple[int, str]]) -> list[dict[str, Any]]:
    """Return candidates for mandatory manual negative-construction review.

    The checker intentionally does not decide whether a negative clause is
    analytically necessary; that decision requires source- and argument-aware
    human review under the skill's hard gate.
    """
    found: list[dict[str, Any]] = []
    for index, value in paragraphs:
        for sentence in re.split(r"(?<=[.!?;])\s+", value):
            if NEGATIVE_CONSTRUCTION.search(sentence):
                found.append({"paragraph": index, "sentence": sentence.strip()})
    return found


def strip_greek_tonos(text: str, *, all_caps_box: bool) -> str:
    """Strip tonos; in all-caps boxes strip lowercase and uppercase Greek tonos.

    Combining diaeresis is preserved. In ordinary boxes only uppercase Greek
    vowel tonos is removed, matching the course-wide heading rule.
    """
    out: list[str] = []
    base = ""
    for char in unicodedata.normalize("NFD", text):
        if char == "\u0301" and base in VOWELS and (all_caps_box or base.isupper()):
            continue
        out.append(char)
        if not unicodedata.combining(char):
            base = char
    return unicodedata.normalize("NFC", "".join(out))


def tonos_positions(text: str, *, all_caps_box: bool) -> list[int]:
    positions: list[int] = []
    base = ""
    for i, char in enumerate(unicodedata.normalize("NFD", text)):
        if char == "\u0301" and base in VOWELS and (all_caps_box or base.isupper()):
            positions.append(i)
        if not unicodedata.combining(char):
            base = char
    return positions


def safe_title(title: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", title)
    value = re.sub(r"-{2,}", "-", value)
    value = re.sub(r"\s*-\s*", " - ", value).strip()
    value = value.rstrip(" .")
    if value.split(".")[0].upper() in {
        "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        value = "_" + value
    return value


def docx_paragraphs(path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(path) as z:
        root = xml_part(z, "word/document.xml")
        if root is None:
            raise ValueError(f"Δεν διαβάζεται το DOCX: {path}")
        styles_root = xml_part(z, "word/styles.xml")
        styles: dict[str, str] = {}
        if styles_root is not None:
            for style in styles_root.findall(".//w:style", NS):
                sid = style.get(q("styleId", W), "")
                name = style.find("w:name", NS)
                if sid:
                    styles[sid] = name.get(q("val", W), sid) if name is not None else sid
        result = []
        for p in root.findall(".//w:body/w:p", NS):
            node = p.find("w:pPr/w:pStyle", NS)
            sid = node.get(q("val", W), "") if node is not None else ""
            result.append((styles.get(sid, sid), text_of(p, q("t", W))))
        return result


def audit_docx(path: Path, kind: str) -> list[dict[str, Any]]:
    paras = docx_paragraphs(path)
    out: list[dict[str, Any]] = []
    if kind == "lecture":
        prose: list[str] = []
        substantive: list[tuple[int, str]] = []
        found_bib = False
        for index, (style, value) in enumerate(paras):
            if value.strip().casefold() == "βιβλιογραφία":
                found_bib = True
                break
            prose.append(value)
            if (style.casefold().replace(" ", "") not in {"title", "heading1", "heading2", "heading3"}
                    and word_count(value) >= 20):
                substantive.append((index + 1, value))
        count = word_count(" ".join(prose))
        seen: dict[str, list[int]] = {}
        for index, value in substantive:
            key = normalise_prose_paragraph(value)
            if key:
                seen.setdefault(key, []).append(index)
        duplicates = [locations for locations in seen.values() if len(locations) > 1]
        out += [
            {"check": "lecture_prose_words_3600_4400", "value": count,
             "pass": found_bib and 3600 <= count <= 4400},
            {"check": "bibliography_heading_found", "value": found_bib, "pass": found_bib},
            {"check": "lecture_duplicate_substantive_paragraphs", "value": duplicates,
             "pass": not duplicates},
            {"check": "lecture_negative_construction_candidates_manual_review_required",
             "value": negative_construction_candidates(substantive),
             "pass": True, "manual_review_required": True},
        ]
    elif kind == "summaries":
        entries: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        for style, value in paras:
            if style.casefold().replace(" ", "") == "heading3":
                if current is not None:
                    entries.append(current)
                current = {"heading": value, "body": []}
            elif current is not None:
                current["body"].append(value)
        if current is not None:
            entries.append(current)
        paragraph_seen: dict[str, list[str]] = {}
        sentence_seen: dict[str, list[str]] = {}
        for entry in entries:
            count = word_count(" ".join(entry["body"]))
            out.append({"check": "critical_summary_words_270_330", "heading": entry["heading"],
                        "value": count, "pass": 270 <= count <= 330})
            for paragraph in entry["body"]:
                key = normalise_prose_paragraph(paragraph)
                if key and word_count(key) >= 12:
                    paragraph_seen.setdefault(key, []).append(entry["heading"])
                for sentence in substantive_sentences(paragraph):
                    sentence_seen.setdefault(sentence, []).append(entry["heading"])
        paragraph_duplicates = [heads for heads in paragraph_seen.values() if len(heads) > 1]
        sentence_duplicates = [heads for heads in sentence_seen.values() if len(heads) > 1]
        out += [
            {"check": "critical_summary_duplicate_substantive_paragraphs",
             "value": paragraph_duplicates, "pass": not paragraph_duplicates},
            {"check": "critical_summary_duplicate_substantive_sentences",
             "value": sentence_duplicates, "pass": not sentence_duplicates},
        ]
        out.append({"check": "critical_summary_sections_present", "value": len(entries), "pass": bool(entries)})
    return out


def rels(z: zipfile.ZipFile, owner: str) -> list[ET.Element]:
    from posixpath import dirname, basename, join, normpath
    path = join(dirname(owner), "_rels", basename(owner) + ".rels")
    root = xml_part(z, path)
    return list(root) if root is not None else []


def target_path(owner: str, target: str) -> str:
    from posixpath import dirname, normpath
    return target.lstrip("/") if target.startswith("/") else normpath(dirname(owner) + "/" + target)


def related(z: zipfile.ZipFile, owner: str, suffix: str) -> str | None:
    names = set(z.namelist())
    for rel in rels(z, owner):
        if rel.get("Type", "").endswith("/" + suffix):
            path = target_path(owner, rel.get("Target", ""))
            if path in names:
                return path
    return None


def slides(z: zipfile.ZipFile) -> list[str]:
    return sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                  key=lambda s: int(re.search(r"slide(\d+)", s).group(1)))


def layout_name(z: zipfile.ZipFile, slide: str) -> tuple[str | None, str | None]:
    lp = related(z, slide, "slideLayout")
    root = xml_part(z, lp) if lp else None
    cs = root.find("p:cSld", NS) if root is not None else None
    return (cs.get("name") if cs is not None else None, lp)


def placeholder_key(shape: ET.Element) -> tuple[str, str] | None:
    ph = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
    return (ph.get("type", "obj"), ph.get("idx", "0")) if ph is not None else None


def direct_template_spacing_errors(shape: ET.Element) -> list[str]:
    """Detect spacing overrides on a native template placeholder.

    A local font-size reduction can be legitimate only after a rendered
    native-size trial and is documented in the build contract. Spacing is
    never an allowed overflow remedy.
    """
    if placeholder_key(shape) is None:
        return []
    errors: list[str] = []
    for node in shape.iter():
        local = node.tag.rsplit("}", 1)[-1]
        if local in {"spcBef", "spcAft", "lnSpc"}:
            errors.append("paragraph-or-line-spacing override")
    return errors


def caps_values(node: ET.Element | None) -> list[str]:
    if node is None:
        return []
    return [x.get("cap", "") for x in node.iter()
            if x.tag.rsplit("}", 1)[-1] in {"rPr", "defRPr", "endParaRPr"} and x.get("cap")]


def caps_state(node: ET.Element | None) -> bool | None:
    vals = caps_values(node)
    return ("all" in vals) if vals else None


def is_all_caps(z: zipfile.ZipFile, slide: str, shape: ET.Element,
                layout_path: str | None) -> bool:
    state = caps_state(shape)
    key = placeholder_key(shape)
    if state is not None:
        return state
    layout = xml_part(z, layout_path) if layout_path else None
    if layout is not None and key is not None:
        for item in layout.findall(".//p:sp", NS):
            if placeholder_key(item) == key:
                state = caps_state(item)
                if state is not None:
                    return state
    master_path = related(z, layout_path, "slideMaster") if layout_path else None
    master = xml_part(z, master_path) if master_path else None
    if master is not None and key is not None:
        for item in master.findall(".//p:sp", NS):
            if placeholder_key(item) == key:
                state = caps_state(item)
                if state is not None:
                    return state
        ph_type = key[0]
        style_name = ("titleStyle" if ph_type in {"title", "ctrTitle"}
                      else "bodyStyle" if ph_type in {"body", "obj"}
                      else "otherStyle")
        style = master.find(f"p:txStyles/p:{style_name}", NS)
        state = caps_state(style)
        if state is not None:
            return state
    return False


def notes_box_is_all_caps(z: zipfile.ZipFile, notes_path: str,
                          shape: ET.Element) -> bool:
    state = caps_state(shape)
    if state is not None:
        return state
    master_path = related(z, notes_path, "notesMaster")
    master = xml_part(z, master_path) if master_path else None
    key = placeholder_key(shape)
    if master is not None and key is not None:
        for item in master.findall(".//p:sp", NS):
            if placeholder_key(item) == key:
                state = caps_state(item)
                if state is not None:
                    return state
        state = caps_state(master.find("p:txStyles/p:bodyStyle", NS))
        if state is not None:
            return state
    return False


def picture_brief_error(note: str) -> str | None:
    marker = "Εικόνα:"
    if marker not in note:
        return "λείπει η σημείωση Εικόνα:"
    brief = note.split(marker, 1)[1].strip()
    folded = strip_greek_tonos(brief, all_caps_box=True).casefold()
    if len(brief) < 45:
        return "η σημείωση Εικόνα: είναι υπερβολικά σύντομη"
    if any(phrase in folded for phrase in GENERIC_PICTURE_BRIEF_PHRASES):
        return "η σημείωση Εικόνα: δηλώνει μόνο έλλειψη υλικού αντί να προτείνει οπτικό"
    if not any(term in folded for term in PICTURE_BRIEF_TYPES):
        return "η σημείωση Εικόνα: δεν ορίζει είδος οπτικού"
    if not any(term in folded for term in PICTURE_BRIEF_RELATIONS):
        return "η σημείωση Εικόνα: δεν εξηγεί τι θα κάνει ορατό το οπτικό"
    return None


def read_template_layouts(path: Path) -> set[str]:
    with zipfile.ZipFile(path) as z:
        names = set()
        for item in z.namelist():
            if re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", item):
                root = xml_part(z, item)
                cs = root.find("p:cSld", NS) if root is not None else None
                if cs is not None and cs.get("name"):
                    names.add(cs.get("name"))
        return names


def audit_pptx(path: Path, template: Path | None = None,
               expected_total: int | None = None) -> list[dict[str, Any]]:
    errors: list[str] = []
    speaker_note_errors: list[str] = []
    checks: list[dict[str, Any]] = []
    with zipfile.ZipFile(path) as z:
        broken = z.testzip()
        all_slides = slides(z)
        picture = bib = 0
        picture_policy_errors: list[str] = []
        native_picture_placeholder_errors: list[str] = []
        template_spacing_errors: list[str] = []
        bib_slides = 0
        for sp in all_slides:
            root = xml_part(z, sp)
            if root is None:
                errors.append(f"Malformed slide XML: {sp}")
                continue
            lname, layout = layout_name(z, sp)
            if lname not in LAYOUTS:
                errors.append(f"Unapproved or unresolved layout {lname!r}: {sp}")
            if lname == "Content":
                pass
            elif lname in PICTURE_LAYOUTS:
                picture += 1
            slide_text = text_of(root, q("t", A))
            is_bibliography = "βιβλιογραφια" in unicodedata.normalize(
                "NFD", strip_greek_tonos(slide_text, all_caps_box=True)
            ).casefold()
            if is_bibliography:
                bib_slides += 1
            for shape in root.findall(".//p:sp", NS):
                value = text_of(shape, q("t", A))
                key = placeholder_key(shape)
                for spacing_error in direct_template_spacing_errors(shape):
                    message = f"{sp}: {spacing_error} in native template placeholder"
                    errors.append(message)
                    template_spacing_errors.append(message)
                if key and key[0] == "pic" and value.strip():
                    errors.append(f"Text in picture placeholder: {sp}: {value[:80]}")
                if value and tonos_positions(value, all_caps_box=is_all_caps(z, sp, shape, layout)):
                    errors.append(f"Tonos in all-caps-sensitive text: {sp}: {value[:80]}")
            note_path = related(z, sp, "notesSlide")
            note_paragraphs = 0
            if note_path is not None:
                notes_root = xml_part(z, note_path)
                if notes_root is not None:
                    for shape in notes_root.findall(".//p:sp", NS):
                        key = placeholder_key(shape)
                        if not key or key[0] != "body":
                            continue
                        for paragraph in shape.findall(".//a:p", NS):
                            if text_of(paragraph, q("t", A)).strip():
                                note_paragraphs += 1
            substantive_slide = lname not in {"Title", "Section Header"} and not is_bibliography
            if substantive_slide and note_paragraphs == 0:
                speaker_note_errors.append(f"Speaker notes are missing for substantive slide: {sp}")
            if note_paragraphs > 2:
                speaker_note_errors.append(
                    f"Speaker notes exceed two non-empty paragraphs: {sp} ({note_paragraphs})"
                )
            if lname in PICTURE_LAYOUTS:
                native_picture_placeholders = [
                    shape for shape in root.findall(".//p:sp", NS)
                    if (placeholder_key(shape) or (None, None))[0] == "pic"
                ]
                if len(native_picture_placeholders) != 1:
                    message = (f"{sp}: το native picture placeholder του template "
                               f"λείπει ή έχει αντικατασταθεί (βρέθηκαν "
                               f"{len(native_picture_placeholders)}).")
                    errors.append(message)
                    native_picture_placeholder_errors.append(message)
                has_pic = any(e.tag == q("pic", P) for e in root.iter())
                if has_pic:
                    message = f"The skill must not insert an image: {sp}"
                    errors.append(message)
                    picture_policy_errors.append(message)

        checks.extend([
            {"check": "pptx_zip_integrity", "value": broken or "ok", "pass": broken is None},
            {"check": "approved_layouts_and_speaker_notes", "errors": errors,
             "slides": len(all_slides), "pass": not errors},
            {"check": "speaker_notes_quality_structure", "errors": speaker_note_errors,
             "pass": not speaker_note_errors},
            {"check": "exported_total_matches_slide_plan", "value": len(all_slides),
             "expected": expected_total,
             "pass": expected_total is None or len(all_slides) == expected_total},
            {"check": "picture_layouts_empty_for_user_completion",
             "value": {"Content_with_Picture": picture,
                       "policy_errors": picture_policy_errors},
             "pass": not picture_policy_errors},
            {"check": "native_picture_placeholders_preserved",
             "value": native_picture_placeholder_errors,
             "pass": not native_picture_placeholder_errors},
            {"check": "template_spacing_not_overridden",
             "value": template_spacing_errors,
             "pass": not template_spacing_errors},
            {"check": "single_bibliography_slide", "value": bib_slides,
             "pass": bib_slides == 1},
        ])
    if template is not None:
        actual = read_template_layouts(template)
        missing = sorted(LAYOUTS - actual)
        checks.append({"check": "required_template_layouts", "value": sorted(actual & LAYOUTS),
                       "missing": missing, "pass": not missing})
    return checks


def audit_package(directory: Path, unit: str, title: str, template: Path,
                  expected_total: int) -> list[dict[str, Any]]:
    stem = f"ΔΑ - {unit} - {safe_title(title)}"
    files = {
        "summaries": directory / f"{stem} - Κριτικές περιλήψεις βιβλιογραφίας.docx",
        "lecture": directory / f"{stem}.docx",
        "pptx": directory / f"{stem}.pptx",
    }
    checks: list[dict[str, Any]] = []
    for kind, path in files.items():
        exists = path.is_file()
        checks.append({"check": f"deliverable_{kind}_exists", "value": str(path), "pass": exists})
        if exists and kind != "pptx":
            checks.extend(audit_docx(path, kind))
    if files["lecture"].is_file():
        body_titles = [text.strip() for _, text in docx_paragraphs(files["lecture"]) if text.strip()]
        checks.append({"check": "lecture_starts_with_exact_unit_title",
                       "value": body_titles[0] if body_titles else None,
                       "expected": title,
                       "pass": bool(body_titles) and body_titles[0] == title})
    if files["pptx"].is_file():
        checks.extend(audit_pptx(files["pptx"], template, expected_total))
    return checks


def audit_docx_package(directory: Path, unit: str, title: str) -> list[dict[str, Any]]:
    stem = f"ΔΑ - {unit} - {safe_title(title)}"
    files = {
        "summaries": directory / f"{stem} - Κριτικές περιλήψεις βιβλιογραφίας.docx",
        "lecture": directory / f"{stem}.docx",
    }
    checks: list[dict[str, Any]] = []
    for kind, path in files.items():
        exists = path.is_file()
        checks.append({"check": f"deliverable_{kind}_exists", "value": str(path), "pass": exists})
        if exists:
            checks.extend(audit_docx(path, kind))
    if files["lecture"].is_file():
        body_titles = [text.strip() for _, text in docx_paragraphs(files["lecture"]) if text.strip()]
        checks.append({"check": "lecture_starts_with_exact_unit_title",
                       "value": body_titles[0] if body_titles else None,
                       "expected": title,
                       "pass": bool(body_titles) and body_titles[0] == title})
    return checks


def self_test() -> None:
    tests = [
        ("Άνθρωπος, πόλη, μαΐου, ΰ", True, "Ανθρωπος, πολη, μαϊου, ϋ"),
        ("Άνθρωπος, πόλη, μαΐου, ΰ", False, "Ανθρωπος, πόλη, μαΐου, ΰ"),
        ("Α\u0301θήνα", True, "Αθηνα"),
    ]
    for raw, allcaps, expected in tests:
        got = strip_greek_tonos(raw, all_caps_box=allcaps)
        if got != unicodedata.normalize("NFC", expected):
            raise AssertionError(f"tonos normalization failed: {raw!r} -> {got!r}")
    if safe_title("Δικαιώματα: πρόσβαση/ισότητα") != "Δικαιώματα - πρόσβαση - ισότητα":
        raise AssertionError("filename sanitization failed")
    if word_count("Δικαιώματα και ανισότητες: 20–30 διαφάνειες") != 6:
        raise AssertionError("word counter failed")
    print("quality_gate.py self-test: PASS")


def assert_delivery_ready(directory: Path, unit: str, title: str, receipt: Path) -> list[dict[str, Any]]:
    """Confirm that the final DOCX audit passed and a visual-inspection receipt exists."""
    checks = audit_docx_package(directory, unit, title)
    receipt_ok = False
    receipt_error: str | None = None
    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        receipt_ok = (
            payload.get("unit") == str(unit)
            and payload.get("title") == title
            and payload.get("visual_inspection_passed") is True
            and bool(payload.get("summaries_render"))
            and bool(payload.get("lecture_render"))
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        receipt_error = str(exc)
    checks.append({
        "check": "delivery_receipt_with_visual_inspection",
        "value": str(receipt),
        "pass": receipt_ok,
        **({"error": receipt_error} if receipt_error else {}),
    })
    return checks


def main() -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    norm = sub.add_parser("normalize")
    group = norm.add_mutually_exclusive_group(required=True)
    group.add_argument("--all-caps", action="store_true")
    group.add_argument("--ordinary", action="store_true")
    norm.add_argument("--text")
    audit = sub.add_parser("audit")
    audit.add_argument("--directory", required=True, type=Path)
    audit.add_argument("--unit", required=True)
    audit.add_argument("--title", required=True)
    audit.add_argument("--template", required=True, type=Path)
    audit.add_argument("--expected-total", required=True, type=int)
    docx_audit = sub.add_parser("audit-docx")
    docx_audit.add_argument("--directory", required=True, type=Path)
    docx_audit.add_argument("--unit", required=True)
    docx_audit.add_argument("--title", required=True)
    ready = sub.add_parser("assert-delivery-ready")
    ready.add_argument("--directory", required=True, type=Path)
    ready.add_argument("--unit", required=True)
    ready.add_argument("--title", required=True)
    ready.add_argument("--receipt", required=True, type=Path)
    ppt = sub.add_parser("audit-pptx")
    ppt.add_argument("--pptx", required=True, type=Path)
    ppt.add_argument("--template", type=Path)
    ppt.add_argument("--expected-total", type=int)
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            self_test()
            return 0
        if args.command == "normalize":
            value = args.text if args.text is not None else sys.stdin.read()
            print(strip_greek_tonos(value, all_caps_box=args.all_caps), end="")
            return 0
        if args.command == "audit-pptx":
            result = audit_pptx(args.pptx, args.template, args.expected_total)
        elif args.command == "assert-delivery-ready":
            result = assert_delivery_ready(args.directory, args.unit, args.title, args.receipt)
        elif args.command == "audit-docx":
            result = audit_docx_package(args.directory, args.unit, args.title)
        else:
            result = audit_package(args.directory, args.unit, args.title,
                                   args.template, args.expected_total)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if all(x.get("pass", False) for x in result) else 1
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
