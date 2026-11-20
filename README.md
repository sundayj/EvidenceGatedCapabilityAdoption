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

One EGCA tracker/program owns one cumulative feature/integration branch. Create it from the authoritative repository baseline before experiments begin.

Each experiment or production adaptation branches from that feature branch and merges back into it only when its evidence gate justifies integration. Rejected experiments remain historical evidence and are not merged into the cumulative branch.

```text
main
  └── feature/<egca-program>
        ├── experiment/e-001-...
        ├── adaptation/e-001-...
        ├── experiment/e-002-...
        └── ...
```

Partial EGCA adoption work must not be merged directly into `main`. The cumulative feature branch is merged into `main` only once the complete capability-adoption program is ready, the program-level final evidence gate passes, and the host repository's current authority requirements are satisfied.

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

## Install in Codex (no Python required)

Choose one way to get the skill folder. None requires Python:

- **GitHub ZIP:** On the [repository page](https://github.com/sundayj/EvidenceGatedCapabilityAdoption), choose **Code → Download ZIP** and extract it. To pin the source, open the exact commit before downloading its archive and keep its SHA.
- **Git:** Clone the repository with `git clone https://github.com/sundayj/EvidenceGatedCapabilityAdoption.git`. To pin the source, check out the exact reviewed SHA in that clone before copying the folder. Keep the checkout's SHA with the installation.

Then:

1. Copy the **whole** `skills/evidence-gated-capability-adoption` folder, not the repository root or just `SKILL.md`, to one of these locations:

   | Scope | Destination folder |
   | --- | --- |
   | One repository | `<your-project>/.agents/skills/evidence-gated-capability-adoption/` |
   | All your local projects | `~/.agents/skills/evidence-gated-capability-adoption/` (Windows: `%USERPROFILE%\.agents\skills\evidence-gated-capability-adoption\`) |

   Create the parent folders if needed. Inside the destination, `SKILL.md`, `manifest.json`, `templates/`, and `examples/` should be direct children. Use the filesystem that runs Codex. If the skill is already installed, don't install a second copy or overwrite it: use the governed update procedure below.

2. Open Codex in your project, type `$evidence-gated-capability-adoption` and select it. Restart Codex if the skill isn't listed, then check the folder layout and scope. See [OpenAI's skill discovery documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

**Already using a recent GitHub CLI?** [`gh skill install`](https://cli.github.com/manual/gh_skill_install) is another **fresh-install** option (preview). Run it from the target project:

```bash
gh skill install sundayj/EvidenceGatedCapabilityAdoption skills/evidence-gated-capability-adoption --agent codex --scope project --pin REF
```

Replace `REF` with the full reviewed commit SHA, then verify the skill in Codex as above. This command manages the copy itself; do not also copy the folder. If your GitHub CLI does not offer `gh skill`, use ZIP or Git. Do not run a general-purpose skill update against an active EGCA installation as a substitute for EGCA's update gate.

**Next:** [Run your first EGCA program and choose where to save it](skills/evidence-gated-capability-adoption/examples/first-program.md). It includes copyable prompts, example outputs, and a fresh-session persistence check.

## Update an existing installation

### Update through the tool that manages your copy (no Python)

- **Project-local, Git-managed skill:** Use an ordinary dependency-bump PR.
  Review the upstream changelog and migration notes and resolve the candidate
  to an exact upstream commit. Retain the old source SHA, stage the complete
  folder from that exact candidate, and review the package diff. Record the
  new source SHA alongside the replacement in the consuming repository.
  Review, test discovery in a disposable checkout, and activate through the
  consuming project's normal merge/release controls. Rolling back that Git
  change restores both the previous package and its recorded source.
- **User-scoped ZIP or Git copy:** Stage the exact new copy outside skill
  discovery folders. Keep a backup of the old folder there as well. Once the
  exact replacement is admitted and authorized, close Codex, replace the
  complete folder at its existing path, and restart to verify discovery. If
  verification fails, restore the backup and confirm discovery again. Don't
  leave two installed copies of the same name.
- **GitHub CLI-managed copy:** [`gh skill update --dry-run`](https://cli.github.com/manual/gh_skill_update)
  can preview changes for CLI-managed skills. A pinned copy intentionally skips
  ordinary updates. Stage and review the exact new revision, then re-pin to
  that revision using the [installer's `--pin` and `--force` options](https://cli.github.com/manual/gh_skill_install)
  only after the existing copy is backed up and the replacement is admitted.
  Keep the original project/user scope. Do not unpin to accept whatever
  happens to be latest.

These are standard **package replacement** paths, not an EGCA admission
verifier. When a governing EGCA policy applies, use that currently active
policy and the host's required authority and evidence before replacement.
Neither a tool refresh nor a human clicking Update is evidence of admission.
If the installed policy requires its legacy updater to validate/apply the
admission, follow that policy; these instructions do not retrofit a new
governance path into old installations.

For an active program, keep its exact governing revision available and pinned:
prefer a project-owned copy, or change the distribution copy only after
confirming that the agent can still load that program's recorded revision.
If that revision cannot be recovered, pause changes to that program rather
than using the newest skill. Upgrading the installed package does not
migrate a program.

### Legacy EGCA-managed automated updates

The original automated checker and admission validator remain available for
existing workflows. **This separate path** still requires Python. From the
folder containing the installed `SKILL.md`, run
`python scripts/egca_update.py check` for a read-only report of the available
version, exact canonical commit, changelog and migration notes.

For the one-time **0.3.1 -> 0.4.0 bootstrap**, 0.3.1 remains the governing methodology. After the exact candidate commit has received the explicit approval required by 0.3.1 and the host grants the update action, run:

```bash
python scripts/egca_update.py update --approved-sha <exact-approved-sha>
```

`--approved-sha` is a bootstrap-only compatibility path. The updater accepts it only while the installed version predates 0.4.0 and refuses it once autonomous update governance is active.

For **subsequent updates governed by installed EGCA 0.4.0 or newer**, an external evidence gate must emit an admission bundle for the candidate digest reported by `check`. Run:

```bash
python scripts/egca_update.py update --admission admission.json
```

The updater locally integrity-checks that bundle: schema and criteria revisions, an `Adopt` decision, the installed governing version, the exact candidate digest, preservation of active-program version pins, a scoped admitting-controller claim, and exactly one passing artifact for each required evidence kind (`compatibility_review`, `migration_review`, `isolated_validation`, `rollback_validation`, and `independent_audit`). Every artifact is path-confined, SHA-256 verified, and bound to the candidate; the independent audit must use a different producer and provenance domain from the admitting controller. The external gate remains responsible for authenticating the claimed principals before writing the bundle.

Both update paths re-check the canonical branch immediately before download. If it moved after approval or admission, the updater refuses the update and requires a fresh check and transition decision. Before replacing package files it creates a sibling backup of the installed skill directory.

There is intentionally no evidence-free or silent self-update mode. Autonomous checking and application are valid only when the versioned mandate, independent evidence, rollback conditions, current host authority, and exact-revision fence are machine-verifiable.

### Updating a pre-0.2 installation

Older copies lack the updater. Follow the currently installed methodology and host permissions to approve the exact replacement revision first. Back up the existing skill folder outside all scanned skill locations, then copy the approved package into the chosen location and verify discovery. Do not replace or reinterpret any active program's governing version.

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
- Humans, agents, services, and hybrid workflows may propose work; actor type alone neither admits nor rejects it.
- Authoritative lifecycle transitions require a machine-verifiable transition mandate binding objective, policy, authority, criteria, object revision, and applicable evidence.
- Self-validation is useful evidence but cannot satisfy a declared independence requirement; independence is established by provenance and failure-domain separation, not actor labels or vote count.
- A methodology or policy candidate cannot govern its own adoption. The current version evaluates the candidate, and historical decisions are not retroactively reinterpreted.
- Every completed experiment ends with **Adopt**, **Adapt**, **Reject**, or **Repeat** and a durable rationale.
- Skill updates may be checked read-only. Installed skill files may change only after the exact proposed source revision passes the current methodology's evidence gate and the host grants the required action.
- Active EGCA programs preserve the methodology version governing historical decisions; global updates do not rewrite history.
- When EGCA work produces a pull request, follow host-repository conventions and, unless expressly disabled, assign the current/authenticated GitHub user and apply clearly appropriate existing labels when possible.
- Consequential merge/deployment actions remain subject to the host project's authority rules. If an external host actually reserves an action for an unavailable principal, record `ExternalBlock`; do not invent a human queue or bypass the host.

## Status

**v0.4 candidate — experimental, with multiple real-world validation runs completed.**

The method originated while evaluating architectural capabilities in a private full-stack application. It has since been exercised on unrelated work, including a public two-repository Jekyll modernization using Google Sheets as durable state and a production workplace case using Git-tracked Markdown. Those runs validated the storage-agnostic design and also changed the methodology itself: they added clearer cumulative-integration rules, environment-blocked validation, experiment execution-log guidance, and a stronger burden of proof for new abstractions.

Version 0.3 added explicit evidence-applicability and productionization gates so prototype or fixture evidence cannot silently become production-readiness evidence. Version 0.4 makes lifecycle governance actor-neutral: capability remains open, while authoritative commitments are constrained by versioned transition mandates, independent evidence, exact-revision fencing, non-circular policy evolution, and explicit external-host authority blocks. It also distinguishes production readiness, merge, deployment, and operational validation in the durable lifecycle.

EGCA remains experimental because the goal is not to freeze the method after a few successful uses. Additional projects, failure cases, multi-agent workflows, team-scale use, and independent repeatable benchmarks should continue to refine the skill and its evidence gates.

## License

MIT. See `LICENSE`.
