from __future__ import annotations

import json
import unittest
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional validation dependency
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "evidence-gated-capability-adoption"

SHARED_FILES = (
    "SKILL.md",
    "references/methodology.md",
    "templates/tracker-schema.md",
    "templates/experiment-template.md",
    "templates/decision-record-template.md",
    "templates/goal-prompt-template.md",
    "templates/execution-ledger-template.md",
    "schemas/experiment.schema.json",
    "schemas/autonomy-transition.schema.json",
)


def legacy_experiment() -> dict:
    """A minimal 0.3.1-shaped record with none of the 0.4 optional fields."""
    return {
        "experiment_id": "E-101",
        "candidate_id": "C-101",
        "title": "Legacy compatibility fixture",
        "hypothesis": "The historical record remains readable.",
        "scope": "Validate schema compatibility only.",
        "success_evidence": ["The record validates."],
        "rejection_evidence": ["The record is rejected."],
        "status": "Complete",
        "observed_evidence": ["Historical evidence."],
        "decision": "Adopt",
    }


def autonomous_experiment() -> dict:
    record = legacy_experiment()
    record.update(
        {
            "experiment_id": "E-102",
            "governing_methodology": {
                "id": "egca",
                "version": "0.3.1",
                "revision": "2a62f090365dc7eb1767ad7f63d3ae60566b995e",
            },
            "criteria_revision": "criteria-v1",
            "transition_mandate": {
                "id": "mandate-E-102",
                "revision": "1",
                "objective_refs": ["program:EGCA-AUTONOMY-001"],
                "action": "record-experiment-decision",
                "object_ref": "experiment:E-102",
                "object_revision": 1,
                "authority_refs": ["repository-instructions@revision-1"],
                "stop_conditions": ["object revision changes"],
                "rollback_conditions": [],
                "synthesizer_provenance": "agent:methodology-lane",
                "audit_provenance": ["test:test_methodology_contract"],
            },
            "self_validation_evidence": [
                {
                    "reference": "test://self",
                    "producer": "agent:methodology-lane",
                    "provenance_domain": "implementation-context",
                    "subject_revision": 1,
                    "criteria_revision": "criteria-v1",
                }
            ],
            "independent_evidence": [
                {
                    "reference": "test://contract",
                    "producer": "unittest",
                    "provenance_domain": "deterministic-contract-run",
                    "subject_revision": 1,
                    "criteria_revision": "criteria-v1",
                }
            ],
            "transition_outcome": "Admit",
            "transition_object_revision": 1,
        }
    )
    return record


class PackageParityTests(unittest.TestCase):
    def test_root_and_installable_contracts_are_identical(self):
        for relative_path in SHARED_FILES:
            with self.subTest(path=relative_path):
                self.assertEqual(
                    (ROOT / relative_path).read_bytes(),
                    (PACKAGE / relative_path).read_bytes(),
                )

    def test_manifest_declares_methodology_0_4_schema_2(self):
        manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["version"], "0.4.0")
        self.assertEqual(manifest["schema_version"], 2)


class MethodologyContractTests(unittest.TestCase):
    def test_json_documents_parse(self):
        paths = [ROOT / "schemas" / "experiment.schema.json"]
        paths.append(ROOT / "schemas" / "autonomy-transition.schema.json")
        paths.append(PACKAGE / "manifest.json")

        for path in paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_actor_neutral_and_non_circular_contract_is_explicit(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("EGCA is actor-neutral", skill)
        self.assertIn("open capability, gated commitment", skill)
        self.assertIn("may never govern its own adoption", skill)
        self.assertIn("ExternalBlock", skill)
        self.assertIn("No human relay is intrinsically required", skill)
        self.assertIn("returns it for another fresh claim", skill)
        self.assertIn("authenticated service controller", skill)

    def test_contract_does_not_require_intrinsic_human_update_approval(self):
        contract = "\n".join(
            [
                (ROOT / "SKILL.md").read_text(encoding="utf-8"),
                (ROOT / "references" / "methodology.md").read_text(encoding="utf-8"),
                (ROOT / "README.md").read_text(encoding="utf-8"),
            ]
        ).lower()

        self.assertNotIn("obtain explicit user approval", contract)
        self.assertNotIn("human approval under repository instructions", contract)

    @unittest.skipIf(jsonschema is None, "jsonschema is not installed")
    def test_legacy_0_3_1_record_remains_valid(self):
        schema = json.loads(
            (ROOT / "schemas" / "experiment.schema.json").read_text(encoding="utf-8")
        )

        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(legacy_experiment(), schema)

    @unittest.skipIf(jsonschema is None, "jsonschema is not installed")
    def test_autonomous_0_4_record_is_valid(self):
        schema = json.loads(
            (ROOT / "schemas" / "experiment.schema.json").read_text(encoding="utf-8")
        )

        jsonschema.validate(autonomous_experiment(), schema)

    @unittest.skipIf(jsonschema is None, "jsonschema is not installed")
    def test_transition_outcome_requires_versioned_governing_contract(self):
        schema = json.loads(
            (ROOT / "schemas" / "experiment.schema.json").read_text(encoding="utf-8")
        )
        record = legacy_experiment()
        record["transition_outcome"] = "Admit"

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(record, schema)

    @unittest.skipIf(jsonschema is None, "jsonschema is not installed")
    def test_external_block_requires_exact_external_authority_record(self):
        schema = json.loads(
            (ROOT / "schemas" / "experiment.schema.json").read_text(encoding="utf-8")
        )
        record = autonomous_experiment()
        record["transition_outcome"] = "ExternalBlock"

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(record, schema)

        record["external_block"] = {
            "authority_source": "host:protected-branch-policy@revision-1",
            "required_action": "merge",
            "reason": "The host reserves merge authority to an unavailable principal.",
            "recheck_condition": "The host grants object-scoped merge authority.",
        }
        jsonschema.validate(record, schema)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
