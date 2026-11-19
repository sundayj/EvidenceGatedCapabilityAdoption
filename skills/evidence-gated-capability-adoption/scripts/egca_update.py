#!/usr/bin/env python3
"""Check for and apply EGCA skill updates through an evidence admission gate.

Read-only check:
    python scripts/egca_update.py check

Evidence-admitted update (candidate digest and exact SHA are immutable inputs):
    python scripts/egca_update.py update --admission admission.json

Legacy migration path (kept for 0.3.1 callers):
    python scripts/egca_update.py update --approved-sha <sha>

The updater intentionally has no timer, daemon, or background update mode. An
external EGCA program must produce an admission artifact before each update.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "egca-skill-updater/0.3.1"
DEFAULT_REPOSITORY = "sundayj/EvidenceGatedCapabilityAdoption"
DEFAULT_CHANNEL = "main"
SKILL_PATH = "skills/evidence-gated-capability-adoption"
ADMISSION_SCHEMA_VERSION = 1
ADMISSION_CRITERIA_REVISION = "egca-update-admission-v1"
ACTIVE_PROGRAM_POLICY = "preserve_pinned_versions"
AUTONOMOUS_GOVERNANCE_MIN_VERSION = (0, 4, 0)
REQUIRED_EVIDENCE = {
    "compatibility_review",
    "migration_review",
    "isolated_validation",
    "rollback_validation",
    "independent_audit",
}


@dataclass(frozen=True)
class UpdateInfo:
    local_version: str
    remote_version: str
    remote_sha: str
    update_available: bool
    changelog: str
    migrations: str
    repository: str
    channel: str
    skill_path: str
    manifest_sha256: str

    def candidate(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "repository": self.repository,
            "channel": self.channel,
            "skill_path": self.skill_path,
            "governing_version": self.local_version,
            "candidate_version": self.remote_version,
            "candidate_commit": self.remote_sha,
            "manifest_sha256": self.manifest_sha256,
            "changelog_sha256": _text_digest(self.changelog),
            "migrations_sha256": _text_digest(self.migrations),
        }

    @property
    def candidate_digest(self) -> str:
        return _json_digest(self.candidate())


def _json_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _request_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def _request_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _semver(value: str) -> tuple[int, int, int]:
    try:
        major, minor, patch = value.split(".", 2)
        return int(major), int(minor), int(patch)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Unsupported EGCA version format: {value!r}") from exc


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _local_manifest() -> dict[str, Any]:
    path = _skill_root() / "manifest.json"
    if not path.exists():
        raise RuntimeError(f"Missing local manifest: {path}")
    return _load_json(path)


def _branch_head(repository: str, channel: str) -> str:
    payload = json.loads(
        _request_text(f"https://api.github.com/repos/{repository}/branches/{channel}")
    )
    return payload["commit"]["sha"]


def _raw_url(repository: str, sha: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repository}/{sha}/{path}"


def _remote_text(repository: str, sha: str, path: str) -> str:
    return _request_text(_raw_url(repository, sha, path))


def check_for_updates() -> UpdateInfo:
    local = _local_manifest()
    repository = local.get("repository", DEFAULT_REPOSITORY)
    channel = local.get("channel", DEFAULT_CHANNEL)
    skill_path = local.get("skill_path", SKILL_PATH)

    remote_sha = _branch_head(repository, channel)
    manifest_text = _remote_text(repository, remote_sha, f"{skill_path}/manifest.json")
    remote_manifest = json.loads(manifest_text)

    if remote_manifest.get("name") != local.get("name"):
        raise RuntimeError("Remote manifest does not describe the installed EGCA skill")
    if remote_manifest.get("repository") != repository:
        raise RuntimeError("Remote manifest repository does not match the installed source")

    local_version = str(local["version"])
    remote_version = str(remote_manifest["version"])
    update_available = _semver(remote_version) > _semver(local_version)

    changelog_path = str(remote_manifest.get("changelog_path", "CHANGELOG.md"))
    migrations_path = str(remote_manifest.get("migrations_path", "MIGRATIONS.md"))
    changelog = _remote_text(repository, remote_sha, changelog_path)
    migrations = _remote_text(repository, remote_sha, migrations_path)

    return UpdateInfo(
        local_version=local_version,
        remote_version=remote_version,
        remote_sha=remote_sha,
        update_available=update_available,
        changelog=changelog,
        migrations=migrations,
        repository=repository,
        channel=channel,
        skill_path=skill_path,
        manifest_sha256=_text_digest(manifest_text),
    )


def _print_check(info: UpdateInfo) -> None:
    print(f"Installed EGCA version: {info.local_version}")
    print(f"Available EGCA version: {info.remote_version}")
    print(f"Source commit: {info.remote_sha}")
    print(f"Candidate digest: {info.candidate_digest}")
    print(f"Update available: {'yes' if info.update_available else 'no'}")
    print("\n--- CHANGELOG ---")
    print(info.changelog.rstrip())
    print("\n--- MIGRATIONS ---")
    print(info.migrations.rstrip())
    if info.update_available:
        print("\nNo files were changed.")
        print("Create an admission artifact from the candidate JSON below, then run:")
        print("  python scripts/egca_update.py update --admission admission.json")
        print(
            json.dumps(
                {
                    "candidate": info.candidate(),
                    "candidate_digest": info.candidate_digest,
                },
                indent=2,
                sort_keys=True,
            )
        )


def _archive_url(repository: str, sha: str) -> str:
    return f"https://github.com/{repository}/archive/{sha}.zip"


def _package_from_archive(archive: Path, destination: Path, skill_path: str) -> Path:
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            path = Path(member.filename)
            mode = member.external_attr >> 16
            if path.is_absolute() or ".." in path.parts or stat.S_ISLNK(mode):
                raise RuntimeError(f"Unsafe archive member: {member.filename}")
        zf.extractall(destination)

    roots = [p for p in destination.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Unexpected GitHub archive layout")
    package = roots[0] / skill_path
    if not (package / "SKILL.md").exists() or not (package / "manifest.json").exists():
        raise RuntimeError("Downloaded archive does not contain a valid EGCA skill package")
    return package


def _validate_package(source: Path, *, repository: str, version: str) -> None:
    manifest = _load_json(source / "manifest.json")
    if manifest.get("name") != "evidence-gated-capability-adoption":
        raise RuntimeError("Staged package does not identify the EGCA skill")
    if str(manifest.get("version")) != version:
        raise RuntimeError("Staged package version does not match admitted manifest")
    if manifest.get("repository") != repository:
        raise RuntimeError("Staged package repository does not match installed source")
    if not (source / "SKILL.md").is_file():
        raise RuntimeError("Staged package is missing SKILL.md")


def _activate_package(source: Path, target: Path, verify: Any) -> Path:
    """Atomically activate a complete directory and restore on verification failure."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.parent / f"{target.name}.backup-{timestamp}"
    candidate = target.parent / f".{target.name}.candidate-{os.getpid()}"
    if candidate.exists() or backup.exists():
        raise RuntimeError("Activation path collision; refusing to overwrite")
    shutil.copytree(source, candidate)
    target.rename(backup)
    try:
        candidate.rename(target)
        verify(target)
    except BaseException:
        failed = target.parent / f".{target.name}.failed-{os.getpid()}"
        if target.exists():
            target.rename(failed)
        backup.rename(target)
        shutil.rmtree(failed, ignore_errors=True)
        shutil.rmtree(candidate, ignore_errors=True)
        raise
    return backup


def _validate_admission(
    admission: dict[str, Any], info: UpdateInfo, evidence_root: Path
) -> None:
    """Verify local artifact integrity, not producer authentication.

    ``admitted_by`` and evidence producer names are claims emitted by the
    external release gate. That gate remains responsible for authenticating
    principals before it writes this bundle; this offline updater does not
    turn declarative JSON identity into an authenticated identity.
    """
    if admission.get("schema_version") != ADMISSION_SCHEMA_VERSION:
        raise RuntimeError("Unsupported admission schema version")
    if admission.get("criteria_revision") != ADMISSION_CRITERIA_REVISION:
        raise RuntimeError("Admission criteria revision mismatch")
    if admission.get("decision") != "Adopt":
        raise RuntimeError("Update admission decision must be Adopt")
    if admission.get("governing_version") != info.local_version:
        raise RuntimeError("Admission was not governed by the installed EGCA version")
    if admission.get("candidate_digest") != info.candidate_digest:
        raise RuntimeError("Candidate moved or evidence targets a different candidate")
    if admission.get("active_program_policy") != ACTIVE_PROGRAM_POLICY:
        raise RuntimeError("Admission must preserve active program version pins")

    admitted = admission.get("admitted_by")
    if not isinstance(admitted, dict) or not all(
        isinstance(admitted.get(key), str) and admitted[key]
        for key in ("principal", "domain", "transition")
    ):
        raise RuntimeError("Admission requires a scoped admitting identity")

    evidence = admission.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != len(REQUIRED_EVIDENCE):
        raise RuntimeError("Admission must contain exactly the required evidence set")
    kinds: set[str] = set()
    ids: set[str] = set()
    artifacts: set[str] = set()
    independent: dict[str, Any] | None = None
    for item in evidence:
        if not isinstance(item, dict):
            raise RuntimeError("Malformed admission evidence")
        kind = item.get("kind")
        if kind not in REQUIRED_EVIDENCE or item.get("result") != "pass":
            raise RuntimeError("Admission contains unknown or failing evidence")
        if item.get("subject_digest") != info.candidate_digest:
            raise RuntimeError("Evidence is not bound to the admitted candidate")
        evidence_id = item.get("evidence_id")
        artifact = item.get("artifact_sha256")
        artifact_path = item.get("artifact_path")
        producer = item.get("producer")
        domain = item.get("domain")
        if not all(
            isinstance(v, str) and v
            for v in (evidence_id, artifact, artifact_path, producer, domain)
        ):
            raise RuntimeError(
                "Evidence identity, artifact digest, producer, and domain are required"
            )
        if len(artifact) != 64 or any(c not in "0123456789abcdef" for c in artifact):
            raise RuntimeError("Evidence artifact digest must be lowercase SHA-256")
        relative = Path(artifact_path)
        root = evidence_root.resolve()
        resolved = (root / relative).resolve()
        if (
            relative.is_absolute()
            or not resolved.is_relative_to(root)
            or not resolved.is_file()
        ):
            raise RuntimeError("Evidence artifact path must name a confined regular file")
        if _file_digest(resolved) != artifact:
            raise RuntimeError("Evidence artifact digest does not match its file")
        kinds.add(kind)
        ids.add(evidence_id)
        artifacts.add(artifact)
        if kind == "independent_audit":
            independent = item
    if (
        kinds != REQUIRED_EVIDENCE
        or len(ids) != len(evidence)
        or len(artifacts) != len(evidence)
    ):
        raise RuntimeError("Evidence kinds, identities, and artifacts must be unique")
    if (
        independent is None
        or independent["producer"] == admitted["principal"]
        or independent["domain"] == admitted["domain"]
    ):
        raise RuntimeError("Independent audit must be produced by a separate identity and domain")


def apply_update(
    *, approved_sha: str | None = None, admission_path: Path | None = None
) -> None:
    info = check_for_updates()
    if not info.update_available:
        print(f"No newer EGCA version is available ({info.local_version} installed).")
        return
    if admission_path is not None:
        if _semver(info.local_version) < AUTONOMOUS_GOVERNANCE_MIN_VERSION:
            raise RuntimeError(
                "Installed EGCA predates autonomous update governance; this "
                "bootstrap update requires the legacy exact approved SHA"
            )
        _validate_admission(_load_json(admission_path), info, admission_path.parent)
        admitted_sha = info.remote_sha
        authority = f"locally verified evidence admission {info.candidate_digest}"
    elif approved_sha:
        if _semver(info.local_version) >= AUTONOMOUS_GOVERNANCE_MIN_VERSION:
            raise RuntimeError(
                "Installed EGCA supports autonomous governance; an evidence admission "
                "artifact is required"
            )
        if approved_sha != info.remote_sha:
            raise RuntimeError("The canonical branch moved after approval. Refusing to update.")
        admitted_sha = approved_sha
        authority = f"legacy exact-commit approval {approved_sha}"
    else:
        raise RuntimeError("An admission artifact or legacy approved SHA is required")

    # Re-read the branch immediately before download: a mutable head may not move
    # between evidence admission and activation.
    if _branch_head(info.repository, info.channel) != admitted_sha:
        raise RuntimeError("The canonical branch moved after admission. Refusing to update.")

    remote_manifest_text = _remote_text(
        info.repository, admitted_sha, f"{info.skill_path}/manifest.json"
    )
    if _text_digest(remote_manifest_text) != info.manifest_sha256:
        raise RuntimeError("Admitted manifest content changed unexpectedly")
    remote_manifest = json.loads(remote_manifest_text)
    local_version = info.local_version
    remote_version = str(remote_manifest["version"])

    with tempfile.TemporaryDirectory(prefix="egca-update-") as temp_dir:
        temp = Path(temp_dir)
        archive = temp / "egca.zip"
        archive.write_bytes(_request_bytes(_archive_url(info.repository, admitted_sha)))
        package = _package_from_archive(archive, temp / "extracted", info.skill_path)
        _validate_package(package, repository=info.repository, version=remote_version)
        backup = _activate_package(
            package,
            _skill_root(),
            lambda path: _validate_package(
                path, repository=info.repository, version=remote_version
            ),
        )

    print(f"Updated EGCA from {local_version} to {remote_version}.")
    print(f"Admitted source commit: {admitted_sha}")
    print(f"Authority: {authority}")
    print(f"Backup created at: {backup}")
    print("Active programs retain their pinned methodology versions.")
    print("Restart/reload the agent surface if it does not automatically reload skill files.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check for or apply evidence-admitted EGCA skill updates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="Read-only update check; never modifies the skill")

    update_parser = subparsers.add_parser(
        "update", help="Apply an admitted update for an exact canonical commit"
    )
    authority = update_parser.add_mutually_exclusive_group(required=True)
    authority.add_argument(
        "--admission",
        type=Path,
        help="Locally integrity-checked admission from an external release gate",
    )
    authority.add_argument(
        "--approved-sha",
        help="Legacy 0.3.1 exact-commit approval migration path",
    )

    args = parser.parse_args()
    try:
        if args.command == "check":
            _print_check(check_for_updates())
        else:
            apply_update(approved_sha=args.approved_sha, admission_path=args.admission)
        return 0
    except (RuntimeError, ValueError, KeyError, urllib.error.URLError, zipfile.BadZipFile) as exc:
        print(f"EGCA update error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
