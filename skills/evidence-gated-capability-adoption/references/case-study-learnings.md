# Case-study learnings

EGCA is being refined through real use rather than treated as a fixed process. These notes capture reusable findings without exposing private application or employer-specific implementation details.

## Architecture deflation and burden of proof

Agent-assisted development makes speculative architecture cheap to generate. New models, services, registries, engines, and abstractions can appear reasonable before the existing system has been inspected deeply enough.

EGCA counters this by requiring the smallest experiment that can determine whether existing primitives already satisfy the capability. New complexity should earn adoption through evidence.

This is not a minimal-code rule. In a separate production-development case, narrow fixes were tested first; repeated experiments then justified a small shared typed abstraction while a broader generalized registry remained deferred. EGCA should be capable of both removing unnecessary architecture and justifying the smallest abstraction that evidence supports.

## Storage portability

The methodology has now been exercised with both:

- Google Sheets as shared durable state across human, ChatGPT, and coding-agent work; and
- Git-tracked Markdown as durable state in a separate production-development environment.

This supports treating storage as an adapter. The invariant is durable, inspectable project/decision state, not a particular tool.

## Validation outcomes

Do not collapse an environment blocker into negative evidence. Record at least these distinct situations:

- evidence supports the hypothesis;
- evidence weakens or falsifies the hypothesis;
- evidence is insufficient;
- validation is blocked by the environment.

A blocked test, missing service, unavailable fixture, CI outage, or inaccessible dependency means the intended evidence was not collected.

## Lightweight execution log

Experiments benefit from a small provenance log containing meaningful events such as:

- commands/test suites executed;
- observed results and failures;
- environment blockers;
- unexpected findings;
- relevant commits, branches, and PRs.

The log should remain concise. It is evidence provenance, not a transcript of agent activity.

## Incidental improvements

Experiments may expose defects in test harnesses, documentation, tooling, or workflow. Those improvements may be retained when useful, but they must be recorded separately from evidence for the hypothesis. Fixing the measuring apparatus does not prove the capability under test.

## Overlapping experiments and integration

A follow-on experiment may begin before earlier work reaches production when dependencies are explicit and experiment-specific evidence remains reconstructable. Preserve isolated experiment branches/commits and record the cumulative baseline used. Accepted/adapted work should converge on the program integration branch before the final program-level gate.

## Prototype-to-production evidence transfer

A full sanitized public case study accompanies this distilled learning in the methodology repository's `examples/` directory.

A production UI case exposed two classes of defect after static semantic/projection prototypes had already passed their experiments: real relationship cardinality invalidated an assumed grouping edge, and shared list/Markdown component defaults produced accessibility and responsive-identity defects that friendly fixtures did not exercise.

The experiments were not wrong about the artifacts they tested. The failure was allowing prototype evidence to cross into a materially different production implementation without a linked productionization gate.

The expected improvement is earlier discovery of integration-specific defects without forcing teams to repeat already-resolved architectural research. Requiring a full new EGCA program for every implementation was rejected as unnecessary ceremony; relying on post-merge production validation was rejected because safely testable defects should be found before release.

Reusable conclusions:

- Record the artifact/environment and evidence applicability boundary for every experiment.
- Treat Adopt as "adopt as tested," not unrestricted production approval.
- Carry accepted evidence forward, but isolate the productionization delta in a linked experiment/adaptation.
- Trace accepted criteria to production code, adversarial fixtures, direct assertions, and branch-matched runtime evidence.
- Include counterexamples for real input shapes, relationship cardinality, shared-component defaults, permissions, degraded states, responsive behavior, and accessibility when those variables are material.
- Keep production readiness, merge, deployment, and operational validation as distinct facts.

This clarification is backward-compatible with historical decisions: their evidence remains valid within the scope actually tested. Active programs should add applicability and productionization records prospectively rather than rewriting prior verdicts.

## Methodology feedback loop

Real EGCA programs should be allowed to change EGCA itself:

```text
skill/methodology
    -> real project
    -> observed friction or missing state
    -> durable case-study note
    -> methodology change
    -> next real project
```

Changes to EGCA should still carry their own burden of proof. A single inconvenience need not become permanent ceremony; repeated or consequential findings should drive revisions.

## Inviting case-study contributions

Case-study invitations should help the methodology learn from real programs without turning closeout into another approval ceremony.

Invite a contribution only when the run has durable evidence and a reusable lesson, such as meaningful negative evidence, a surprising boundary condition, a consequential Adapt/Reject/Repeat result, measurable execution evidence, or a methodology correction. Routine work and conclusions already represented by an existing case study do not need an invitation.

The invitation should happen once, at the end of the final report, and must not block program completion. Omit it when the user has already authorized, declined, or prohibited a case study. State the specific lesson that may be useful rather than making a generic request for content.

Keep permissions distinct:

1. permission to prepare a sanitized draft;
2. permission to place that draft in a repository;
3. permission to push, publish, or open a contribution pull request.

One permission does not imply the next. Repository access, implementation approval, or a previous contribution is not publication consent.

A public case study should:

- remain a derived artifact rather than replace or rewrite the original evidence;
- remove private repository paths, organizations, people, tickets, credentials, private URLs, customer information, and materially reconstructable operational details;
- preserve hypotheses, evidence boundaries, negative findings, decisions, rejected alternatives, and remaining uncertainty;
- distinguish repository-verifiable evidence from participant recollection or inference;
- receive a final privacy and accuracy review before publication.

Do not invite or prepare a public contribution when meaningful sanitization would destroy the evidence or still expose sensitive context.
