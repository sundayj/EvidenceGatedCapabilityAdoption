# Repository Instructions

## Purpose

This repository defines and distributes **Evidence-Gated Capability Adoption (EGCA)** as a reusable engineering methodology and Agent Skill.

## Source of truth

- `SKILL.md` defines agent behavior.
- `references/methodology.md` defines methodology rationale and terminology.
- `templates/` defines reusable human/agent records.
- `schemas/` defines machine-readable interchange contracts.
- `examples/` demonstrates the method without exposing private source systems.

Keep these layers consistent. When behavior changes in `SKILL.md`, update supporting methodology/templates if the change affects their contract.

## Methodology invariants

Do not weaken these without an explicit methodology decision:

- candidate does not mean committed work;
- investigate before experimenting;
- experiments require falsifiable hypotheses;
- use the smallest bounded experiment that can produce meaningful evidence;
- stable experiment IDs are independent of priority/order;
- repository/observed behavior outranks stale tracker assumptions;
- agent self-report is not sufficient evidence;
- completed experiments end in Adopt, Adapt, Reject, or Repeat;
- preserve negative results and decision rationale.

## Public-safety boundary

The methodology was initially derived from work on a private application. Do not copy private repository paths, personal/financial data, credentials, private URLs, provider/account details, or materially reconstructable implementation details into this public repository.

Use sanitized capability-level examples.

## Change discipline

EGCA is itself experimental. Significant methodology changes should state:

1. the problem in the current method;
2. the proposed change;
3. expected improvement;
4. evidence supporting the change;
5. whether the change is backward-compatible with existing trackers.

Prefer testing important methodology changes on a real use case before presenting them as stable.
