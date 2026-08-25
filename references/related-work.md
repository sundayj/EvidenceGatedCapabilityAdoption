# Related work and adjacent tools

EGCA is a synthesis of established engineering practices, and it should be compared openly with contemporary tools that attack similar failure modes.

## Ponytail

[Ponytail](https://github.com/DietrichGebert/ponytail) is an agent ruleset and skill suite designed to reduce over-engineering by making coding agents prefer the least code that safely solves the task. Its decision ladder asks, in order, whether the work needs to exist, whether the codebase already solves it, whether the standard library/platform/current dependencies solve it, and only then what minimum new code is required. Ponytail also provides diff/repository audits for over-engineering and a debt ledger for intentionally deferred shortcuts.

Ponytail and EGCA materially overlap in one important area: both push investigation and reuse ahead of speculative implementation. That overlap should be treated as related prior art, not hidden behind terminology differences.

The primary distinction is the level of decision being controlled:

| Concern | Ponytail | EGCA |
| --- | --- | --- |
| Primary objective | Minimize unnecessary implementation | Minimize unjustified architectural/capability commitment |
| Typical unit | Coding task, diff, or repository cleanup | Capability, architecture decision, dependency, integration, or multi-experiment program |
| Core bias | Smallest sufficient implementation | Evidence-backed adoption decision |
| Existing primitives | Prefer reuse before adding code | Investigate existing system/source before forming the experiment |
| Experimental evidence gate | Not the organizing mechanism | Required when meaningful uncertainty remains |
| Valid outcome can add architecture | Possible, but not the central framing | Explicitly yes when evidence justifies it |
| Rejection | Usually avoid/delete unnecessary implementation | First-class Adopt / Adapt / Reject / Repeat decision with durable rationale |
| Durable decision history | Includes a deferred-shortcut/debt ledger | Core project state: hypotheses, evidence, decisions, dependencies, and program lineage |
| Cumulative capability integration | Not a primary concern | Explicit integration branch and program-level final gate |

The most useful shorthand is:

> **EGCA decides what earns adoption. Ponytail helps keep the experiment or accepted implementation from overbuilding the answer.**

They are therefore complementary rather than mutually exclusive. An EGCA experiment can run under Ponytail-style implementation constraints so that the experiment itself does not manufacture unnecessary complexity. Conversely, an EGCA evidence gate may conclude that a new abstraction or additional architecture is justified; EGCA is not a minimum-lines-of-code methodology.

### Benchmark note

Ponytail publishes agentic benchmarks reporting lower source-code volume, token use, cost, and execution time while maintaining its tested safety floor. Those measurements are useful evidence about Ponytail itself, but EGCA does not treat third-party benchmark claims as automatically transferable to another repository, model, or task mix. If Ponytail is considered for an EGCA program, evaluate it against the target system's own baseline and evidence criteria.

References:

- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- https://github.com/DietrichGebert/ponytail/blob/main/AGENTS.md
- https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/agentic/README.md

## Predeclared implementation boundaries

A related practical technique is to constrain a coding agent with an explicit implementation surface before execution—for example, a list of permitted function names and their inputs/outputs, allowed files, or an interface budget. The agent is instructed to stop and explain why the boundary is insufficient rather than silently adding new functions, layers, or subsystems.

This concrete technique was suggested to the EGCA project during an [r/codex discussion](https://www.reddit.com/r/codex/comments/1vxyfin/comment/p5sjtbp/) after the methodology was published. The commenter described defining the permitted function names and their input/output contracts, then requiring the agent to stop and explain if the task could not reasonably be completed within that constraint. That suggestion prompted its inclusion here. This attribution is for the contribution to EGCA's evolving practice, not a claim that the commenter originated the broader ideas of interface constraints, design by contract, or bounded implementation.

This is useful inside EGCA as an **experiment-bounding technique**, especially when the hypothesis can be tested through a known interface. It reduces implementation drift and makes scope expansion visible to the human reviewer.

It should not be applied mechanically. Investigation comes first. A prematurely frozen function list can encode the wrong architecture and prevent the experiment from discovering that an existing primitive or a different interface is better. Use predeclared boundaries when they help test the hypothesis; treat a justified request to cross the boundary as evidence to review, not automatically as agent failure.
