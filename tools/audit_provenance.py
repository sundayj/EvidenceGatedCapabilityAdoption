"""Conservative provenance evaluator for independent EGCA audit evidence.

This E-003 experiment treats attestation count as insufficient. Attestations
that share a producer, execution, prompt, context, or evidence bundle are one
correlation cluster. Self/executor attestations remain supporting evidence but
do not satisfy an independent-cluster threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class AuditDecision(str, Enum):
    SUPPORTED = "Supported"
    ADAPT = "Adapt"
    REJECT = "Reject"
    REPEAT = "Repeat"


@dataclass(frozen=True)
class AuditResult:
    decision: AuditDecision
    reasons: tuple[str, ...]
    independent_clusters: int = 0
    model_families: int = 0


class InvalidAudit(ValueError):
    pass


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InvalidAudit(f"{field} must be an object")
    return value


def _items(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise InvalidAudit(f"{field} must be an array")
    return value


def _text(record: dict[str, Any], field: str, parent: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise InvalidAudit(f"{parent}.{field} must be a non-empty string")
    return value.strip()


def _integer(record: dict[str, Any], field: str, parent: str) -> int:
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise InvalidAudit(f"{parent}.{field} must be a non-negative integer")
    return value


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


_CORRELATION_FIELDS = (
    "producer_id",
    "execution_id",
    "prompt_digest",
    "context_digest",
    "evidence_bundle_digest",
)


def _clusters(attestations: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    union = _UnionFind(len(attestations))
    seen: dict[tuple[str, str], int] = {}
    for index, attestation in enumerate(attestations):
        for field in _CORRELATION_FIELDS:
            value = _text(attestation, field, "attestation")
            key = (field, value)
            if key in seen:
                union.union(index, seen[key])
            else:
                seen[key] = index
    grouped: dict[int, list[dict[str, Any]]] = {}
    for index, attestation in enumerate(attestations):
        grouped.setdefault(union.find(index), []).append(attestation)
    return list(grouped.values())


def _findings(attestation: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for raw in _items(attestation.get("findings"), "attestation.findings"):
        finding = _mapping(raw, "finding")
        _text(finding, "id", "finding")
        if finding.get("severity") not in {"advisory", "blocking"}:
            raise InvalidAudit("finding.severity is invalid")
        if finding.get("status") not in {"open", "resolved"}:
            raise InvalidAudit("finding.status is invalid")
        if not isinstance(finding.get("remediable"), bool):
            raise InvalidAudit("finding.remediable must be a boolean")
        findings.append(finding)
    return findings


def _finding_result(attestations: list[dict[str, Any]]) -> AuditResult | None:
    open_blocking = [
        finding
        for attestation in attestations
        for finding in _findings(attestation)
        if finding["status"] == "open" and finding["severity"] == "blocking"
    ]
    if not open_blocking:
        return None
    if any(item["remediable"] is False for item in open_blocking):
        return AuditResult(
            AuditDecision.REJECT,
            ("a verified non-remediable blocking finding remains open",),
        )
    return AuditResult(
        AuditDecision.ADAPT,
        ("verified remediable blocking findings require adaptation",),
    )


def assess_audit(record: dict[str, Any]) -> AuditResult:
    """Fail closed while classifying applicable audit evidence."""

    try:
        return assess_audit_strict(record)
    except (InvalidAudit, KeyError, TypeError) as exc:
        return AuditResult(AuditDecision.REJECT, (f"malformed audit: {exc}",))


def assess_audit_strict(record: dict[str, Any]) -> AuditResult:
    record = _mapping(record, "audit")
    subject_revision = _integer(record, "subject_revision", "audit")
    criteria_revision = _text(record, "criteria_revision", "audit")
    policy = _mapping(record.get("policy"), "policy")
    minimum_support = _integer(policy, "minimum_supporting_attestations", "policy")
    minimum_clusters = _integer(policy, "minimum_independent_clusters", "policy")
    minimum_models = _integer(policy, "minimum_model_families", "policy")
    if minimum_support < 1 or minimum_clusters < 1:
        raise InvalidAudit("support and independent-cluster thresholds must be positive")
    if not isinstance(policy.get("require_adversarial"), bool):
        raise InvalidAudit("policy.require_adversarial must be a boolean")
    executor_values = _items(policy.get("executor_ids"), "policy.executor_ids")
    if any(not isinstance(value, str) or not value.strip() for value in executor_values):
        raise InvalidAudit("policy.executor_ids must contain non-empty strings")
    executor_ids = {value.strip().lower() for value in executor_values}
    if len(executor_ids) != len(executor_values):
        raise InvalidAudit("policy.executor_ids must not contain duplicates")

    attestations = [
        _mapping(value, "attestation")
        for value in _items(record.get("attestations"), "attestations")
    ]
    identifiers = [_text(item, "id", "attestation") for item in attestations]
    artifacts = [_text(item, "artifact_digest", "attestation") for item in attestations]
    if duplicate := _duplicates(identifiers):
        raise InvalidAudit(f"duplicate attestation ids: {', '.join(sorted(duplicate))}")
    if duplicate := _duplicates(artifacts):
        raise InvalidAudit(f"duplicate attestation artifacts: {', '.join(sorted(duplicate))}")

    applicable: list[dict[str, Any]] = []
    for item in attestations:
        if item.get("stance") not in {"supports", "refutes", "inconclusive"}:
            raise InvalidAudit("attestation.stance is invalid")
        if not isinstance(item.get("verified"), bool):
            raise InvalidAudit("attestation.verified must be a boolean")
        if not isinstance(item.get("self_attestation"), bool):
            raise InvalidAudit("attestation.self_attestation must be a boolean")
        if not isinstance(item.get("adversarial"), bool):
            raise InvalidAudit("attestation.adversarial must be a boolean")
        _text(item, "model_family", "attestation")
        _integer(item, "subject_revision", "attestation")
        _text(item, "criteria_revision", "attestation")
        _findings(item)
        for field in _CORRELATION_FIELDS:
            _text(item, field, "attestation")
        if (
            item["verified"] is True
            and item.get("subject_revision") == subject_revision
            and _text(item, "criteria_revision", "attestation") == criteria_revision
        ):
            applicable.append(item)

    refuting = [item for item in applicable if item["stance"] == "refutes"]
    if refuting:
        return AuditResult(
            AuditDecision.REJECT,
            ("applicable verified audit evidence refutes the transition",),
        )

    finding_result = _finding_result(applicable)
    if finding_result is not None:
        return finding_result

    supporting = [item for item in applicable if item["stance"] == "supports"]
    if len(supporting) < minimum_support:
        return AuditResult(
            AuditDecision.REPEAT,
            ("insufficient applicable supporting attestations",),
        )

    independent = [
        item
        for item in supporting
        if item["self_attestation"] is False
        and _text(item, "producer_id", "attestation").lower() not in executor_ids
    ]
    # Correlate the complete applicable supporting set first. A self/executor
    # attestation can therefore reveal shared prompt, context, or evidence
    # provenance between nominally independent reviews instead of disappearing
    # before transitive clustering.
    # Every applicable attestation participates in correlation, regardless of
    # stance. An inconclusive or refuting third run may still prove that two
    # nominally separate supporting reviews shared provenance.
    all_clusters = _clusters(applicable) if applicable else []
    independent_ids = {id(item) for item in independent}
    non_independent_ids = {
        id(item)
        for item in applicable
        if item["self_attestation"] is True
        or _text(item, "producer_id", "attestation").lower() in executor_ids
    }
    clusters = [
        cluster
        for cluster in all_clusters
        if (
            any(id(item) in independent_ids for item in cluster)
            and not any(id(item) in non_independent_ids for item in cluster)
        )
    ]
    qualifying_independent = [
        item
        for cluster in clusters
        for item in cluster
        if id(item) in independent_ids
    ]
    model_families = {
        _text(item, "model_family", "attestation")
        for item in qualifying_independent
    }
    if len(clusters) < minimum_clusters:
        return AuditResult(
            AuditDecision.REPEAT,
            ("independent attestations collapse into too few provenance clusters",),
            independent_clusters=len(clusters),
            model_families=len(model_families),
        )
    if len(model_families) < minimum_models:
        return AuditResult(
            AuditDecision.REPEAT,
            ("independent evidence lacks the required model-family diversity",),
            independent_clusters=len(clusters),
            model_families=len(model_families),
        )
    if policy["require_adversarial"] and not any(
        item["adversarial"] is True for item in qualifying_independent
    ):
        return AuditResult(
            AuditDecision.REPEAT,
            ("no applicable independent adversarial attestation exists",),
            independent_clusters=len(clusters),
            model_families=len(model_families),
        )
    return AuditResult(
        AuditDecision.SUPPORTED,
        ("independent audit provenance satisfies the declared evidence policy",),
        independent_clusters=len(clusters),
        model_families=len(model_families),
    )
