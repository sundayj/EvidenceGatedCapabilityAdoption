# Evidence-Gated Capability Adoption (EGCA)

Evidence-gated methodology and reusable agent skill for evaluating and adopting software capabilities through bounded experiments.

## What EGCA is

EGCA is a practical engineering method for deciding whether a capability, architectural pattern, dependency, integration, or design idea actually belongs in an existing system.

A candidate does **not** become committed implementation work merely because it sounds useful, appears in a respected source project, or an agent recommends it. It advances through investigation, a falsifiable hypothesis, a bounded experiment, observed evidence, and an explicit decision gate.

```text
Candidate
  -> Investigate
  -> Hypothesize
  -> Design the smallest useful experiment
  -> Execute + validate
  -> Evidence gate
  -> Adopt / Adapt / Reject / Repeat
  -> Record the decision
```

EGCA combines ideas from hypothesis-driven development, technical/architectural spikes, Lean experimentation, evolutionary architecture, and Architecture Decision Records. The name describes this particular synthesis; it does not claim those underlying practices are new.

## Branching model

One EGCA tracker/program owns one cumulative feature/integration branch. Create it from the approved repository baseline before experiments begin.

Each experiment or production adaptation branches from that feature branch and merges back into it only when its evidence gate justifies integration. Rejected experiments remain historical evidence and are not merged into the cumulative branch.

```text
main
  └── feature/<egca-program>
        ├── experiment/e-001-...
        ├── adaptation/e-001-...
        ├── experiment/e-002-...
        └── ...
```

Partial EGCA adoption work must not be merged directly into `main`. The cumulative feature branch is merged into `main` only once the complete capability-adoption program is ready, the program-level final evidence gate passes, and the host repository's normal approval requirements are satisfied.

This isolation is deliberate: an experiment can validate one piece of an architecture without making that partial architecture a production baseline for unrelated work.

## Evidence boundaries and productionization

EGCA decisions apply only to the artifact, environment, data shapes/scale, integration path, and operational conditions actually tested. Adopting a static prototype, fixture, documentation contract, isolated module, or mocked integration does not automatically establish that a materially different live implementation is production-ready.

Carry accepted evidence forward without repeating resolved discovery. When implementation introduces material untested variables, create a linked productionization experiment or adaptation that isolates the delta, exercises adversarial cases, and traces each accepted criterion to production code, automated evidence, and branch-matched runtime evidence.

Track production readiness, merge, deployment, and operational validation separately. No state implies the next.

## Why this repository exists

This repository has two goals:

1. Define EGCA precisely enough that a human or coding agent can reproduce it on an unrelated project.
2. Package the method as a portable Agent Skill with templates and machine-readable conventions.

The method is deliberately **storage-agnostic**. Google Sheets, Git-tracked files, issue trackers, or a database can all serve as durable EGCA state if they preserve the required concepts.

## Install in Codex

The installable skill lives at:

```text
skills/evidence-gated-capability-adoption
```

The `SKILL.md` includes the YAML frontmatter Codex requires (`name` and `description`). Codex installs skills under `$CODEX_HOME/skills`, which defaults to `~/.codex/skills`.

### Recommended: ask Codex to install it

In Codex, ask:

```text
Use $skill-installer to install the skill from
https://github.com/sundayj/EvidenceGatedCapabilityAdoption/tree/main/skills/evidence-gated-capability-adoption
```

Codex's built-in skill installer accepts GitHub repository paths and installs the selected directory into your Codex skills directory.

After installation, restart Codex so it reloads the skill list.

### Install with the built-in installer script

If you are invoking Codex's bundled installer manually, use the repository plus the skill path:

```bash
python3 scripts/install-skill-from-github.py \
  --repo sundayj/EvidenceGatedCapabilityAdoption \
  --path skills/evidence-gated-capability-adoption
```

Run that command from the bundled `skill-installer` skill directory (the exact location is Codex-version dependent).

### Check for skill updates

Beginning with EGCA 0.2.0, the installed package contains a read-only update checker:

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/evidence-gated-capability-adoption"
python scripts/egca_update.py check
```

The checker reports the installed version, available version, exact canonical Git commit, changelog, and migration notes. It **does not modify any files**.

An agent may run this check and explain the proposed update. It must obtain explicit user approval for the exact commit shown before applying anything.

After approval:

```bash
python scripts/egca_update.py update --approved-sha <exact-approved-sha>
```

The updater re-checks the canonical branch. If the branch moved after approval, it refuses the update and requires a fresh check and new approval. Before replacing package files it creates a sibling backup of the installed skill directory.

There is intentionally no unattended or silent self-update mode.

### Updating a pre-0.2 installation

Older installations do not contain the updater. The built-in installer intentionally refuses to overwrite an existing skill directory, so remove the old copy first:

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/evidence-gated-capability-adoption"
```

Then reinstall from the canonical skill path above and restart/reload Codex.

If you previously copied this repository root directly into `~/.codex/skills/evidence-gated-capability-adoption`, reinstall from the `skills/evidence-gated-capability-adoption` path so future packaging changes remain isolated from repository-level documentation.

### Verify the installation

Check that the installed skill starts with valid frontmatter:

```bash
sed -n '1,8p' "${CODEX_HOME:-$HOME/.codex}/skills/evidence-gated-capability-adoption/SKILL.md"
```

It should begin with:

```yaml
---
name: evidence-gated-capability-adoption
description: ...
---
```

The installed package should also contain:

```text
manifest.json
scripts/egca_update.py
```

## Distribution direction

The repository remains the canonical source. EGCA currently supports standalone Agent Skill installation, while the long-term preferred distribution target is a versioned, skill-only plugin so eligible users can discover/install it through supported ChatGPT and Codex plugin surfaces.

A repository-local copy remains useful when a project needs to pin its EGCA methodology version. A global skill/plugin update must not silently reinterpret historical experiments in an active EGCA program.

See [`ROADMAP.md`](ROADMAP.md) for plugin packaging, release hardening, methodology-version pinning, and validation work.

## Repository layout

```text
.
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── MIGRATIONS.md
├── AGENTS.md
├── LICENSE
├── SKILL.md                         # root-compatible copy
├── references/                      # repository-level source/reference copy
├── templates/                       # repository-level source/template copy
├── schemas/
├── examples/
└── skills/
    └── evidence-gated-capability-adoption/   # canonical installable skill
        ├── SKILL.md
        ├── manifest.json
        ├── scripts/
        │   └── egca_update.py
        ├── references/
        ├── templates/
        ├── schemas/
        └── examples/
```

The nested directory is the canonical Codex-installable package. The root copies remain convenient for browsing and development of the methodology repository itself.

## Core invariants

- Candidates are possibilities, not commitments.
- Investigate the source and current system before designing an experiment.
- Every experiment must test a falsifiable hypothesis.
- Every decision is bounded by the artifact, environment, data, integration, and operational conditions actually tested.
- Materially different production implementations require a linked productionization experiment/adaptation rather than inheriting prototype evidence silently.
- Accepted criteria must be traceable to production code and direct evidence before a program is production-ready.
- Prefer the smallest bounded change that can produce meaningful evidence.
- Stable experiment IDs are independent of execution priority.
- One EGCA program uses one cumulative feature/integration branch.
- Experiment and adaptation branches target that feature branch, not `main`.
- `main` remains free of partial EGCA adoption work until the program-level final evidence gate passes.
- Repository reality and measured behavior outrank tracker assumptions.
- An agent's assertion is not evidence.
- Every completed experiment ends with **Adopt**, **Adapt**, **Reject**, or **Repeat** and a durable rationale.
- Skill updates may be checked read-only, but installed skill files may change only after explicit approval of the exact proposed source commit.
- Active EGCA programs preserve the methodology version governing historical decisions; global updates do not rewrite history.
- When EGCA work produces a pull request, follow host-repository conventions and, unless expressly disabled, assign the current/authenticated GitHub user and apply clearly appropriate existing labels when possible.
- Consequential merge/deployment actions remain subject to the host project's approval rules.

## Status

**v0.3 — experimental, with multiple real-world validation runs completed.**

The method originated while evaluating architectural capabilities in a private full-stack application. It has since been exercised on unrelated work, including a public two-repository Jekyll modernization using Google Sheets as durable state and a production workplace case using Git-tracked Markdown. Those runs validated the storage-agnostic design and also changed the methodology itself: they added clearer cumulative-integration rules, environment-blocked validation, experiment execution-log guidance, and a stronger burden of proof for new abstractions.

Version 0.3 adds explicit evidence-applicability and productionization gates so prototype or fixture evidence cannot silently become production-readiness evidence. It also distinguishes production readiness, merge, deployment, and operational validation in the durable lifecycle.

EGCA remains experimental because the goal is not to freeze the method after a few successful uses. Additional projects, failure cases, multi-agent workflows, team-scale use, and independent repeatable benchmarks should continue to refine the skill and its evidence gates.

## License

MIT. See `LICENSE`.
