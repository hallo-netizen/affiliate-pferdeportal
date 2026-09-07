#!/usr/bin/env python3
"""DESIGN Hobbyraum fail-closed runner.

V1 supports exactly ONE operation: swap two adjacent complete source ranges inside
ONE member of an existing baseline plugin ZIP. No parsing, no rewriting, no CSS
changes, no version bump, no extra file changes.

A candidate is emitted only after positive AND negative checks pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

BLOCKED_EXIT = 23


def blocked(code: str) -> None:
    raise RuntimeError(f"BLOCKED:{code}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_job(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "mode", "baseline_sha256", "target_member_suffix", "encoding",
        "first_start", "second_start", "after_second"
    }
    allowed = required | {"job_id", "description"}
    if set(raw) - allowed:
        blocked("JOB_UNKNOWN_KEYS")
    if required - set(raw):
        blocked("JOB_MISSING_KEYS")
    if raw["mode"] != "swap_two_adjacent_complete_ranges_only":
        blocked("MODE_NOT_ALLOWED")
    for key in ("baseline_sha256", "target_member_suffix", "encoding", "first_start", "second_start", "after_second"):
        if not isinstance(raw[key], str) or not raw[key]:
            blocked(f"JOB_FIELD_INVALID:{key}")
    return raw


def read_zip(path: Path) -> Tuple[List[zipfile.ZipInfo], Dict[str, bytes]]:
    try:
        with zipfile.ZipFile(path, "r") as zf:
            bad = zf.testzip()
            if bad:
                blocked("ZIP_CRC_FAIL:" + bad)
            infos = zf.infolist()
            files = {i.filename: zf.read(i.filename) for i in infos if not i.is_dir()}
            return infos, files
    except zipfile.BadZipFile:
        blocked("BAD_ZIP")


def resolve_target(files: Dict[str, bytes], suffix: str) -> str:
    hits = [name for name in files if name.endswith(suffix)]
    if len(hits) != 1:
        blocked(f"TARGET_MEMBER_COUNT:{len(hits)}")
    return hits[0]


def unique_at(text: str, needle: str, label: str) -> int:
    first = text.find(needle)
    if first < 0:
        blocked(label + "_MISSING")
    if text.find(needle, first + 1) >= 0:
        blocked(label + "_NOT_UNIQUE")
    return first


def exact_swap(source: str, job: dict) -> Tuple[str, str, str]:
    p1 = unique_at(source, job["first_start"], "FIRST_START")
    p2 = unique_at(source, job["second_start"], "SECOND_START")
    p3 = unique_at(source, job["after_second"], "AFTER_SECOND")
    if not (p1 < p2 < p3):
        blocked("SOURCE_ORDER_INVALID")

    first = source[p1:p2]
    second = source[p2:p3]
    if not first.strip() or not second.strip():
        blocked("EMPTY_RANGE")

    candidate = source[:p1] + second + first + source[p3:]
    if candidate == source:
        blocked("NO_CHANGE")
    return candidate, first, second


def clone_zip_with_one_replacement(baseline: Path, output: Path, target: str, target_bytes: bytes) -> None:
    with zipfile.ZipFile(baseline, "r") as zin, zipfile.ZipFile(output, "w") as zout:
        for info in zin.infolist():
            data = b"" if info.is_dir() else (target_bytes if info.filename == target else zin.read(info.filename))
            ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            ni.compress_type = info.compress_type
            ni.comment = info.comment
            ni.extra = info.extra
            ni.internal_attr = info.internal_attr
            ni.external_attr = info.external_attr
            ni.create_system = info.create_system
            ni.flag_bits = info.flag_bits
            zout.writestr(ni, data)


def validate(baseline: Path, candidate: Path, job: dict) -> dict:
    if not baseline.exists():
        blocked("BASELINE_MISSING")
    if sha256_file(baseline).lower() != job["baseline_sha256"].lower():
        blocked("BASELINE_HASH_MISMATCH")

    b_infos, b_files = read_zip(baseline)
    c_infos, c_files = read_zip(candidate)

    b_names = [i.filename for i in b_infos]
    c_names = [i.filename for i in c_infos]
    if b_names != c_names:
        blocked("ARCHIVE_STRUCTURE_CHANGED")

    target = resolve_target(b_files, job["target_member_suffix"])
    if target not in c_files:
        blocked("TARGET_MISSING")

    changed = [name for name in b_files if b_files[name] != c_files[name]]
    if changed != [target]:
        blocked("CHANGED_MEMBER_SET:" + ",".join(changed))

    try:
        b_text = b_files[target].decode(job["encoding"])
        c_text = c_files[target].decode(job["encoding"])
    except UnicodeDecodeError:
        blocked("TARGET_DECODE_FAIL")

    expected, first, second = exact_swap(b_text, job)
    if c_text != expected:
        blocked("NOT_EXACT_TWO_RANGE_SWAP")

    if c_text.count(first) != 1 or c_text.count(second) != 1:
        blocked("RANGE_SINGLETON_FAIL")
    if c_text.find(second) >= c_text.find(first):
        blocked("SWAP_ORDER_FAIL")

    s = c_text.find(second)
    f = c_text.find(first)
    restored = c_text[:s] + first + second + c_text[f + len(first):]
    if restored != b_text:
        blocked("REVERSIBILITY_FAIL")

    return {
        "status": "PASS",
        "baseline_sha256": sha256_file(baseline),
        "candidate_sha256": sha256_file(candidate),
        "archive_members": len(b_names),
        "target_member": target,
        "changed_members": changed,
        "first_range_sha256": sha256_bytes(first.encode(job["encoding"])),
        "second_range_sha256": sha256_bytes(second.encode(job["encoding"])),
        "positive_checks": [
            "BASELINE_HASH_PASS",
            "ZIP_CRC_PASS",
            "ARCHIVE_STRUCTURE_IDENTICAL",
            "ONLY_ONE_MEMBER_CHANGED",
            "EXACT_TWO_RANGE_SWAP_PASS",
            "RANGES_BYTE_IDENTICAL_SINGLETON_PASS",
            "SWAPPED_ORDER_PASS",
            "REVERSIBILITY_PASS",
        ],
    }


def negative_tests(baseline: Path, candidate: Path, job: dict) -> List[str]:
    _, b_files = read_zip(baseline)
    _, c_files = read_zip(candidate)
    target = resolve_target(b_files, job["target_member_suffix"])
    b_text = b_files[target].decode(job["encoding"])
    c_text = c_files[target].decode(job["encoding"])
    _, first, second = exact_swap(b_text, job)
    other = next((n for n in b_files if n != target), None)
    if other is None:
        blocked("NO_UNRELATED_MEMBER_FOR_NEGATIVE_TEST")

    passed: List[str] = []

    def must_block(name: str, target_text: str, mutate_other: bool = False) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "negative.zip"
            with zipfile.ZipFile(baseline, "r") as zin, zipfile.ZipFile(p, "w") as zout:
                for info in zin.infolist():
                    if info.is_dir():
                        data = b""
                    elif info.filename == target:
                        data = target_text.encode(job["encoding"])
                    else:
                        data = zin.read(info.filename)
                        if mutate_other and info.filename == other:
                            data += b"X"
                    ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                    ni.compress_type = info.compress_type
                    ni.comment = info.comment
                    ni.extra = info.extra
                    ni.internal_attr = info.internal_attr
                    ni.external_attr = info.external_attr
                    ni.create_system = info.create_system
                    ni.flag_bits = info.flag_bits
                    zout.writestr(ni, data)
            try:
                validate(baseline, p, job)
            except RuntimeError as exc:
                if str(exc).startswith("BLOCKED:"):
                    passed.append(name + "_BLOCKED_PASS")
                    return
                raise
            blocked("NEGATIVE_ACCEPTED:" + name)

    must_block("NEG_UNCHANGED_WRONG_ORDER", b_text)
    must_block("NEG_DUPLICATE_RANGE", c_text + first)
    must_block("NEG_MUTATED_RANGE", c_text.replace(second, second + "X", 1))
    must_block("NEG_UNRELATED_FILE_CHANGED", c_text, mutate_other=True)
    return passed


def build(baseline: Path, output: Path, job: dict) -> dict:
    if output.resolve() == baseline.resolve():
        blocked("OUTPUT_MAY_NOT_OVERWRITE_BASELINE")
    if sha256_file(baseline).lower() != job["baseline_sha256"].lower():
        blocked("BASELINE_HASH_MISMATCH")

    _, files = read_zip(baseline)
    target = resolve_target(files, job["target_member_suffix"])
    try:
        source = files[target].decode(job["encoding"])
    except UnicodeDecodeError:
        blocked("TARGET_DECODE_FAIL")

    candidate_text, _, _ = exact_swap(source, job)
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    clone_zip_with_one_replacement(baseline, tmp, target, candidate_text.encode(job["encoding"]))

    report = validate(baseline, tmp, job)
    report["negative_checks"] = negative_tests(baseline, tmp, job)
    if len(report["negative_checks"]) != 4:
        blocked("NEGATIVE_SUITE_INCOMPLETE")

    os.replace(tmp, output)
    receipt = output.with_suffix(output.suffix + ".receipt.json")
    receipt.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def selftest() -> dict:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        baseline = root / "baseline.zip"
        with zipfile.ZipFile(baseline, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("plugin/main.php", "HEAD\nFIRST\nA\nSECOND\nB\nAFTER\nTAIL\n")
            zf.writestr("plugin/keep.txt", "KEEP")
        job = {
            "mode": "swap_two_adjacent_complete_ranges_only",
            "baseline_sha256": sha256_file(baseline),
            "target_member_suffix": "/main.php",
            "encoding": "utf-8",
            "first_start": "FIRST\n",
            "second_start": "SECOND\n",
            "after_second": "AFTER\n",
        }
        out = root / "candidate.zip"
        report = build(baseline, out, job)
        if report["status"] != "PASS" or len(report["negative_checks"]) != 4:
            blocked("SELFTEST_FAIL")
        return {"status": "PASS", "negative_checks": report["negative_checks"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("build")
    p.add_argument("job", type=Path)
    p.add_argument("--baseline", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)

    p = sub.add_parser("verify")
    p.add_argument("job", type=Path)
    p.add_argument("--baseline", required=True, type=Path)
    p.add_argument("--candidate", required=True, type=Path)

    sub.add_parser("selftest")
    args = parser.parse_args()

    try:
        if args.cmd == "selftest":
            result = selftest()
        else:
            job = load_job(args.job)
            if args.cmd == "build":
                result = build(args.baseline, args.output, job)
            else:
                result = validate(args.baseline, args.candidate, job)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return BLOCKED_EXIT


if __name__ == "__main__":
    raise SystemExit(main())
