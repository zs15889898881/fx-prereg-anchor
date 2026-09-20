"""Read-only verifier for the v3.6 canonical record.

Default execution only reads the parent record, current record, and anchor and
prints verification JSON.  ``--output`` is explicit and must name a new
isolated directory; only there the canonical UTF-8 bytes and result JSON are
written.  This script never generates or overwrites a record, anchor, README,
or controller file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
PARENT = ROOT / "FX_LOCAL" / "controller" / "24_SEED_A预注册记录_v3_5_20260920.json"
RECORD = ROOT / "FX_LOCAL" / "controller" / "25_SEED_A预注册记录_v3_6_20260920.json"
ANCHOR = PACKAGE / "FX_SEED_A_PREREGISTRATION_RECORD_V3_6_20260920_01.anchor.json"
EXPECTED_PARENT_RECORD = "8773aa46e86992da6d19a68877844d2601bb81b21712da07ca371b10385b8394"
EXPECTED_PARENT_CANONICAL = "19fbb3f43a842584547d6ff5495461a16e17b202ce6e8b2460c5b5a7fc846542"
EXPECTED_RECORD = "45957d96fa074b5fc7364ae8e17def9a5b5435d6ef35951f251e70adf7fa3d69"
EXPECTED_CANONICAL = "470bd5507046e19c885af6a3111771ba8a2dbcc3712c5e03dc17535fce790cd6"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(payload: object) -> bytes:
    """The published v3.5/v3.6 type-preserving canonical byte operation."""
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    for source, replacement in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), ("'", "\\u0027")):
        text = text.replace(source, replacement)
    return text.encode("utf-8")


def read_json(path: Path) -> tuple[bytes, dict[str, object]]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"INVALID_JSON:{path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"INVALID_OBJECT:{path}")
    return raw, value


def verify(parent_path: Path = PARENT, record_path: Path = RECORD, anchor_path: Path = ANCHOR) -> dict[str, object]:
    parent_raw, parent = read_json(parent_path)
    parent_sha = sha256(parent_raw)
    if parent_sha != EXPECTED_PARENT_RECORD:
        raise ValueError(f"PARENT_RECORD_HASH_MISMATCH:{parent_sha}")
    parent_payload = parent.get("canonical_payload")
    if not isinstance(parent_payload, dict):
        raise ValueError("PARENT_CANONICAL_PAYLOAD_MISSING")
    parent_canonical = sha256(canonical_bytes(parent_payload))
    if parent_canonical != EXPECTED_PARENT_CANONICAL or parent.get("canonical_payload_sha256") != EXPECTED_PARENT_CANONICAL:
        raise ValueError(f"PARENT_CANONICAL_HASH_MISMATCH:{parent_canonical}")

    record_raw, record = read_json(record_path)
    record_sha = sha256(record_raw)
    if record_sha != EXPECTED_RECORD:
        raise ValueError(f"CURRENT_RECORD_HASH_MISMATCH:{record_sha}")
    payload = record.get("canonical_payload")
    if not isinstance(payload, dict):
        raise ValueError("CURRENT_CANONICAL_PAYLOAD_MISSING")
    canonical_raw = canonical_bytes(payload)
    canonical_sha = sha256(canonical_raw)
    if canonical_sha != EXPECTED_CANONICAL or record.get("canonical_payload_sha256") != EXPECTED_CANONICAL:
        raise ValueError(f"CURRENT_CANONICAL_HASH_MISMATCH:{canonical_sha}")
    if record.get("record_id") != "FX_SEED_A_PREREGISTRATION_RECORD_V3_6_20260920_01" or record.get("version") != "v3.6":
        raise ValueError("OUTER_RECORD_ID_VERSION_MISMATCH")
    if payload.get("record_id") != record.get("record_id") or payload.get("schema") != "fx-seed-a-control-contract-v3.6":
        raise ValueError("ACTIVE_CANONICAL_IDENTITY_MISMATCH")
    if payload.get("active_rule_selector") != "v3_6_rule_confirmation":
        raise ValueError("ACTIVE_SELECTOR_MISMATCH")
    if payload.get("placebo_B", {}).get("status") != "NOT_REQUIRED":
        raise ValueError("B_STATUS_MISMATCH")
    states = payload.get("multiple_testing_and_states", {})
    if "NOT_EVALUABLE_DEPENDENCE_INSUFFICIENT" not in states.get("no_conclusion", []):
        raise ValueError("A_MBB_NO_CONCLUSION_MISSING")
    gates = payload.get("estimand_and_gates", {}).get("gate_logic", {})
    if gates.get("matched_predictive_increment_evidence_requires") != ["E", "D"]:
        raise ValueError("CLAIM_REQUIREMENT_MISMATCH")
    if "mechanism_increment_evidence_requires" in gates:
        raise ValueError("STALE_MECHANISM_CLAIM_KEY")

    anchor_raw, anchor = read_json(anchor_path)
    if anchor.get("anchor_record_id") != record.get("record_id"):
        raise ValueError("ANCHOR_RECORD_ID_MISMATCH")
    if anchor.get("record_bytes") != len(record_raw) or anchor.get("record_sha256") != record_sha:
        raise ValueError("ANCHOR_RECORD_BINDING_MISMATCH")
    if anchor.get("canonical_payload_sha256") != canonical_sha:
        raise ValueError("ANCHOR_CANONICAL_BINDING_MISMATCH")
    return {
        "status": "V3_6_READ_ONLY_VERIFY_OK",
        "parent_record_sha256": parent_sha,
        "parent_canonical_sha256": parent_canonical,
        "record_bytes": len(record_raw),
        "record_sha256": record_sha,
        "canonical_bytes": len(canonical_raw),
        "canonical_sha256": canonical_sha,
        "anchor_bytes": len(anchor_raw),
        "b_status": payload["placebo_B"]["status"],
        "active_selector": payload["active_rule_selector"],
        "no_conclusion_restored": "NOT_EVALUABLE_DEPENDENCE_INSUFFICIENT" in states["no_conclusion"],
        "write_mode": "read_only_default",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, default=PARENT)
    parser.add_argument("--record", type=Path, default=RECORD)
    parser.add_argument("--anchor", type=Path, default=ANCHOR)
    parser.add_argument("--output", type=Path, default=None, help="explicit new isolated directory for verifier artifacts")
    args = parser.parse_args()
    try:
        result = verify(args.parent, args.record, args.anchor)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"VERIFY_FAILED:{exc}", file=sys.stderr)
        return 1
    if args.output is not None:
        if args.output.exists() and any(args.output.iterdir()):
            print(f"VERIFY_FAILED:OUTPUT_NOT_EMPTY:{args.output}", file=sys.stderr)
            return 1
        args.output.mkdir(parents=True, exist_ok=True)
        canonical = canonical_bytes(read_json(args.record)[1]["canonical_payload"])
        (args.output / "canonical_payload_utf8.json").write_bytes(canonical)
        result = {**result, "write_mode": "explicit_output"}
        (args.output / "verification_result.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
