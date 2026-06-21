#!/usr/bin/env python3
"""
Test: Full Lifecycle Event-Chain Integrity (KR-019 full expert gate, KR-072 lifecycle)

Faz 7 contract-side real-world test. Beyond validating each document against its
own schema, this asserts the cross-document invariants that make the end-to-end
flow correct:

  1. Multi-document fixture: every stage payload validates against its schema.
  2. ID-join integrity WITHIN each identifier family
     (prefixed result_/mission_ ... vs RFC 4122 UUIDs — the two families do not
     string-match by design, see schema notes.id_format).
  3. Publication gate (KR-019): a farmer-facing derived.published document exists
     ONLY when the expert verdict resolved to gate_outcome=APPROVED_PUBLISHED.
     On rejection there is NO publication.
  4. verdict -> gate_outcome derivation is consistent with the schema's mapping.
  5. dataset_status / mission_status transitions in the chain are legal edges of
     the canonical state machines (enums/*.enum.v1.json).
"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

try:
    from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
    from referencing import Registry, Resource  # type: ignore[import-untyped]
except ImportError:
    pytest.skip("jsonschema or referencing not installed", allow_module_level=True)

BASE_DIR = Path(__file__).parent.parent
FIXTURE = Path(__file__).parent / "fixtures" / "full_lifecycle_chain.json"

# verdict -> gate_outcome mapping, canonical per expert_review_decided.v1 schema.
VERDICT_TO_GATE = {
    "confirmed": "APPROVED_PUBLISHED",
    "corrected": "APPROVED_PUBLISHED",
    "rejected": "REJECTED",
    "needs_more_expert": "ESCALATED",
}

# Join keys shared by the two UUID-family review events.
_UUID_JOIN_KEYS = ("review_id", "analysis_result_id", "mission_id", "field_id")


def _build_local_registry(base_dir: Path) -> Registry:
    """Build a referencing.Registry from all local schema/enum JSON files."""
    registry = Registry()
    for search_dir in [base_dir / "schemas", base_dir / "enums"]:
        if not search_dir.exists():
            continue
        for json_file in search_dir.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    contents = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(contents, dict):
                continue
            schema_id = contents.get("$id")
            if schema_id:
                registry = registry.with_resource(schema_id, Resource.from_contents(contents))
    return registry


def _load_schema(rel_path: str) -> Dict[str, Any]:
    with open(BASE_DIR / "schemas" / rel_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_enum(name: str) -> Dict[str, Any]:
    with open(BASE_DIR / "enums" / name, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def registry() -> Registry:
    return _build_local_registry(BASE_DIR)


@pytest.fixture(scope="module")
def chain() -> Dict[str, Any]:
    with open(FIXTURE, "r", encoding="utf-8") as f:
        return json.load(f)


def _validate(stage: Dict[str, Any], registry: Registry) -> None:
    """Validate one fixture stage {schema, document} against its schema."""
    schema = _load_schema(stage["schema"])
    Draft202012Validator(schema, registry=registry).validate(stage["document"])


# ---------------------------------------------------------------------------
# 1. Every document in both paths validates against its schema
# ---------------------------------------------------------------------------


def test_approved_path_documents_validate(chain: Dict[str, Any], registry: Registry) -> None:
    approved = chain["approved_path"]
    for stage_name in (
        "analysis_completed",
        "analysis_review_requested",
        "expert_review_decided",
        "derived_published",
    ):
        _validate(approved[stage_name], registry)


def test_rejected_path_documents_validate(chain: Dict[str, Any], registry: Registry) -> None:
    rejected = chain["rejected_path"]
    for stage_name in ("analysis_review_requested", "expert_review_decided"):
        _validate(rejected[stage_name], registry)


# ---------------------------------------------------------------------------
# 2. ID-join integrity within the UUID family (review_requested -> decided)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path_name", ["approved_path", "rejected_path"])
def test_review_uuid_family_id_join(chain: Dict[str, Any], path_name: str) -> None:
    path = chain[path_name]
    requested = path["analysis_review_requested"]["document"]["data"]
    decided = path["expert_review_decided"]["document"]["data"]
    for key in _UUID_JOIN_KEYS:
        assert requested[key] == decided[key], (
            f"{path_name}: review event join key '{key}' diverges "
            f"({requested[key]!r} != {decided[key]!r})"
        )


def test_prefixed_family_id_join_approved(chain: Dict[str, Any]) -> None:
    """analysis.completed and derived.published share the same prefixed mission_id."""
    approved = chain["approved_path"]
    completed = approved["analysis_completed"]["document"]["data"]
    published = approved["derived_published"]["document"]["data"]
    assert completed["mission_id"] == published["mission_id"]


# ---------------------------------------------------------------------------
# 3 + 4. Publication gate (KR-019) and verdict -> gate_outcome derivation
# ---------------------------------------------------------------------------


def test_verdict_to_gate_outcome_is_canonical(chain: Dict[str, Any]) -> None:
    for path_name in ("approved_path", "rejected_path"):
        data = chain[path_name]["expert_review_decided"]["document"]["data"]
        expected = VERDICT_TO_GATE[data["verdict"]]
        assert data["gate_outcome"] == expected, (
            f"{path_name}: verdict {data['verdict']!r} must map to {expected!r}, "
            f"got {data['gate_outcome']!r}"
        )


def test_approved_gate_authorises_publication(chain: Dict[str, Any]) -> None:
    """APPROVED_PUBLISHED -> a derived.published document MUST exist."""
    approved = chain["approved_path"]
    assert approved["expert_review_decided"]["document"]["data"]["gate_outcome"] == "APPROVED_PUBLISHED"
    assert "derived_published" in approved, "approved path must publish to the farmer"
    pub = approved["derived_published"]["document"]
    assert pub["event_type"] == "derived.published"


def test_rejected_gate_blocks_publication(chain: Dict[str, Any]) -> None:
    """REJECTED -> NO derived.published document in the chain (farmer never sees it)."""
    rejected = chain["rejected_path"]
    assert rejected["expert_review_decided"]["document"]["data"]["gate_outcome"] == "REJECTED"
    assert "derived_published" not in rejected, (
        "rejected result must NOT be published to the farmer (KR-019 full gate)"
    )


# ---------------------------------------------------------------------------
# 5. State-machine transition consistency
# ---------------------------------------------------------------------------


def test_published_transition_is_legal_dataset_edge(chain: Dict[str, Any]) -> None:
    """derived.published status_from/status_to is a declared dataset_status edge."""
    data = chain["approved_path"]["derived_published"]["document"]["data"]
    transitions = _load_enum("dataset_status.enum.v1.json")["x-state-machine"]["transitions"]
    legal = {(t["from"], t["to"]) for t in transitions}
    edge = (data["status_from"], data["status_to"])
    assert edge in legal, f"dataset transition {edge} is not a legal state-machine edge"


def test_published_statuses_are_valid_enum_members(chain: Dict[str, Any]) -> None:
    data = chain["approved_path"]["derived_published"]["document"]["data"]
    members = set(_load_enum("dataset_status.enum.v1.json")["enum"])
    assert data["status_from"] in members
    assert data["status_to"] in members


def test_terminal_mission_states_reachable(chain: Dict[str, Any]) -> None:
    """The gate's terminal mission outcomes (DELIVERED on approve, REJECTED on
    reject) exist in the canonical mission_status enum so the platform can drive
    the mission there."""
    members = set(_load_enum("mission_status.enum.v1.json")["enum"])
    assert "DELIVERED" in members
    assert "REJECTED" in members
    assert "ANALYSIS_COMPLETED" in members
