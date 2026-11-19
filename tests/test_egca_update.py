import importlib.util
import io
import json
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).parents[1]
    / "skills/evidence-gated-capability-adoption/scripts/egca_update.py"
)
SPEC = importlib.util.spec_from_file_location("egca_update_under_test", SCRIPT)
assert SPEC and SPEC.loader
updater = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = updater
SPEC.loader.exec_module(updater)


class EgcaUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.evidence_root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def info(self):
        return updater.UpdateInfo(
            local_version="0.3.1",
            remote_version="0.4.0",
            remote_sha="a" * 40,
            update_available=True,
            changelog="changes",
            migrations="migrations",
            repository="owner/repo",
            channel="main",
            skill_path="skills/egca",
            manifest_sha256="b" * 64,
        )

    def admission(self, info=None):
        info = info or self.info()
        evidence = []
        for index, kind in enumerate(sorted(updater.REQUIRED_EVIDENCE), 1):
            artifact_path = Path(f"evidence-{index}.json")
            artifact = json.dumps({"kind": kind, "result": "pass"}).encode()
            (self.evidence_root / artifact_path).write_bytes(artifact)
            evidence.append(
                {
                    "kind": kind,
                    "result": "pass",
                    "subject_digest": info.candidate_digest,
                    "evidence_id": f"e-{index}",
                    "artifact_path": str(artifact_path),
                    "artifact_sha256": updater.hashlib.sha256(artifact).hexdigest(),
                    "producer": "auditor" if kind == "independent_audit" else f"worker-{index}",
                    "domain": "audit" if kind == "independent_audit" else f"gate-{index}",
                }
            )
        return {
            "schema_version": 1,
            "criteria_revision": "egca-update-admission-v1",
            "decision": "Adopt",
            "governing_version": info.local_version,
            "candidate_digest": info.candidate_digest,
            "active_program_policy": "preserve_pinned_versions",
            "admitted_by": {
                "principal": "admission-controller",
                "domain": "admission",
                "transition": "egca-update-admit",
            },
            "evidence": evidence,
        }

    def test_candidate_digest_is_stable_and_content_bound(self):
        info = self.info()
        self.assertEqual(info.candidate_digest, info.candidate_digest)
        changed = updater.UpdateInfo(**{**info.__dict__, "remote_sha": "c" * 40})
        self.assertNotEqual(info.candidate_digest, changed.candidate_digest)

    def test_valid_admission(self):
        updater._validate_admission(self.admission(), self.info(), self.evidence_root)

    def test_check_builds_candidate_from_local_and_remote_manifests(self):
        local = {
            "name": "evidence-gated-capability-adoption",
            "version": "0.3.1",
            "repository": "owner/repo",
            "channel": "main",
            "skill_path": "skills/egca",
        }
        remote = {**local, "version": "0.4.0"}
        with mock.patch.object(updater, "_local_manifest", return_value=local), mock.patch.object(
            updater, "_branch_head", return_value="a" * 40
        ), mock.patch.object(
            updater,
            "_remote_text",
            side_effect=[json.dumps(remote), "changes", "migrations"],
        ):
            info = updater.check_for_updates()
        self.assertEqual(info.local_version, "0.3.1")
        self.assertEqual(info.remote_version, "0.4.0")
        self.assertTrue(info.update_available)

    def test_public_cli_guidance_matches_installed_version_fence(self):
        bootstrap = self.info()
        governed = updater.UpdateInfo(
            **{
                **bootstrap.__dict__,
                "local_version": "0.4.0",
                "remote_version": "0.4.1",
            }
        )

        with mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            updater._print_check(bootstrap)
        self.assertIn(f"--approved-sha {bootstrap.remote_sha}", output.getvalue())
        self.assertNotIn("--admission admission.json", output.getvalue())

        with mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            updater._print_check(governed)
        self.assertIn("--admission admission.json", output.getvalue())
        self.assertNotIn("--approved-sha", output.getvalue())

        readme = (Path(__file__).parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("0.3.1 -> 0.4.0 bootstrap", readme)
        self.assertIn("subsequent updates governed by installed EGCA 0.4.0", readme)

    def test_user_agent_uses_installed_package_version(self):
        with mock.patch.object(
            updater, "_local_manifest", return_value={"version": "9.8.7"}
        ):
            self.assertEqual(updater._user_agent(), "egca-skill-updater/9.8.7")

    def test_moved_candidate_is_rejected(self):
        admission = self.admission()
        admission["candidate_digest"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "Candidate moved"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_prior_version_must_govern_admission(self):
        admission = self.admission()
        admission["governing_version"] = "0.4.0"
        with self.assertRaisesRegex(RuntimeError, "installed EGCA version"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_missing_or_duplicate_evidence_is_rejected(self):
        admission = self.admission()
        admission["evidence"][-1] = dict(admission["evidence"][0])
        with self.assertRaises(RuntimeError):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_correlated_audit_is_rejected(self):
        admission = self.admission()
        audit = next(e for e in admission["evidence"] if e["kind"] == "independent_audit")
        audit["producer"] = admission["admitted_by"]["principal"]
        with self.assertRaisesRegex(RuntimeError, "Independent audit"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_active_program_version_fence_is_required(self):
        admission = self.admission()
        admission["active_program_policy"] = "upgrade_in_place"
        with self.assertRaisesRegex(RuntimeError, "active program"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_tampered_evidence_artifact_is_rejected(self):
        admission = self.admission()
        artifact = self.evidence_root / admission["evidence"][0]["artifact_path"]
        artifact.write_text("tampered")
        with self.assertRaisesRegex(RuntimeError, "digest does not match"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_evidence_path_escape_is_rejected(self):
        admission = self.admission()
        admission["evidence"][0]["artifact_path"] = "../outside"
        with self.assertRaisesRegex(RuntimeError, "confined regular file"):
            updater._validate_admission(admission, self.info(), self.evidence_root)

    def test_safe_extraction_rejects_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, symlink in (("../escape", False), ("root/link", True)):
                archive = root / ("link.zip" if symlink else "traversal.zip")
                with zipfile.ZipFile(archive, "w") as zf:
                    item = zipfile.ZipInfo(name)
                    if symlink:
                        item.external_attr = (stat.S_IFLNK | 0o777) << 16
                    zf.writestr(item, "payload")
                with self.assertRaisesRegex(RuntimeError, "Unsafe archive"):
                    updater._package_from_archive(archive, root / name.replace("/", "-"), "skill")

    def test_atomic_activation_retains_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root / "source", root / "target"
            source.mkdir(); target.mkdir()
            (source / "value").write_text("new")
            (target / "value").write_text("old")
            backup = updater._activate_package(source, target, lambda p: self.assertEqual((p / "value").read_text(), "new"))
            self.assertEqual((target / "value").read_text(), "new")
            self.assertEqual((backup / "value").read_text(), "old")

    def test_failed_activation_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root / "source", root / "target"
            source.mkdir(); target.mkdir()
            (source / "value").write_text("new")
            (target / "value").write_text("old")
            def fail(_path):
                raise RuntimeError("post-activation failure")
            with self.assertRaisesRegex(RuntimeError, "post-activation"):
                updater._activate_package(source, target, fail)
            self.assertEqual((target / "value").read_text(), "old")

    def test_apply_uses_info_version_and_rechecks_head(self):
        base = self.info()
        info = updater.UpdateInfo(
            **{**base.__dict__, "local_version": "0.4.0", "remote_version": "0.4.1"}
        )
        remote_manifest = {
            "name": "evidence-gated-capability-adoption",
            "version": info.remote_version,
            "repository": info.repository,
        }
        manifest_text = json.dumps(remote_manifest)
        info = updater.UpdateInfo(
            **{**info.__dict__, "manifest_sha256": updater._text_digest(manifest_text)}
        )
        admission = self.admission(info)
        root = self.evidence_root
        admission_path = root / "admission.json"
        admission_path.write_text(json.dumps(admission))
        package = root / "package"
        package.mkdir()
        with mock.patch.object(updater, "check_for_updates", return_value=info), mock.patch.object(
            updater, "_branch_head", return_value=info.remote_sha
        ) as head, mock.patch.object(
            updater, "_remote_text", return_value=manifest_text
        ), mock.patch.object(
            updater, "_request_bytes", return_value=b"archive"
        ), mock.patch.object(
            updater, "_package_from_archive", return_value=package
        ), mock.patch.object(
            updater, "_validate_package"
        ), mock.patch.object(
            updater, "_activate_package", return_value=root / "backup"
        ):
            updater.apply_update(admission_path=admission_path)
        head.assert_called_once_with(info.repository, info.channel)

    def test_pre_autonomous_version_requires_legacy_exact_sha(self):
        info = self.info()  # installed 0.3.1
        admission = self.admission(info)
        admission_path = self.evidence_root / "admission.json"
        admission_path.write_text(json.dumps(admission))
        with mock.patch.object(updater, "check_for_updates", return_value=info):
            with self.assertRaisesRegex(RuntimeError, "predates autonomous"):
                updater.apply_update(admission_path=admission_path)

        governed = updater.UpdateInfo(
            **{**info.__dict__, "local_version": "0.4.0", "remote_version": "0.4.1"}
        )
        with mock.patch.object(updater, "check_for_updates", return_value=governed):
            with self.assertRaisesRegex(RuntimeError, "evidence admission artifact"):
                updater.apply_update(approved_sha=governed.remote_sha)


if __name__ == "__main__":
    unittest.main()
