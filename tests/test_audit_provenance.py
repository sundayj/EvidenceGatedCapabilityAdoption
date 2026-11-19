from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.audit_provenance import AuditDecision, assess_audit


FIXTURE = Path(__file__).parent / "fixtures" / "audit-provenance" / "valid.json"


def valid_record() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def decision(record: dict) -> AuditDecision:
    return assess_audit(record).decision


class AuditProvenanceTests(unittest.TestCase):
    def test_valid_independent_audit_is_supported_without_human_field(self):
        record = valid_record()
        self.assertNotIn("human_approval", record)
        result = assess_audit(record)
        self.assertEqual(result.decision, AuditDecision.SUPPORTED)
        self.assertEqual(result.independent_clusters, 2)
        self.assertEqual(result.model_families, 2)

    def test_self_check_supports_but_is_not_independent(self):
        record = valid_record()
        record["attestations"] = [record["attestations"][0]]
        record["policy"]["minimum_supporting_attestations"] = 1
        record["policy"]["minimum_independent_clusters"] = 1
        record["policy"]["minimum_model_families"] = 0
        record["policy"]["require_adversarial"] = False
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_executor_attestation_is_not_independent_even_if_labeled_otherwise(self):
        record = valid_record()
        item = record["attestations"][0]
        item["self_attestation"] = False
        record["attestations"] = [item]
        record["policy"]["minimum_supporting_attestations"] = 1
        record["policy"]["minimum_independent_clusters"] = 1
        record["policy"]["minimum_model_families"] = 0
        record["policy"]["require_adversarial"] = False
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_agents_sharing_context_are_one_cluster(self):
        record = valid_record()
        record["attestations"][2]["context_digest"] = record["attestations"][1]["context_digest"]
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_agents_sharing_prompt_are_one_cluster(self):
        record = valid_record()
        record["attestations"][2]["prompt_digest"] = record["attestations"][1]["prompt_digest"]
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_agents_sharing_evidence_bundle_are_one_cluster(self):
        record = valid_record()
        record["attestations"][2]["evidence_bundle_digest"] = record[
            "attestations"
        ][1]["evidence_bundle_digest"]
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_transitive_correlation_collapses_clusters(self):
        record = valid_record()
        third = copy.deepcopy(record["attestations"][2])
        third.update({
            "id": "audit-c", "producer_id": "review-agent-c",
            "execution_id": "execution-c", "model_family": "family-c",
            "prompt_digest": record["attestations"][1]["prompt_digest"],
            "context_digest": record["attestations"][2]["context_digest"],
            "evidence_bundle_digest": "sha256:bundle-c",
            "artifact_digest": "sha256:report-c",
        })
        record["attestations"].append(third)
        record["attestations"][2]["prompt_digest"] = record["attestations"][1]["prompt_digest"]
        record["policy"]["minimum_supporting_attestations"] = 4
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_self_attestation_bridge_collapses_independent_reviews(self):
        record = valid_record()
        self_check, audit_a, audit_b = record["attestations"]
        self_check["prompt_digest"] = audit_a["prompt_digest"]
        self_check["context_digest"] = audit_b["context_digest"]

        result = assess_audit(record)

        self.assertEqual(result.decision, AuditDecision.REPEAT)
        self.assertEqual(result.independent_clusters, 0)

    def test_reviewer_correlated_with_executor_is_not_independent(self):
        record = valid_record()
        self_check, audit_a, _audit_b = record["attestations"]
        record["attestations"] = [self_check, audit_a]
        audit_a["prompt_digest"] = self_check["prompt_digest"]
        record["policy"]["minimum_supporting_attestations"] = 2
        record["policy"]["minimum_independent_clusters"] = 1
        record["policy"]["minimum_model_families"] = 1

        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_inconclusive_attestation_bridge_collapses_supporting_reviews(self):
        record = valid_record()
        audit_a, audit_b = record["attestations"][1:]
        bridge = copy.deepcopy(audit_b)
        bridge.update({
            "id": "inconclusive-bridge",
            "producer_id": "review-agent-c",
            "execution_id": "execution-c",
            "model_family": "family-c",
            "prompt_digest": audit_a["prompt_digest"],
            "context_digest": audit_b["context_digest"],
            "evidence_bundle_digest": "sha256:bundle-c",
            "artifact_digest": "sha256:report-c",
            "stance": "inconclusive",
        })
        record["attestations"].append(bridge)

        result = assess_audit(record)

        self.assertEqual(result.decision, AuditDecision.REPEAT)
        self.assertEqual(result.independent_clusters, 1)

    def test_model_family_diversity_is_separate_from_cluster_count(self):
        record = valid_record()
        record["attestations"][2]["model_family"] = "family-a"
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_missing_adversarial_review_repeats(self):
        record = valid_record()
        for item in record["attestations"]:
            item["adversarial"] = False
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_stale_attestation_does_not_count(self):
        record = valid_record()
        record["attestations"][2]["subject_revision"] = 3
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_unverified_attestation_does_not_count(self):
        record = valid_record()
        record["attestations"][2]["verified"] = False
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_verified_refutation_rejects(self):
        record = valid_record()
        record["attestations"][2]["stance"] = "refutes"
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_whitespace_normalized_current_refutation_rejects(self):
        record = valid_record()
        record["attestations"][2]["stance"] = "refutes"
        record["attestations"][2]["criteria_revision"] = " criteria-v2 "

        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_stale_refutation_does_not_reject_current_revision(self):
        record = valid_record()
        stale = copy.deepcopy(record["attestations"][2])
        stale.update({
            "id": "stale-refutation", "stance": "refutes", "subject_revision": 3,
            "artifact_digest": "sha256:stale-refutation",
        })
        record["attestations"].append(stale)
        self.assertEqual(decision(record), AuditDecision.SUPPORTED)

    def test_remediable_blocking_finding_adapts(self):
        record = valid_record()
        record["attestations"][1]["findings"] = [{
            "id": "finding-1", "severity": "blocking", "status": "open",
            "remediable": True,
        }]
        self.assertEqual(decision(record), AuditDecision.ADAPT)

    def test_nonremediable_blocking_finding_rejects(self):
        record = valid_record()
        record["attestations"][1]["findings"] = [{
            "id": "finding-1", "severity": "blocking", "status": "open",
            "remediable": False,
        }]
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_duplicate_attestation_id_rejects(self):
        record = valid_record()
        record["attestations"][2]["id"] = record["attestations"][1]["id"]
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_duplicate_report_artifact_rejects(self):
        record = valid_record()
        record["attestations"][2]["artifact_digest"] = record["attestations"][1]["artifact_digest"]
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_empty_attestation_set_repeats(self):
        record = valid_record()
        record["attestations"] = []
        self.assertEqual(decision(record), AuditDecision.REPEAT)

    def test_zero_independence_threshold_is_malformed(self):
        record = valid_record()
        record["policy"]["minimum_independent_clusters"] = 0
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_malformed_executor_identity_fails_closed(self):
        record = valid_record()
        record["policy"]["executor_ids"] = [{"id": "builder-agent"}]

        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_malformed_stale_attestation_revision_fails_closed(self):
        record = valid_record()
        extra = copy.deepcopy(record["attestations"][2])
        extra.update({
            "id": "malformed-stale",
            "subject_revision": "not-an-integer",
            "artifact_digest": "sha256:malformed-stale",
        })
        record["attestations"].append(extra)

        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_malformed_nested_finding_fails_closed(self):
        record = valid_record()
        record["attestations"][1]["findings"] = ["invalid"]
        self.assertEqual(decision(record), AuditDecision.REJECT)

    def test_malformed_finding_on_stale_attestation_still_fails_closed(self):
        record = valid_record()
        record["attestations"][1]["subject_revision"] = 3
        record["attestations"][1]["findings"] = ["invalid"]
        self.assertEqual(decision(record), AuditDecision.REJECT)


if __name__ == "__main__":
    unittest.main()
