"""Pure evaluator for the E-001 evidence-derived transition experiment.

The evaluator deliberately does not authenticate provenance, issue authority,
mutate state, or perform the requested transition.  It answers one bounded
question: does a supplied transition record contain internally consistent,
applicable evidence and scoped authority under a prior governing policy?
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable


class Decision(str, Enum):
    """Possible transition-gate outcomes.

    ``ADMIT`` is transition admission.  ``ADAPT``, ``REJECT``, and ``REPEAT``
    retain EGCA's decision vocabulary.  ``EXTERNAL_BLOCK`` distinguishes a
    missing externally enforced authority from missing evidence; it is not a
    request for a human approval relay.
    """

    ADMIT = "Admit"
    ADAPT = "Adapt"
    REJECT = "Reject"
    REPEAT = "Repeat"
    EXTERNAL_BLOCK = "ExternalBlock"


@dataclass(frozen=True)
class GateResult:
    decision: Decision
    reasons: tuple[str, ...]

    @property
    def admitted(self) -> bool:
        return self.decision is Decision.ADMIT


class InvalidTransition(ValueError):
    """Raised only by the optional strict API for malformed requests."""


def _as_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InvalidTransition(f"{name} must be an object")
    return value


def _as_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise InvalidTransition(f"{name} must be an array")
    return value


def _required_text(mapping: dict[str, Any], key: str, parent: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise InvalidTransition(f"{parent}.{key} must be a non-empty string")
    return value


def _required_int(mapping: dict[str, Any], key: str, parent: str) -> int:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise InvalidTransition(f"{parent}.{key} must be a non-negative integer")
    return value


def _exact_keys(
    mapping: dict[str, Any], *, required: set[str], optional: set[str] = frozenset(), name: str
) -> None:
    missing = required - mapping.keys()
    unknown = mapping.keys() - required - optional
    if missing:
        raise InvalidTransition(f"{name} is missing required fields: {', '.join(sorted(missing))}")
    if unknown:
        raise InvalidTransition(f"{name} has unknown fields: {', '.join(sorted(unknown))}")


def _text_array(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    values = _as_list(value, name)
    if not allow_empty and not values:
        raise InvalidTransition(f"{name} must contain at least one item")
    if any(not isinstance(item, str) or not item.strip() for item in values):
        raise InvalidTransition(f"{name} must contain non-empty strings")
    return values


def _parse_time(value: Any, name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise InvalidTransition(f"{name} must be an ISO-8601 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise InvalidTransition(f"{name} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise InvalidTransition(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicate: set[str] = set()
    for value in values:
        if value in seen:
            duplicate.add(value)
        seen.add(value)
    return duplicate


def _source_identity(value: Any, name: str) -> tuple[str, str, str]:
    source = _as_mapping(value, name)
    _exact_keys(source, required={"id", "version", "digest"}, name=name)
    return (
        _required_text(source, "id", name),
        _required_text(source, "version", name),
        _required_text(source, "digest", name),
    )


def _validate_structure(request: dict[str, Any]) -> None:
    """Validate the complete public record before applying semantic policy.

    This intentionally mirrors the interchange schema without making the pure
    evaluator depend on the optional ``jsonschema`` package.  Keeping one
    mandatory structural pass prevents unused or stale fields from bypassing
    validation merely because a later semantic branch does not inspect them.
    """

    _exact_keys(
        request,
        required={
            "transition_id", "program_id", "criteria_revision", "subject", "object",
            "transition", "governance", "mandate", "criteria", "evidence",
            "findings",
        },
        name="request",
    )
    _required_text(request, "transition_id", "request")
    _required_text(request, "program_id", "request")
    _required_text(request, "criteria_revision", "request")

    subject_identity = _source_identity(request.get("subject"), "subject")

    obj = _as_mapping(request.get("object"), "object")
    _exact_keys(
        obj,
        required={"id", "type", "current_revision", "expected_revision", "next_revision"},
        name="object",
    )
    _required_text(obj, "id", "object")
    _required_text(obj, "type", "object")
    _required_int(obj, "current_revision", "object")
    _required_int(obj, "expected_revision", "object")
    if _required_int(obj, "next_revision", "object") < 1:
        raise InvalidTransition("object.next_revision must be at least one")
    if subject_identity[0] != _required_text(obj, "id", "object"):
        raise InvalidTransition("subject must identify the transition object")

    transition = _as_mapping(request.get("transition"), "transition")
    _exact_keys(
        transition,
        required={"action", "from_state", "to_state"},
        name="transition",
    )
    for field in ("action", "from_state", "to_state"):
        _required_text(transition, field, "transition")

    governance = _as_mapping(request.get("governance"), "governance")
    _exact_keys(
        governance,
        required={"current", "governing_sources"},
        optional={"candidate"},
        name="governance",
    )
    _source_identity(governance.get("current"), "governance.current")
    candidate = governance.get("candidate")
    if candidate is not None:
        _source_identity(candidate, "governance.candidate")
    governors = _as_list(governance.get("governing_sources"), "governance.governing_sources")
    if not governors:
        raise InvalidTransition("governance.governing_sources must contain at least one item")
    for source in governors:
        _source_identity(source, "governing source")

    mandate = _as_mapping(request.get("mandate"), "mandate")
    _exact_keys(
        mandate,
        required={"synthesized_by", "objective_refs", "policy_refs", "authority"},
        name="mandate",
    )
    _required_text(mandate, "synthesized_by", "mandate")
    for field, label in (("objective_refs", "objective reference"), ("policy_refs", "policy reference")):
        sources = _as_list(mandate.get(field), f"mandate.{field}")
        for source in sources:
            _source_identity(source, label)
    for raw in _as_list(mandate.get("authority"), "mandate.authority"):
        authority = _as_mapping(raw, "mandate authority")
        _exact_keys(
            authority,
            required={
                "id", "source", "target", "actions", "from_states", "to_states",
                "valid_from", "valid_until", "enforcement", "status",
            },
            name="mandate authority",
        )
        _required_text(authority, "id", "mandate authority")
        _source_identity(authority.get("source"), "authority.source")
        _required_text(authority, "target", "mandate authority")
        for field in ("actions", "from_states", "to_states"):
            _text_array(authority.get(field), f"authority.{field}")
        valid_from = _parse_time(authority.get("valid_from"), "authority.valid_from")
        valid_until = _parse_time(authority.get("valid_until"), "authority.valid_until")
        if valid_until <= valid_from:
            raise InvalidTransition("authority validity window must end after it starts")
        if authority.get("enforcement") not in {"internal", "external"}:
            raise InvalidTransition("authority.enforcement is invalid")
        if authority.get("status") not in {"active", "inactive", "unavailable", "revoked"}:
            raise InvalidTransition("authority.status is invalid")

    criteria = _as_list(request.get("criteria"), "criteria")
    if not criteria:
        raise InvalidTransition("criteria must contain at least one criterion")
    declared_criterion_ids: set[str] = set()
    for raw in criteria:
        criterion = _as_mapping(raw, "criterion")
        _exact_keys(
            criterion,
            required={"id", "minimum_supporting_evidence", "minimum_independent_domains"},
            name="criterion",
        )
        criterion_id = _required_text(criterion, "id", "criterion")
        if criterion_id in declared_criterion_ids:
            raise InvalidTransition(f"duplicate criterion ids: {criterion_id}")
        declared_criterion_ids.add(criterion_id)
        if _required_int(criterion, "minimum_supporting_evidence", "criterion") < 1:
            raise InvalidTransition("criterion.minimum_supporting_evidence must be at least one")
        _required_int(criterion, "minimum_independent_domains", "criterion")

    for raw in _as_list(request.get("evidence"), "evidence"):
        item = _as_mapping(raw, "evidence item")
        _exact_keys(
            item,
            required={
                "id", "criterion_ids", "effect", "verified", "producer_id",
                "producer_kind", "independence_domain", "self_attestation",
                "subject_revision", "criteria_revision", "artifact_ref", "artifact_digest",
            },
            name="evidence item",
        )
        for field in ("id", "producer_id", "producer_kind", "independence_domain", "criteria_revision", "artifact_ref", "artifact_digest"):
            _required_text(item, field, "evidence item")
        item_criterion_ids = _text_array(
            item.get("criterion_ids"), "evidence item.criterion_ids"
        )
        if _duplicates(item_criterion_ids):
            raise InvalidTransition("evidence item.criterion_ids must not contain duplicates")
        unknown_criteria = set(item_criterion_ids) - declared_criterion_ids
        if unknown_criteria:
            raise InvalidTransition(
                "evidence item references unknown criteria: "
                + ", ".join(sorted(unknown_criteria))
            )
        if item.get("effect") not in {"supports", "refutes"}:
            raise InvalidTransition("evidence item.effect is invalid")
        if not isinstance(item.get("verified"), bool):
            raise InvalidTransition("evidence item.verified must be a boolean")
        if not isinstance(item.get("self_attestation"), bool):
            raise InvalidTransition("evidence item.self_attestation must be a boolean")
        _required_int(item, "subject_revision", "evidence item")

    for raw in _as_list(request.get("findings"), "findings"):
        finding = _as_mapping(raw, "finding")
        _exact_keys(
            finding,
            required={"id", "severity", "status", "remediable", "authority_external"},
            name="finding",
        )
        _required_text(finding, "id", "finding")
        if finding.get("severity") not in {"advisory", "blocking"}:
            raise InvalidTransition("finding.severity is invalid")
        if finding.get("status") not in {"open", "resolved"}:
            raise InvalidTransition("finding.status is invalid")
        if not isinstance(finding.get("remediable"), bool):
            raise InvalidTransition("finding.remediable must be a boolean")
        if not isinstance(finding.get("authority_external"), bool):
            raise InvalidTransition("finding.authority_external must be a boolean")


def _governance_reasons(request: dict[str, Any]) -> list[str]:
    governance = _as_mapping(request.get("governance"), "governance")
    current = _as_mapping(governance.get("current"), "governance.current")
    current_identity = _source_identity(current, "governance.current")
    governors = _as_list(governance.get("governing_sources"), "governance.governing_sources")
    governor_identities = {
        _source_identity(item, "governing source") for item in governors
    }
    reasons: list[str] = []
    if current_identity not in governor_identities:
        reasons.append("the pinned current methodology is not a governing source")

    subject_identity = _source_identity(request.get("subject"), "subject")
    mandate = _as_mapping(request.get("mandate"), "mandate")
    policy_identities = {
        _source_identity(item, "policy reference")
        for item in _as_list(mandate.get("policy_refs"), "mandate.policy_refs")
    }
    if subject_identity in governor_identities or subject_identity in policy_identities:
        reasons.append("the transition subject cannot govern or authorize itself")

    candidate = governance.get("candidate")
    if candidate is not None:
        candidate_identity = _source_identity(candidate, "governance.candidate")
        if candidate_identity != subject_identity:
            reasons.append("the governance candidate must equal the bound transition subject")
        if candidate_identity in governor_identities:
            reasons.append("a candidate governance version cannot govern its own transition")
        if candidate_identity == current_identity:
            reasons.append("candidate and current governance identities must differ")
        if candidate_identity in policy_identities:
            reasons.append("a candidate policy cannot authorize its own transition")
    return reasons


def _authority_result(
    request: dict[str, Any], *, now: datetime
) -> GateResult | None:
    obj = _as_mapping(request.get("object"), "object")
    transition = _as_mapping(request.get("transition"), "transition")
    mandate = _as_mapping(request.get("mandate"), "mandate")
    object_id = _required_text(obj, "id", "object")
    action = _required_text(transition, "action", "transition")
    from_state = _required_text(transition, "from_state", "transition")
    to_state = _required_text(transition, "to_state", "transition")

    objective_refs = _as_list(mandate.get("objective_refs"), "mandate.objective_refs")
    policy_refs = _as_list(mandate.get("policy_refs"), "mandate.policy_refs")
    if not objective_refs:
        return GateResult(
            Decision.REPEAT, ("the derived mandate has no objective reference",)
        )
    if not policy_refs:
        return GateResult(
            Decision.REPEAT, ("the derived mandate has no policy reference",)
        )
    objective_identities = {
        _source_identity(item, "objective reference") for item in objective_refs
    }
    policy_identities = {
        _source_identity(item, "policy reference") for item in policy_refs
    }
    if len(objective_identities) != len(objective_refs):
        return GateResult(
            Decision.REPEAT,
            ("the derived mandate contains duplicate objective references",),
        )
    if len(policy_identities) != len(policy_refs):
        return GateResult(
            Decision.REPEAT,
            ("the derived mandate contains duplicate policy references",),
        )

    authorities = _as_list(mandate.get("authority"), "mandate.authority")
    matching_scope: list[dict[str, Any]] = []
    unavailable_external = False
    active_valid = False
    expired = False
    for raw in authorities:
        authority = _as_mapping(raw, "mandate authority")
        if _source_identity(authority.get("source"), "authority.source") not in policy_identities:
            continue
        if authority.get("target") != object_id:
            continue
        if action not in _as_list(authority.get("actions"), "authority.actions"):
            continue
        if from_state not in _as_list(authority.get("from_states"), "authority.from_states"):
            continue
        if to_state not in _as_list(authority.get("to_states"), "authority.to_states"):
            continue
        matching_scope.append(authority)
        if (
            authority.get("enforcement") == "external"
            and authority.get("status") in {"unavailable", "revoked"}
        ):
            unavailable_external = True
            continue
        if authority.get("status") != "active":
            continue
        valid_from = _parse_time(authority.get("valid_from"), "authority.valid_from")
        valid_until = _parse_time(authority.get("valid_until"), "authority.valid_until")
        if valid_until <= valid_from:
            raise InvalidTransition("authority validity window must end after it starts")
        if not valid_from <= now < valid_until:
            expired = True
            continue
        active_valid = True

    # Precedence is explicit and independent of serialization order. A declared
    # unavailable external authority is conservative and blocks even if another
    # supplied grant claims to be active; provenance authentication happens
    # outside this pure evaluator.
    if unavailable_external:
        return GateResult(
            Decision.EXTERNAL_BLOCK,
            ("an externally enforced authority is unavailable",),
        )
    if active_valid:
        return None

    if expired:
        return GateResult(
            Decision.REPEAT,
            ("matching authority is not currently valid; resynthesize the mandate",),
        )
    if matching_scope:
        return GateResult(
            Decision.REPEAT,
            ("matching authority is not active; resynthesize the mandate",),
        )
    return GateResult(
        Decision.REPEAT,
        ("the mandate lacks authority for the exact object and transition",),
    )


def _evidence_integrity_reasons(request: dict[str, Any]) -> list[str]:
    evidence = _as_list(request.get("evidence"), "evidence")
    identifiers = [
        _required_text(_as_mapping(item, "evidence item"), "id", "evidence item")
        for item in evidence
    ]
    digests = [
        _required_text(item, "artifact_digest", "evidence item") for item in evidence
    ]
    reasons: list[str] = []
    if duplicate := _duplicates(identifiers):
        reasons.append(f"duplicate evidence ids: {', '.join(sorted(duplicate))}")
    if duplicate := _duplicates(digests):
        reasons.append(f"duplicate evidence artifacts: {', '.join(sorted(duplicate))}")
    return reasons


def _revision_reasons(request: dict[str, Any]) -> tuple[list[str], list[str]]:
    obj = _as_mapping(request.get("object"), "object")
    current = _required_int(obj, "current_revision", "object")
    expected = _required_int(obj, "expected_revision", "object")
    next_revision = _required_int(obj, "next_revision", "object")
    reject: list[str] = []
    repeat: list[str] = []
    if next_revision != current + 1:
        reject.append("next object revision must be exactly current revision plus one")
    if expected != current:
        repeat.append("expected object revision is stale")
    return reject, repeat


def _finding_result(request: dict[str, Any]) -> GateResult | None:
    findings = [
        _as_mapping(item, "finding")
        for item in _as_list(request.get("findings"), "findings")
    ]
    for finding in findings:
        _required_text(finding, "id", "finding")
        if finding.get("severity") not in {"advisory", "blocking"}:
            raise InvalidTransition("finding.severity is invalid")
        if finding.get("status") not in {"open", "resolved"}:
            raise InvalidTransition("finding.status is invalid")
        if not isinstance(finding.get("remediable"), bool):
            raise InvalidTransition("finding.remediable must be a boolean")
        if not isinstance(finding.get("authority_external"), bool):
            raise InvalidTransition("finding.authority_external must be a boolean")
    open_findings = [
        item for item in findings if item.get("status") == "open"
    ]
    blocking = [item for item in open_findings if item.get("severity") == "blocking"]
    if not blocking:
        return None
    if any(item.get("authority_external") is True for item in blocking):
        return GateResult(
            Decision.EXTERNAL_BLOCK,
            ("an external-authority finding remains unresolved",),
        )
    if any(item.get("remediable") is True for item in blocking):
        return GateResult(
            Decision.ADAPT,
            ("a remediable blocking finding requires an adapted transition",),
        )
    return GateResult(
        Decision.REJECT,
        ("a non-remediable blocking finding contradicts the transition",),
    )


def _criterion_reasons(request: dict[str, Any]) -> list[str]:
    obj = _as_mapping(request.get("object"), "object")
    current_revision = _required_int(obj, "current_revision", "object")
    criteria_revision = _required_text(request, "criteria_revision", "request")
    evidence = [
        _as_mapping(item, "evidence item")
        for item in _as_list(request.get("evidence"), "evidence")
    ]
    reasons: list[str] = []

    criteria = [
        _as_mapping(item, "criterion")
        for item in _as_list(request.get("criteria"), "criteria")
    ]
    if not criteria:
        raise InvalidTransition("criteria must contain at least one criterion")
    criterion_ids = [
        _required_text(criterion, "id", "criterion") for criterion in criteria
    ]
    if duplicate := _duplicates(criterion_ids):
        raise InvalidTransition(
            f"duplicate criterion ids: {', '.join(sorted(duplicate))}"
        )

    for criterion in criteria:
        criterion_id = _required_text(criterion, "id", "criterion")
        minimum_support = _required_int(
            criterion, "minimum_supporting_evidence", "criterion"
        )
        if minimum_support < 1:
            raise InvalidTransition(
                "criterion.minimum_supporting_evidence must be at least one"
            )
        minimum_domains = _required_int(
            criterion, "minimum_independent_domains", "criterion"
        )
        applicable = [
            item
            for item in evidence
            if criterion_id
            in _as_list(item.get("criterion_ids"), "evidence item.criterion_ids")
            and item.get("effect") == "supports"
            and item.get("verified") is True
            and item.get("subject_revision") == current_revision
            and item.get("criteria_revision") == criteria_revision
        ]
        if len(applicable) < minimum_support:
            reasons.append(
                f"criterion {criterion_id} lacks applicable supporting evidence"
            )
        independent_domains = {
            _required_text(item, "independence_domain", "evidence item")
            for item in applicable
            if item.get("self_attestation") is False
        }
        if len(independent_domains) < minimum_domains:
            reasons.append(
                f"criterion {criterion_id} lacks independent evidence domains"
            )
    return reasons


def evaluate_transition(
    request: dict[str, Any], *, now: datetime | None = None
) -> GateResult:
    """Evaluate a transition record without mutating any external state.

    Malformed records are returned as ``Reject`` so callers cannot accidentally
    turn parsing errors into admission.  ``evaluate_transition_strict`` is
    available to tests or tooling that need the original validation exception.
    """

    try:
        return evaluate_transition_strict(request, now=now)
    except (InvalidTransition, KeyError, TypeError) as exc:
        return GateResult(Decision.REJECT, (f"malformed transition: {exc}",))


def evaluate_transition_strict(
    request: dict[str, Any], *, now: datetime | None = None
) -> GateResult:
    if not isinstance(request, dict):
        raise InvalidTransition("request must be an object")
    evaluation_time = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    _validate_structure(request)

    governance_reasons = _governance_reasons(request)
    integrity_reasons = _evidence_integrity_reasons(request)
    revision_reject, revision_repeat = _revision_reasons(request)
    reject_reasons = governance_reasons + integrity_reasons + revision_reject
    if reject_reasons:
        return GateResult(Decision.REJECT, tuple(reject_reasons))
    if revision_repeat:
        return GateResult(Decision.REPEAT, tuple(revision_repeat))

    evidence = [
        _as_mapping(item, "evidence item")
        for item in _as_list(request.get("evidence"), "evidence")
    ]
    obj = _as_mapping(request.get("object"), "object")
    current_revision = _required_int(obj, "current_revision", "object")
    criteria_revision = _required_text(request, "criteria_revision", "request")
    refuting = [
        _required_text(item, "id", "evidence item")
        for item in evidence
        if item.get("effect") == "refutes"
        and item.get("verified") is True
        and item.get("subject_revision") == current_revision
        and item.get("criteria_revision") == criteria_revision
    ]
    if refuting:
        return GateResult(
            Decision.REJECT,
            (f"verified refuting evidence: {', '.join(sorted(refuting))}",),
        )

    finding_result = _finding_result(request)
    if finding_result is not None:
        return finding_result

    authority_result = _authority_result(request, now=evaluation_time)
    if authority_result is not None:
        return authority_result

    criterion_reasons = _criterion_reasons(request)
    if criterion_reasons:
        return GateResult(Decision.REPEAT, tuple(criterion_reasons))

    return GateResult(
        Decision.ADMIT,
        (
            "the exact transition is supported by applicable evidence and scoped authority",
        ),
    )
