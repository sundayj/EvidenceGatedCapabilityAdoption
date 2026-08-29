#!/usr/bin/env python3
"""Check for and apply EGCA skill updates with explicit user approval.

Read-only check:
    python scripts/egca_update.py check

Approved update (only after the user approves the exact SHA shown by check):
    python scripts/egca_update.py update --approved-sha <sha>

The updater intentionally has no unattended/automatic update mode.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "egca-skill-updater/0.2.0"
DEFAULT_REPOSITORY = "sundayj/EvidenceGatedCapabilityAdoption"
DEFAULT_CHANNEL = "main"
SKILL_PATH = "skills/evidence-gated-capability-adoption"


@dataclass(frozen=True)
class UpdateInfo:
    local_version: str
    remote_version: str
    remote_sha: str
    update_available: bool
    changelog: str
    migrations: str


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
    remote_manifest = json.loads(
        _remote_text(repository, remote_sha, f"{skill_path}/manifest.json")
    )

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
    )


def _print_check(info: UpdateInfo) -> None:
    print(f"Installed EGCA version: {info.local_version}")
    print(f"Available EGCA version: {info.remote_version}")
    print(f"Source commit: {info.remote_sha}")
    print(f"Update available: {'yes' if info.update_available else 'no'}")
    print("\n--- CHANGELOG ---")
    print(info.changelog.rstrip())
    print("\n--- MIGRATIONS ---")
    print(info.migrations.rstrip())
    if info.update_available:
        print("\nNo files were changed.")
        print(
            "After the user explicitly approves this exact source commit, run:\n"
            f"  python scripts/egca_update.py update --approved-sha {info.remote_sha}"
        )


def _archive_url(repository: str, sha: str) -> str:
    return f"https://github.com/{repository}/archive/{sha}.zip"


def _package_from_archive(archive: Path, destination: Path, skill_path: str) -> Path:
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(destination)

    roots = [p for p in destination.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Unexpected GitHub archive layout")
    package = roots[0] / skill_path
    if not (package / "SKILL.md").exists() or not (package / "manifest.json").exists():
        raise RuntimeError("Downloaded archive does not contain a valid EGCA skill package")
    return package


def _relative_files(root: Path) -> set[Path]:
    return {
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }


def _apply_package(source: Path, target: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.parent / f"{target.name}.backup-{timestamp}"
    shutil.copytree(target, backup)

    source_files = _relative_files(source)
    target_files = _relative_files(target)

    for obsolete in sorted(target_files - source_files, reverse=True):
        (target / obsolete).unlink(missing_ok=True)

    for relative in sorted(source_files):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)

    for directory in sorted(
        [p for p in target.rglob("*") if p.is_dir()],
        key=lambda p: len(p.parts),
        reverse=True,
    ):
        try:
            directory.rmdir()
        except OSError:
            pass

    return backup


def apply_update(approved_sha: str) -> None:
    local = _local_manifest()
    repository = local.get("repository", DEFAULT_REPOSITORY)
    channel = local.get("channel", DEFAULT_CHANNEL)
    skill_path = local.get("skill_path", SKILL_PATH)

    current_head = _branch_head(repository, channel)
    if current_head != approved_sha:
        raise RuntimeError(
            "The canonical branch moved after approval. Refusing to update. "
            "Run `check` again and obtain approval for the newly reported commit."
        )

    remote_manifest = json.loads(
        _remote_text(repository, approved_sha, f"{skill_path}/manifest.json")
    )
    local_version = str(local["version"])
    remote_version = str(remote_manifest["version"])
    if _semver(remote_version) <= _semver(local_version):
        print(
            f"No newer EGCA version is available ({local_version} installed, "
            f"{remote_version} approved)."
        )
        return

    with tempfile.TemporaryDirectory(prefix="egca-update-") as temp_dir:
        temp = Path(temp_dir)
        archive = temp / "egca.zip"
        archive.write_bytes(_request_bytes(_archive_url(repository, approved_sha)))
        package = _package_from_archive(archive, temp / "extracted", skill_path)

        staged_manifest = _load_json(package / "manifest.json")
        if str(staged_manifest.get("version")) != remote_version:
            raise RuntimeError("Staged package version does not match approved manifest")
        if staged_manifest.get("repository") != repository:
            raise RuntimeError("Staged package repository does not match installed source")

        backup = _apply_package(package, _skill_root())

    print(f"Updated EGCA from {local_version} to {remote_version}.")
    print(f"Approved source commit: {approved_sha}")
    print(f"Backup created at: {backup}")
    print("Restart/reload the agent surface if it does not automatically reload skill files.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check for or apply explicitly approved EGCA skill updates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="Read-only update check; never modifies the skill")

    update_parser = subparsers.add_parser(
        "update", help="Apply an update approved for an exact canonical commit"
    )
    update_parser.add_argument(
        "--approved-sha",
        required=True,
        help="Exact source commit shown to and explicitly approved by the user",
    )

    args = parser.parse_args()
    try:
        if args.command == "check":
            _print_check(check_for_updates())
        else:
            apply_update(args.approved_sha)
        return 0
    except (RuntimeError, ValueError, KeyError, urllib.error.URLError, zipfile.BadZipFile) as exc:
        print(f"EGCA update error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
