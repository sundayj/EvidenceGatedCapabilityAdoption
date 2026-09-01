# Examples

This directory contains public-safe examples showing how EGCA behaves in practice.

## Available case studies

### Prototype evidence and the productionization gap

[`delivery-board-productionization-gap-case-study.md`](delivery-board-productionization-gap-case-study.md) records a sanitized production UI case where accepted fixture and static-prototype evidence did not cover real relationship cardinality or shared-component accessibility and responsive defaults. It distinguishes valid bounded experiment evidence from production readiness and motivates EGCA's evidence-applicability, productionization-delta, traceability, and release-state contracts.

### Selective delegated agent routing

[`payspan-delegated-agent-routing-case-study.md`](payspan-delegated-agent-routing-case-study.md) records a PaySpan EGCA closeout where a Codex parent agent used selective model/reasoning delegation. The case study preserves repository-verifiable timing and validation evidence, distinguishes user-observed usage metrics from repository evidence, and records the durable-state closeout failure that required a later connector repair.

It also defines a prospective comparison hypothesis between selective non-overlapping delegation and symmetric iterative adversarial review loops.

## Planned examples

### Minimal synthetic example

A small, fully public example demonstrating the entire lifecycle from Candidate through Decision without any private-system context.

### Additional sanitized real-world case studies

Derived examples based on capability-adoption trackers that exercise different EGCA conditions.

Public examples should preserve:

- candidate versus committed-work separation;
- source investigation;
- falsifiable hypotheses;
- stable experiment IDs;
- dependencies and execution priority;
- success/rejection evidence;
- observed results;
- Adopt / Adapt / Reject / Repeat decisions;
- decision-history structure;
- execution telemetry when it is relevant to the case-study hypothesis.

They must remove or generalize:

- private repository paths and implementation details;
- credentials, account/provider details, private URLs, or personal data;
- source excerpts that should not be redistributed;
- information that would make a private application materially reconstructable.

## Why include real examples?

A blank tracker teaches the schema. A real historical example teaches the behavior: how hypotheses evolve, how experiment ordering changes without renumbering IDs, how negative evidence is retained, how execution economics can be measured, and how a promising candidate can remain unadopted until the evidence gate is crossed.

Original trackers should remain intact as historical evidence. Public examples should be derived artifacts rather than edits to private source records.
