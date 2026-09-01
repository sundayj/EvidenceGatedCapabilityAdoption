# Native collaboration spine — sanitized EGCA case study

> This is a sanitized derivative of a private engineering tracker. The private
> tracker, raw benchmark, source history, and decision record remain
> authoritative. Organization names, repository paths, branches, commits,
> credentials, provider/account details, personal data, and reconstructable
> application-specific identifiers have been removed or generalized.

## Summary

An internal operations platform needed Slack-like team communication without
silently committing to Slack's entire feature and operating surface. The
program compared a small native, entity-aware collaboration layer with a
self-hosted full-platform integration, then ran one bounded experiment against
the native prerequisite.

The experiment passed its six pre-recorded gates and produced an **Adopt within
the tested boundary** decision for a PostgreSQL-backed room/thread spine. That
decision did not claim production readiness. A separate, stable
productionization experiment remains required for authenticated HTTP,
per-recipient Redis/SSE delivery, reconnect behavior, and a real browser.

The main methodological result was the separation of three states that are
often collapsed: a capability can pass, be adopted as tested, and integrate
into a cumulative feature branch while productionization, deployment, and
operational validation remain incomplete.

## Context

The host platform already had useful primitives:

- canonical workforce identity and role checks;
- PostgreSQL as durable application truth;
- server-sent events for low-latency invalidation;
- an in-app/email notification preference plane;
- established navigation, drawer, and accessibility conventions; and
- entity-specific authorization for business records.

It did not have a safe multi-user conversation log. Existing per-user chat
state was optimized for assistant history, not room membership, shared
ordering, unread progress, or cross-user authorization.

The product question was deliberately narrower than “build Slack”:

> Can the host platform safely support one internal team room with durable
> messages, shallow threads, mentions, unread progress, entity links, and
> reconnect-safe updates without creating a second collaboration platform in
> disguise?

## Candidate framing

Two candidates remained live:

1. A native collaboration layer composed from the host platform's identity,
   authorization, PostgreSQL, realtime, notification, and UI primitives.
2. A self-hosted full collaboration platform integrated behind the host
   platform's identity and entity context.

The full-platform candidate was not rejected. It remains the fallback if
validated launch requirements include calls, native mobile clients, external
guests, federation, legal hold, compliance export, or plugin breadth that
would make a bounded native layer uneconomic.

## Execution policy

The work used cumulative integration isolation:

- a parent feature branch held only accepted increments;
- the bounded experiment ran on a child branch based on that parent;
- the experiment could return only to the parent after a terminal evidence
  record and explicit decision; and
- no experiment branch targeted the mainline directly.

One coding agent performed investigation, implementation, validation, and
documentation. No subagents were delegated. Human input approved the bounded
experiment, clarified deferred search scope, and authorized a mandatory
methodology update at an exact source revision. No push, mainline merge,
deployment, production-data access, or external communication occurred.

## Falsifiable hypothesis

A bounded native implementation could support one roster-derived room with
durable messages, one-level replies, server-resolved mentions, unread progress,
entity links, and reconnect-safe realtime invalidation while:

- denying all room surfaces to a non-member;
- rechecking linked-entity authorization on write and read;
- producing exactly one durable row for an idempotent retry;
- preserving deterministic per-room order under concurrency;
- reconstructing missed messages from PostgreSQL when realtime was absent;
- meeting a fixed, index-backed 100 ms p95 read budget at 10,000 room messages;
- preserving notification-producer constraints; and
- supporting the bounded interaction with keyboard and screen-reader semantics.

## Evidence boundary

The tested artifact used the intended schema, service, API handler,
notification, realtime topic, navigation declaration, and UI component. It was
not a throwaway prototype.

Runtime evidence covered:

- an isolated PostgreSQL 18 database on a developer workstation;
- 10,000 visible-room messages and 2,500 inaccessible-room messages;
- 20% replies and 200 entity-link rows in the benchmark fixture;
- Python service calls against the real database;
- a supported Node runtime with component tests in jsdom; and
- repository notification, navigation, and QA contracts.

It did not cover production data or hardware, deployed authentication,
Redis-backed event routing, real EventSource behavior, a real browser, room
administration, search, attachments, direct messages, retention, calls,
guests, native mobile, federation, legal hold, or compliance export.

## Repository-observed validation

### Authorization and principal integrity

Adversarial tests exercised both direct service calls and HTTP handlers. A
non-roster principal could not enumerate rooms, fetch history, fetch a thread,
send, or advance read progress. Supplying actor-like fields in a request body
did not change the authenticated actor.

An unauthorized entity link was rejected before a database write. Authorized
links were rechecked at read time so room membership did not permanently grant
access to an entity whose visibility later changed. Private realtime
invalidations were stamped only for active recipients.

### Durability, ordering, and degraded realtime

Against real PostgreSQL:

- 12 concurrent retries of one client command produced one message row;
- 24 distinct concurrent commands produced contiguous room sequence values;
- a fresh service read reconstructed all 25 durable messages; and
- 50 per-recipient realtime publication attempts were made to report
  unavailable without blocking any write or database catch-up.

The UI retained existing history while realtime was disconnected, exposed a
factual reconnecting state, caught up from the last observed sequence, and did
not duplicate replayed content.

### Query shape and performance

The benchmark fixed its threshold before measurement: both first-page and
cursor-page reads had to remain index-backed and below 100 ms server-side at
p95 over 100 measured samples after warmup.

Observed results:

| Query | Returned rows | p95 | Gate |
|---|---:|---:|---:|
| First page | 50 | 2.641 ms | Pass |
| Cursor page | 200 | 7.995 ms | Pass |

Both plans used the intended room/sequence and thread indexes. No row from the
inaccessible room was returned. The generator removed its fixture, and an
independent count confirmed zero residual message, room, and membership rows.

These numbers characterize the recorded local fixture only. They are not
production latency claims.

### Notification and interaction contracts

The mention path used the existing in-app/email preference plane rather than
creating another external-channel producer. Its deep link named the room,
containing thread, and exact message, including a reply target.

Terminal focused validation recorded:

- 204 backend tests passed with one expected failure;
- 157 component/navigation tests passed;
- 18 QA-harness tests passed;
- eight focused collaboration-surface tests passed;
- TypeScript checking passed;
- the notification registry was clean across more than 200 send sites; and
- the generated navigation manifest was current across more than 80 tabs.

The UI checks covered loading, empty, error, keyboard mention selection,
record linking, idempotent send shape, thread focus restoration, exact-reply
focus, reconnect announcements, degraded realtime, and critical accessibility
violations.

## Failure and correction sequence

Passing evidence was not linear. Five corrections materially improved the
tested artifact or the quality of its proof:

1. A generated route inventory had to be regenerated after the API surface was
   added.
2. Accessibility checking exposed invalid list semantics in a keyboard mention
   chooser.
3. Navigation contracts exposed an icon/density mismatch and stale generated
   declarations.
4. The initial mention target could identify a message but not the containing
   thread for replies; the server target and UI proof were made reply-aware.
5. The exact-reply test revealed an over-narrow fixture type; static checking
   rejected it before the terminal run.

A separate benchmark rerun was environmental: the restricted command sandbox
could not reach the intentionally isolated database. The unchanged benchmark
passed once explicitly allowed to access that local container. The ledger kept
this distinct from product rework.

## Productionization delta discovered

The experiment used production-shaped modules, but two seams remained mocked or
direct:

- browser tests mocked HTTP and SSE at the component boundary; and
- real-database tests invoked the service directly rather than traversing the
  deployed authentication and HTTP adapters.

Therefore, the next experiment was not “repeat everything in a bigger test.” It
was defined as the smallest material delta:

1. authenticated HTTP with two principals;
2. per-recipient Redis/SSE delivery;
3. deliberate realtime interruption while database writes continue;
4. ordered PostgreSQL catch-up after reconnect; and
5. a real browser completing the keyboard and accessibility flow.

This delta received a stable experiment identity but no execution approval.

## Decision and alternatives rejected

The bounded capability received `Adopt`, not `Adapt`, because every gate passed
without weakening a threshold or changing the core design. The unresolved
integrated runtime is a named productionization delta rather than counterevidence
against the tested service model.

Several shortcuts were rejected:

- adopting the full breadth of an external collaboration platform before the
  product requirements justified it;
- treating per-user JSON state as a shared durable log;
- treating Redis or SSE delivery as message truth;
- inferring authorization safety from route checks alone;
- adding search before a membership- and revocation-safe index path existed;
  and
- treating isolated database plus jsdom success as production readiness.

## What the evidence supports

Within the recorded boundary, the evidence supports:

- a relational room/message spine as the native architectural direction;
- service-layer actor, membership, and entity authorization;
- atomic idempotency and deterministic room sequencing;
- PostgreSQL cursor catch-up with realtime used only for latency;
- registered in-app/email mention delivery; and
- the bounded accessible Team Chat interaction.

## What the evidence does not prove

The evidence does not prove:

- production readiness or deployment safety;
- authentication integrity through the complete deployed stack;
- private Redis/SSE behavior under real reconnects;
- production-scale latency, retention, backup, or incident recovery;
- room governance, moderation, edits/deletes, attachments, or search safety;
- that the native candidate remains preferable if broader launch requirements
  are confirmed; or
- post-deploy adoption, reliability, or operational fitness.

## Mid-program methodology update

The program began under EGCA 0.2 and was required to update to EGCA 0.3 during
execution. The migration was prospective: historical approvals retained their
original governing version, while subsequent work added explicit evidence
applicability, productionization status, criterion-to-code/runtime traceability,
lifecycle separation, and execution telemetry.

That update changed the quality of the decision. Without the new
productionization fields, it would have been easy to report “all gates pass” as
“ready.” Instead, the record can state all of the following without
contradiction:

| Lifecycle state | Outcome |
|---|---|
| Bounded experiment complete | Yes |
| Capability decision | Adopt within evidence boundary |
| Integrated into cumulative feature branch | Yes |
| Productionization validated | No |
| Production-ready | No |
| Merged to mainline | No |
| Deployed / operationally validated | No |

## Execution telemetry

- Primary executor: one coding agent
- Delegations: 0
- Exact serving model/tier and reasoning level: not exposed
- Human active time: not measured
- Interactive elapsed time: discontinuous and therefore not inferred from
  commit timestamps
- Corrective passes: 5 product/evidence corrections
- Environment-only reruns: 1
- Usage telemetry: a runtime checkpoint was preserved in the authoritative
  private ledger; the resumed total was unavailable and was not invented

## Remaining uncertainty

The next decision depends on evidence, not momentum:

- Can the integrated auth/HTTP/Redis/browser path preserve the already accepted
  invariants?
- Which roles may create rooms, manage membership, moderate content, and set
  retention?
- Are broader platform features launch requirements?
- If search is approved, can its real index/query path prove zero leakage of
  content, snippets, counts, and suggestions after membership or entity-access
  revocation?

Until those questions are answered, the native spine is an accepted foundation,
not a finished collaboration product.

## Methodology provenance

The structure of this derivative follows the public EGCA example case studies:

- [Productionization-gap case study](delivery-board-productionization-gap-case-study.md)
- [Delegated-agent routing case study](payspan-delegated-agent-routing-case-study.md)
