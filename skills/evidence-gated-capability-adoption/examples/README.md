# Examples

This directory will contain public-safe examples showing how EGCA behaves in practice.

## Planned examples

### 1. Minimal synthetic example

A small, fully public example demonstrating the entire lifecycle from Candidate through Decision without any private-system context.

### 2. Sanitized real-world case study

A derived example based on the capability-adoption tracker that originally motivated EGCA.

The public version should preserve:

- candidate versus committed-work separation;
- source investigation;
- falsifiable hypotheses;
- stable experiment IDs;
- dependencies and execution priority;
- success/rejection evidence;
- observed results;
- Adopt / Adapt / Reject / Repeat decisions;
- decision-history structure.

It must remove or generalize:

- private repository paths and implementation details;
- credentials, account/provider details, private URLs, or personal data;
- source excerpts that should not be redistributed;
- information that would make a private application materially reconstructable.

## Why include a real example?

A blank tracker teaches the schema. A real historical example teaches the behavior: how hypotheses evolve, how experiment ordering changes without renumbering IDs, how negative evidence is retained, and how a promising candidate can remain unadopted until the evidence gate is crossed.

The original private tracker should remain intact as historical evidence. Public examples should be derived artifacts rather than edits to the original.