# EGCA Goal Prompt Template

Use this template when handing an approved EGCA experiment program to a long-running coding agent.

---

You are executing an **Evidence-Gated Capability Adoption (EGCA)** program against this repository.

## Source of durable project state

Tracker/backend:
`<URL, repository path, database/MCP resource, or other durable location>`

Read the tracker before making changes. Treat it as the source of truth for:

- candidate/research state;
- approved experiment scope;
- experiment IDs and dependencies;
- hypotheses and evidence criteria;
- decision records.

Treat the live repository and observed runtime/test behavior as the source of truth for current implementation reality. If the tracker conflicts with the repository, investigate and record the discrepancy rather than blindly following stale state.

## Objective

`<program objective>`

## Execution rules

1. Work only on experiments marked approved/executable according to the tracker.
2. Respect dependency ordering, but do not reinterpret stable experiment IDs as sequence numbers.
3. Before each experiment, restate:
   - hypothesis;
   - bounded scope;
   - success evidence;
   - rejection evidence.
4. Prefer the smallest implementation capable of producing useful evidence.
5. Do not absorb unrelated cleanup or feature work into the experiment unless necessary to obtain valid evidence; record unavoidable scope changes.
6. Validate with repository-grounded evidence. Passing tests alone are insufficient if the hypothesis concerns UX, performance, architecture, reliability, or another dimension requiring additional evidence.
7. Record negative, ambiguous, and unexpected findings.
8. Do not declare a capability adopted merely because implementation is complete.
9. At the evidence gate choose exactly one:
   - Adopt
   - Adapt
   - Reject
   - Repeat
10. Update the tracker after meaningful progress and at every experiment decision.
11. Preserve historical IDs and previous decisions.
12. When opening or updating a pull request, follow repository-specific conventions first. Unless the user or repository instructions expressly say otherwise, assign the PR to the current/authenticated GitHub user when safely resolvable and apply all clearly appropriate existing labels. Do not create labels merely to satisfy this rule unless requested. Record any inability to assign or label because of permissions, missing labels, or unresolved identity.
13. Record the branch/PR reference in durable EGCA state.
14. Stop before merge, deployment, destructive migration, publication, or any consequential action requiring human approval under repository instructions.

## Repository workflow

Base branch:
`<base branch>`

Experiment branch convention:
`<convention, e.g. egca/E-XXX-short-name>`

Pull-request conventions:
```text
Assignee: current/authenticated GitHub user unless expressly disabled
Labels: apply appropriate existing repository labels based on the work
Draft/review behavior: follow host-repository governance
```

Validation commands:
```text
<tests / linters / build / benchmark commands>
```

## Completion criteria

The goal is complete only when:

- every approved experiment in scope has either completed or has a clearly documented blocker;
- evidence is recorded for each completed experiment;
- each completed experiment has an Adopt / Adapt / Reject / Repeat decision;
- the decision log is updated;
- follow-up dependencies/priorities are updated without renumbering experiments;
- any experiment PR has the expected assignee and appropriate existing labels unless expressly disabled or impossible, with limitations recorded;
- repository changes are left in the state required by the host project's governance rules.

At the end, report:

1. experiments executed;
2. changes made;
3. validation evidence;
4. evidence-gate decisions;
5. blockers or uncertainty;
6. tracker updates;
7. branch/PR references, assignee/label state, and any PR-hygiene limitations;
8. recommended next experiment(s), if justified by evidence.
