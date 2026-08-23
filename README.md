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

## Why this repository exists

This repository has two goals:

1. Define EGCA precisely enough that a human or coding agent can reproduce it on an unrelated project.
2. Package the method as a portable Agent Skill with templates and machine-readable conventions.

The method is deliberately **storage-agnostic**. Google Sheets, Git-tracked files, issue trackers, or a database can all serve as durable EGCA state if they preserve the required concepts.

## Repository layout

```text
.
├── SKILL.md
├── references/
│   └── methodology.md
├── templates/
│   ├── tracker-schema.md
│   ├── candidate-template.md
│   ├── source-investigation-template.md
│   ├── experiment-template.md
│   ├── decision-record-template.md
│   └── goal-prompt-template.md
├── schemas/
│   └── experiment.schema.json
└── examples/
    └── README.md
```

## Core invariants

- Candidates are possibilities, not commitments.
- Investigate the source and current system before designing an experiment.
- Every experiment must test a falsifiable hypothesis.
- Prefer the smallest bounded change that can produce meaningful evidence.
- Stable experiment IDs are independent of execution priority.
- Repository reality and measured behavior outrank tracker assumptions.
- An agent's assertion is not evidence.
- Every completed experiment ends with **Adopt**, **Adapt**, **Reject**, or **Repeat** and a durable rationale.
- Consequential merge/deployment actions remain subject to the host project's approval rules.

## Status

**v0.1 — experimental.**

The initial method was developed while evaluating architectural capabilities in a private full-stack application. Before calling EGCA stable, the skill should be used to bootstrap at least one unrelated capability-adoption program and refined from that evidence.

## License

MIT. See `LICENSE`.
