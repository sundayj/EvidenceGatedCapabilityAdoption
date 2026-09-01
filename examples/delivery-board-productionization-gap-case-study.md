# Case Study: Prototype Evidence and the Productionization Gap

## Summary

This case study records a production user-interface capability whose underlying
semantics were evaluated through bounded EGCA experiments before implementation.
The experiments supported adoption, but the live implementation introduced
material variables that the experimental artifacts had not exercised.

After release, real relationship cardinality exposed an over-grouping defect.
Later browser review found two presentation defects caused by shared-component
defaults: compact titles could emit block-heading semantics, and the responsive
list could select the wrong identity column on small screens.

The lesson is not that the experiments were invalid. Their evidence remained
valid for the prototypes, fixtures, and isolated contracts actually tested. The
methodology failure was allowing that evidence to authorize a materially
different production implementation without a linked productionization gate.

This is a sanitized derivative. Private project names, repository paths,
identifiers, records, and exact operational counts have been removed or
generalized. The original project records remain the authoritative evidence.

## Context

An internal engineering system had several overlapping work surfaces. A new
team delivery-risk board was proposed to group related support tickets,
engineering work, and delivery artifacts into cases, rank those cases, and
provide responsive drill-in behavior.

The EGCA program investigated several distinct questions before implementation:

- which records were eligible to appear as development work;
- which lifecycle statements were justified by available evidence;
- which relationships could combine artifacts into one delivery case;
- how cases should be ranked and explained;
- how the personal and team scopes should be named;
- whether the resulting board concept was useful enough to adopt.

Static semantic prototypes, fixture-driven projection modules, deterministic
tests, and documentation-only interface artifacts answered those questions at
their intended scope. The program adopted or adapted the supported contracts
and rejected broader claims that lacked evidence.

## Evidence boundary of the original experiments

The accepted evidence covered:

- de-identified, bounded fixtures;
- explicit relationship examples chosen for the projection experiment;
- isolated eligibility, lifecycle, grouping, and ranking modules;
- static or documentation-only interface prototypes;
- repository tests for those artifacts;
- stated exclusions, including broad inferred relationships and unsupported
  claims of active implementation.

It did not cover:

- the full relationship-cardinality distribution in live source data;
- the exact production query and pagination path;
- the shared list component's responsive identity-column behavior;
- block-level Markdown semantics inside compact titles;
- branch-rendered browser behavior using adversarial source strings;
- post-deployment behavior against current operational data.

The adoption decisions therefore supported the tested concepts and contracts.
They did not, by themselves, establish that every production realization of
those contracts was ready to merge or deploy.

## The productionization delta

The live implementation added several material variables:

1. Multiple source types were queried and projected through production data
   access paths with real limits, permissions, freshness states, and warnings.
2. Relationship grouping ran against naturally occurring high-fanout
   identifiers rather than only bounded fixture graphs.
3. The board used a shared production list component whose defaults controlled
   responsive row identity.
4. Source-provided titles were rendered through the application's Markdown
   component rather than the static prototype's constrained text treatment.
5. The result was exercised in a real browser and later in production, not only
   as an isolated projection or documentation artifact.

Those differences constituted a productionization delta. Under the clarified
method, they require a linked experiment or adaptation carrying forward the
accepted criteria while testing only the new uncertainty.

## Finding 1: a provenance identifier became a union edge

One source exposed a planning-container identifier shared by many otherwise
independent work items. The production grouping algorithm treated that
identifier as a transitive identity edge.

With friendly fixtures, the edge appeared useful: related artifacts sharing a
container could be displayed together. With real data, a high-fanout container
collapsed many distinct tickets and engineering jobs into one oversized case.

The correction preserved the planning identifier as provenance but removed it
from case identity. Cases were defined only by independently trusted direct
relationships. A corrected replay retained all artifacts while distributing
them across appropriately bounded cases.

The missing pre-merge evidence was not another general architecture review. It
was a small adversarial graph containing:

- two unrelated ticket origins;
- one shared planning container;
- multiple independent engineering jobs;
- assertions for artifact conservation, deterministic grouping, provenance,
  and maximum-case behavior.

## Finding 2: compact titles inherited block semantics

The production row used a general Markdown renderer for a compact case title.
When source text began with Markdown heading syntax, the renderer emitted a
heading element inside the row. That introduced a heading-order accessibility
violation and changed the visual hierarchy of data that should have remained
inline.

Existing component coverage used emphasis syntax only. It proved that ordinary
formatting rendered, but it did not test the boundary between safe inline
formatting and block document structure.

The appropriate production contract is an explicit inline-safe rendering mode:
preserve supported emphasis and safe links while preventing block headings and
other document-level structure in compact labels. Direct tests should assert
the rendered semantics, not merely the presence of formatted text.

## Finding 3: an implicit responsive default chose the wrong identity

The shared list component required an explicit primary-column identifier to
preserve row identity on narrow viewports. The production board omitted it, so
the component defaulted to another visible column. The true case title was
relegated to truncating metadata on mobile.

Desktop rendering did not make the defect obvious because all columns remained
visible. The missing evidence was a narrow-viewport assertion that the intended
title column remains the primary identity and continues to open the correct
drawer.

This was not evidence against the adopted board concept. It was evidence that
shared-component defaults are part of the productionization delta and must be
made explicit when they affect accepted UX criteria.

## Why the original EGCA work missed these defects

Four conditions combined:

1. **Evidence scope was implicit.** The experiments named their artifacts and
   criteria, but the final handoff did not force a statement of what remained
   untested in production.
2. **Adopt was interpreted too broadly.** Conceptual adoption was allowed to
   read as implementation readiness even though the implementation differed
   materially from the validated artifacts.
3. **Fixtures were representative of intended relationships, not adversarial
   production shapes.** They did not contain a high-fanout provenance-only key.
4. **Browser validation was not traced criterion by criterion.** General
   rendering and accessibility checks did not replace direct assertions for
   title semantics and responsive row identity.

The process had strong investigation, explicit decisions, and substantial test
coverage. The gap was narrower: it lacked an enforceable bridge from accepted
experimental evidence to the exact production artifact.

## Methodology correction

The case supports four additions to EGCA:

### 1. Evidence applicability boundary

Every experiment records the artifact, environment, data shapes and scale,
integration path, and operational conditions actually tested. Adopt means
"adopt as tested," not unrestricted approval of future implementations.

### 2. Productionization delta

Before production readiness, compare the intended implementation with the
accepted experimental artifact. If the delta introduces material uncertainty,
create a linked productionization experiment or adaptation. Do not repeat
resolved discovery; test the delta.

### 3. Criterion-to-production traceability

For each accepted criterion, identify:

- the production code path implementing it;
- representative and adversarial fixtures;
- direct automated assertions;
- branch-matched runtime or browser evidence when behavior depends on
  integration, rendering, or environment.

Passing broad suites is supporting evidence, not a substitute for this trace.

### 4. Distinct release states

Track these separately:

- production readiness;
- merge;
- deployment;
- operational validation.

A green pre-merge gate does not prove deployment. A successful deployment does
not prove behavior against live data. Post-release findings do not retroactively
invalidate correctly bounded experiment evidence.

## Alternatives rejected

### Repeat the full EGCA program for every production implementation

Rejected as disproportionate. The earlier investigation and accepted criteria
remain useful. Only material untested deltas need new evidence.

### Treat post-deployment validation as the productionization experiment

Rejected when the relevant behavior can be tested safely before merge. Live
validation remains necessary for operational claims, but it should not be the
first opportunity to discover deterministic relationship, accessibility, or
responsive-layout defects.

### Add every observed defect as a universal checklist item

Rejected as brittle. The reusable rule is to identify material deltas and trace
accepted criteria through them. High-fanout relationships, inline semantics,
and responsive defaults are examples of adversarial evidence, not a permanent
list that can anticipate every future implementation.

## Outcome and remaining uncertainty

The relationship correction demonstrated that a bounded productionization
experiment could preserve the adopted capability while repairing a production
assumption. The presentation findings demonstrated why production readiness,
merge, deployment, and operational validation must remain distinct and why a
methodology change must not be confused with authorization for a separate
product fix.

The resulting EGCA clarification is backward-compatible. Historical decisions
remain valid inside the evidence boundaries they actually established. Active
programs add applicability, productionization-delta, traceability, and release
state records prospectively rather than rewriting their history.

One case cannot establish that the new invariant is optimally calibrated. It
should be evaluated on future backend, integration, data-migration, and UI
programs to determine whether it catches material evidence-transfer gaps
without turning ordinary implementation into unnecessary ceremony.
