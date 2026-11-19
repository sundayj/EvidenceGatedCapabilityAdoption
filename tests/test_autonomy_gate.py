from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools.autonomy_gate import Decision, evaluate_transition

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional validation dependency
    jsonschema = None


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "autonomy-transition"
    / "valid-execute.json"
)
NOW = datetime(2026, 11, 13, 12, 0, tzinfo=timezone.utc)


def valid_request() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def decision(request: dict) -> Decision:
    return evaluate_transition(request, now=NOW).decision


class ValidTransitionTests(unittest.TestCase):
    def test_valid_agent_transition_requires_no_human_approval_field(self):
        request = valid_request()

        self.assertNotIn("human_approval", request)
        self.assertEqual(decision(request), Decision.ADMIT)

    def test_one_evidence_item_may_support_multiple_criteria(self):
        request = valid_request()
        request["criteria"].append(
            {
                "id": "bounded-authority",
                "minimum_supporting_evidence": 1,
                "minimum_independent_domains": 1,
            }
        )
        request["evidence"][1]["criterion_ids"].append("bounded-authority")

        self.assertEqual(decision(request), Decision.ADMIT)

    def test_self_check_counts_as_support_but_not_independent_evidence(self):
        request = valid_request()
        request["criteria"][0]["minimum_independent_domains"] = 2

        result = evaluate_transition(request, now=NOW)

        self.assertEqual(result.decision, Decision.REPEAT)
        self.assertIn("lacks independent evidence domains", result.reasons[0])

    def test_two_independent_domains_can_satisfy_the_declared_threshold(self):
        request = valid_request()
        request["criteria"][0]["minimum_supporting_evidence"] = 3
        request["criteria"][0]["minimum_independent_domains"] = 2
        evidence = copy.deepcopy(request["evidence"][1])
        evidence.update(
            {
                "id": "evidence-independent-b",
                "producer_id": "audit-agent-b",
                "independence_domain": "audit-context-b",
                "artifact_ref": "artifact://independent-audit-b",
                "artifact_digest": "sha256:independent-audit-b",
            }
        )
        request["evidence"].append(evidence)

        self.assertEqual(decision(request), Decision.ADMIT)


class RevisionAndGovernanceTests(unittest.TestCase):
    def test_stale_expected_revision_repeats(self):
        request = valid_request()
        request["object"]["expected_revision"] = 2

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_skipped_next_revision_is_rejected(self):
        request = valid_request()
        request["object"]["next_revision"] = 7

        self.assertEqual(decision(request), Decision.REJECT)

    def test_candidate_methodology_cannot_govern_itself(self):
        request = valid_request()
        candidate = {
            "id": "egca",
            "version": "0.4.0",
            "digest": "sha256:egca-0.4.0-candidate",
        }
        request["governance"]["candidate"] = candidate
        request["governance"]["governing_sources"].append(candidate)
        request["subject"] = candidate
        request["object"]["id"] = candidate["id"]

        result = evaluate_transition(request, now=NOW)

        self.assertEqual(result.decision, Decision.REJECT)
        self.assertTrue(
            any("cannot govern its own transition" in reason for reason in result.reasons)
        )

    def test_subject_cannot_govern_itself_under_free_form_object_type(self):
        request = valid_request()
        subject = {
            "id": "egca",
            "version": "0.4.0",
            "digest": "sha256:egca-0.4.0-candidate",
        }
        request["subject"] = subject
        request["object"]["id"] = subject["id"]
        request["object"]["type"] = "rule"
        request["governance"].pop("candidate")
        request["governance"]["current"] = subject
        request["governance"]["governing_sources"] = [subject]
        request["mandate"]["policy_refs"] = [subject]
        request["mandate"]["authority"][0]["source"] = subject
        request["mandate"]["authority"][0]["target"] = subject["id"]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_candidate_policy_cannot_issue_its_own_authority(self):
        request = valid_request()
        candidate = {
            "id": "egca",
            "version": "0.4.0",
            "digest": "sha256:egca-0.4.0-candidate",
        }
        request["object"]["id"] = "egca"
        request["object"]["type"] = "methodology"
        request["subject"] = candidate
        request["governance"]["candidate"] = candidate
        request["mandate"]["policy_refs"] = [candidate]
        request["mandate"]["authority"][0]["source"] = candidate
        request["mandate"]["authority"][0]["target"] = "egca"

        result = evaluate_transition(request, now=NOW)

        self.assertEqual(result.decision, Decision.REJECT)
        self.assertTrue(
            any("cannot authorize its own transition" in reason for reason in result.reasons)
        )

    def test_prior_governance_must_be_pinned(self):
        request = valid_request()
        request["governance"]["governing_sources"] = [
            {"id": "repository", "version": "1", "digest": "sha256:repo-policy"}
        ]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_evidence_for_old_criteria_revision_repeats(self):
        request = valid_request()
        request["criteria_revision"] = "criteria-v2"

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_evidence_for_old_object_revision_repeats(self):
        request = valid_request()
        request["evidence"][1]["subject_revision"] = 2

        self.assertEqual(decision(request), Decision.REPEAT)


class EvidenceIntegrityTests(unittest.TestCase):
    def test_duplicate_evidence_id_is_rejected(self):
        request = valid_request()
        request["evidence"][1]["id"] = request["evidence"][0]["id"]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_duplicate_artifact_is_rejected(self):
        request = valid_request()
        request["evidence"][1]["artifact_digest"] = request["evidence"][0][
            "artifact_digest"
        ]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_correlated_attestations_do_not_create_independence(self):
        request = valid_request()
        request["criteria"][0]["minimum_independent_domains"] = 2
        second = copy.deepcopy(request["evidence"][1])
        second.update(
            {
                "id": "evidence-correlated-copy",
                "producer_id": "another-agent",
                "artifact_ref": "artifact://correlated-copy",
                "artifact_digest": "sha256:correlated-copy",
            }
        )
        request["evidence"].append(second)

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_unverified_evidence_does_not_satisfy_criterion(self):
        request = valid_request()
        request["evidence"][1]["verified"] = False

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_verified_refuting_evidence_rejects_transition(self):
        request = valid_request()
        request["evidence"][1]["effect"] = "refutes"

        self.assertEqual(decision(request), Decision.REJECT)

    def test_stale_refuting_evidence_does_not_override_current_evidence(self):
        request = valid_request()
        stale = copy.deepcopy(request["evidence"][1])
        stale.update(
            {
                "id": "evidence-stale-refutation",
                "effect": "refutes",
                "subject_revision": 2,
                "artifact_ref": "artifact://stale-refutation",
                "artifact_digest": "sha256:stale-refutation",
            }
        )
        request["evidence"].append(stale)

        self.assertEqual(decision(request), Decision.ADMIT)


class AuthorityTests(unittest.TestCase):
    def test_missing_derived_authority_repeats_without_a_human_queue(self):
        request = valid_request()
        request["mandate"]["authority"] = []

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_expired_authority_repeats_mandate_synthesis(self):
        request = valid_request()
        request["mandate"]["authority"][0]["valid_until"] = "2026-01-02T00:00:00Z"

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_action_mismatch_repeats_mandate_synthesis(self):
        request = valid_request()
        request["mandate"]["authority"][0]["actions"] = ["validate"]

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_object_scope_mismatch_repeats_mandate_synthesis(self):
        request = valid_request()
        request["mandate"]["authority"][0]["target"] = "work-order-002"

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_missing_objective_does_not_create_implicit_authority(self):
        request = valid_request()
        request["mandate"]["objective_refs"] = []

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_authority_must_derive_from_an_exact_policy_reference(self):
        request = valid_request()
        request["mandate"]["authority"][0]["source"]["version"] = "revision-6"

        self.assertEqual(decision(request), Decision.REPEAT)

    def test_unavailable_externally_enforced_authority_is_an_external_block(self):
        request = valid_request()
        authority = request["mandate"]["authority"][0]
        authority["enforcement"] = "external"
        authority["status"] = "unavailable"

        self.assertEqual(decision(request), Decision.EXTERNAL_BLOCK)

    def test_invalid_authority_window_is_rejected_as_malformed(self):
        request = valid_request()
        authority = request["mandate"]["authority"][0]
        authority["valid_from"] = authority["valid_until"]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_authority_precedence_is_independent_of_array_order(self):
        request = valid_request()
        unavailable = copy.deepcopy(request["mandate"]["authority"][0])
        unavailable.update({
            "id": "authority-external-unavailable",
            "enforcement": "external",
            "status": "unavailable",
        })
        request["mandate"]["authority"].append(unavailable)
        forward = decision(request)
        request["mandate"]["authority"].reverse()

        self.assertEqual(forward, Decision.EXTERNAL_BLOCK)
        self.assertEqual(decision(request), forward)


class FindingTests(unittest.TestCase):
    def test_remediable_blocking_finding_adapts(self):
        request = valid_request()
        request["findings"] = [
            {
                "id": "finding-001",
                "severity": "blocking",
                "status": "open",
                "remediable": True,
                "authority_external": False,
            }
        ]

        self.assertEqual(decision(request), Decision.ADAPT)

    def test_non_remediable_blocking_finding_rejects(self):
        request = valid_request()
        request["findings"] = [
            {
                "id": "finding-001",
                "severity": "blocking",
                "status": "open",
                "remediable": False,
                "authority_external": False,
            }
        ]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_external_authority_finding_is_explicitly_blocked(self):
        request = valid_request()
        request["findings"] = [
            {
                "id": "finding-001",
                "severity": "blocking",
                "status": "open",
                "remediable": False,
                "authority_external": True,
            }
        ]

        self.assertEqual(decision(request), Decision.EXTERNAL_BLOCK)

    def test_resolved_finding_does_not_block(self):
        request = valid_request()
        request["findings"] = [
            {
                "id": "finding-001",
                "severity": "blocking",
                "status": "resolved",
                "remediable": True,
                "authority_external": False,
            }
        ]

        self.assertEqual(decision(request), Decision.ADMIT)


class MalformedTransitionTests(unittest.TestCase):
    def test_malformed_request_fails_closed(self):
        result = evaluate_transition({"transition_id": "T-broken"}, now=NOW)

        self.assertEqual(result.decision, Decision.REJECT)
        self.assertIn("malformed transition", result.reasons[0])

    def test_malformed_nested_finding_fails_closed(self):
        request = valid_request()
        request["findings"] = ["not-an-object"]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_invalid_finding_status_fails_closed(self):
        request = valid_request()
        request["findings"] = [
            {
                "id": "finding-001",
                "severity": "blocking",
                "status": "ignored-by-typo",
                "remediable": True,
                "authority_external": False,
            }
        ]

        self.assertEqual(decision(request), Decision.REJECT)

    def test_empty_criteria_fails_closed(self):
        request = valid_request()
        request["criteria"] = []

        self.assertEqual(decision(request), Decision.REJECT)

    def test_duplicate_criterion_ids_fail_closed(self):
        request = valid_request()
        request["criteria"].append(copy.deepcopy(request["criteria"][0]))

        self.assertEqual(decision(request), Decision.REJECT)

    def test_zero_support_threshold_fails_closed(self):
        request = valid_request()
        request["criteria"][0]["minimum_supporting_evidence"] = 0

        self.assertEqual(decision(request), Decision.REJECT)

    def test_empty_evidence_criterion_links_fail_closed(self):
        request = valid_request()
        request["evidence"][0]["criterion_ids"] = []

        self.assertEqual(decision(request), Decision.REJECT)

    def test_invalid_authority_enforcement_fails_closed(self):
        request = valid_request()
        request["mandate"]["authority"][0]["enforcement"] = "garbage"

        self.assertEqual(decision(request), Decision.REJECT)

    def test_missing_authority_enforcement_fails_closed(self):
        request = valid_request()
        request["mandate"]["authority"][0].pop("enforcement")

        self.assertEqual(decision(request), Decision.REJECT)

    def test_unused_invalid_authority_window_fails_closed(self):
        request = valid_request()
        unused = copy.deepcopy(request["mandate"]["authority"][0])
        unused.update({
            "id": "unused-authority",
            "target": "unrelated-object",
            "valid_from": "2027-01-01T00:00:00Z",
            "valid_until": "2026-01-01T00:00:00Z",
        })
        request["mandate"]["authority"].append(unused)

        self.assertEqual(decision(request), Decision.REJECT)

    def test_orphan_evidence_criterion_reference_fails_closed(self):
        request = valid_request()
        request["evidence"][0]["criterion_ids"].append("unknown-criterion")

        self.assertEqual(decision(request), Decision.REJECT)

    def test_malformed_unused_evidence_fails_closed(self):
        request = valid_request()
        request["evidence"].append({
            "id": "malformed-unused",
            "criterion_ids": ["unreferenced"],
            "effect": "unknown",
            "verified": "yes",
            "independence_domain": "unused",
            "self_attestation": False,
            "subject_revision": 3,
            "criteria_revision": "criteria-v1",
            "artifact_digest": "sha256:malformed-unused",
        })

        self.assertEqual(decision(request), Decision.REJECT)

    def test_schema_is_valid_json_and_declares_no_human_approval(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "schemas" / "autonomy-transition.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertNotIn("human_approval", schema["properties"])

    @unittest.skipIf(jsonschema is None, "optional jsonschema package is unavailable")
    def test_valid_fixture_conforms_to_interchange_schema(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "schemas" / "autonomy-transition.schema.json").read_text(
                encoding="utf-8"
            )
        )

        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(valid_request(), schema)


if __name__ == "__main__":
    unittest.main()
