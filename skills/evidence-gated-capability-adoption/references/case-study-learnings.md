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
