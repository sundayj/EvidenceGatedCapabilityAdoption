# EGCA Methodology Reference

## Definition

**Evidence-Gated Capability Adoption (EGCA)** is a method for evaluating whether a capability or architectural idea belongs in a software system through explicit investigation, falsifiable hypotheses, bounded experiments, evidence gates, and durable decisions.

The central rule is simple:

> A candidate capability does not become part of the architecture until observed evidence justifies crossing an explicit adoption gate.

## Why the method exists

Software teams and coding agents are both prone to collapsing distinct states:

- interesting idea;
- researched idea;
- plausible hypothesis;
- approved experiment;
- successful experiment;
- adopted architecture;
- completed implementation.

EGCA keeps those states separate so enthusiasm, authority, or implementation momentum cannot substitute for evidence.

That separation continues after an experiment succeeds. A decision to adopt a prototype or isolated contract is not evidence that every materially different production implementation of that idea is ready.

A recurring benefit in agent-assisted development is **architecture deflation**. Generative agents can make new models, services, registries, engines, and abstractions inexpensive to produce, while the maintenance cost of those abstractions remains. EGCA therefore places a burden of proof on new complexity: inspect and test existing primitives before introducing new architecture.

This is not a bias toward minimal code at all costs. Repeated evidence may justify a small shared abstraction. The goal is for complexity to be earned by observed need rather than by speculative design.

## Evidence applicability

Evidence is scoped. An experiment validates only the artifact, environment, data shapes and scale, integration path, and operational conditions it actually exercised.

Examples:

- A static UI prototype may validate naming, information hierarchy, or task comprehension. It does not validate the production component tree, responsive defaults, accessibility semantics, authorization, failure behavior, or real data.
- A fixture-backed relationship projection may validate intended grouping rules. It does not validate unrepresented cardinality, transitive links, mutable container identifiers, or production-scale pagination.
- An isolated module may validate an algorithm. It does not validate the live API, persistence, deployment topology, observability, or recovery path.

An Adopt decision means **adopt as tested within the recorded evidence boundary**. It must not be silently generalized beyond that boundary.

## Productionization delta

The **productionization delta** is the material difference between the validated experiment artifact and the intended production implementation.

Do not repeat resolved investigation merely because implementation begins. Carry accepted evidence forward and create a linked productionization experiment or adaptation when the delta introduces material uncertainty. Give it a stable experiment identity, bounded scope, explicit success/rejection evidence, and its own gate.

Typical productionization variables include:

- real inputs, malformed inputs, and relationship cardinality;
- shared-component defaults and integration behavior;
- permissions, authorization, and tenant/user scope;
- loading, empty, partial, degraded, and failure states;
- responsive layout, accessibility semantics, and keyboard behavior;
- performance, volume, concurrency, and pagination;
- deployment topology, configuration, observability, and operational recovery.

The productionization experiment should focus on the delta rather than reopening the original architectural question. If the production implementation is substantially the same artifact running in the same relevant conditions, record that conclusion and avoid unnecessary ceremony.

## Criterion-to-evidence traceability

For a materially different production implementation, trace every accepted criterion to:

1. the production code path that owns the behavior;
2. adversarial or counterexample fixtures that exercise likely boundary failures;
3. an automated assertion appropriate to the claim;
4. branch-matched runtime, browser, benchmark, or operational evidence when the behavior is safely testable before merge.

Large test counts, a successful build, and a green generic browser run do not replace this mapping. They remain useful supporting evidence, but they cannot prove cases they did not exercise.

Post-merge and production validation are confirmatory release evidence. They should not be the first observation of behavior that could have been validated in a branch-matched environment. When a behavior genuinely cannot be tested before production, record that residual boundary and the controlled validation/rollback plan explicitly.

## Integration isolation

EGCA also separates **validated experiment work** from the repository's **production baseline**.

A single EGCA program should create one long-lived feature/integration branch from the approved baseline before experiments begin. All experiment and adaptation branches are based on that cumulative branch and, when their evidence gates justify integration, merge back into it. They do not merge directly into `main`.

```text
main
  └── feature/<egca-program>
        ├── experiment/e-001-...
        ├── adaptation/e-001-...
        ├── productionization/e-002-...
        ├── experiment/e-002-...
        └── ...
```

This matters because an experiment may prove a local hypothesis without proving that the broader capability program is ready for production. Merging every successful experiment directly into `main` turns experiment-level evidence gates into piecemeal production releases and makes later rejection, adaptation, or cross-experiment reconciliation harder.

The feature branch is therefore the cumulative **candidate architecture**. `main` remains the production baseline until the whole EGCA program passes a program-level final evidence gate. The host repository may use a different branch name or stricter release model; preserve the same logical isolation using its equivalent integration branch.

Follow-on experiments may begin before earlier work reaches production when their dependencies are understood and their evidence remains isolatable. If experiments overlap, preserve experiment-specific branches/commits and record which cumulative baseline each experiment used so later integration does not erase the evidence boundary.

## Lifecycle

### 1. Candidate

Question: **Could this capability be valuable?**

Capture the candidate without implying that the organization has committed to shipping it.

### 2. Investigate

Question: **How does the source capability actually work, and what principle is transferable?**

Study source code, documentation, comparable systems, constraints, known failures, and alternatives. Distinguish the underlying idea from implementation choices that only make sense in the source system.

### 3. Hypothesize

Question: **What observable improvement do we expect in our system?**

State a falsifiable prediction. Define what would count against it before implementation begins.

### 4. Smallest useful experiment

Question: **What is the cheapest bounded change that can answer the architectural question?**

The experiment exists to reduce uncertainty, not to disguise a production rollout as research. Create the experiment branch from the current EGCA feature branch so it tests against the cumulative candidate architecture established by prior accepted/adapted work.

Record the tested artifact/environment and the evidence applicability boundary. For a linked productionization experiment, state the delta from the prior evidence and test only the unresolved production variables.

### 5. Evidence

Question: **What actually happened?**

Use evidence appropriate to the capability: tests, performance measurements, UX observation, operational behavior, maintenance complexity, review findings, failure modes, or other measurements.

Include adversarial cases for important assumptions and production boundaries. Maintain criterion-to-evidence traceability when the intended implementation differs materially from the experiment artifact.

Keep a lightweight execution log for meaningful experiment events: commands or test suites run, observations, environment blockers, unexpected findings, and relevant commits/PRs. The log is evidence provenance, not a transcript.

Distinguish **validation blocked by environment** from **hypothesis unsupported**. A missing dependency, unavailable service, CI outage, inaccessible fixture, or other environmental constraint means the intended evidence was not collected; it does not count as negative evidence against the hypothesis.

Incidental process, tooling, test-harness, or documentation improvements discovered during an experiment may be retained when useful, but record them separately from evidence for the hypothesis. Improving the experiment apparatus does not by itself validate the capability under test.

### 6. Evidence gate

Question: **Does the observed evidence justify adoption?**

Compare actual results with the predeclared success and rejection criteria.

### 7. Decision

Choose one:

- **Adopt**
- **Adapt**
- **Reject**
- **Repeat**

The branch consequence follows the decision:

- **Adopt:** integrate the validated experiment into the EGCA feature branch within its recorded evidence boundary.
- **Adapt:** implement the evidence-supported adaptation from the EGCA feature branch, validate it, then integrate that adaptation into the feature branch.
- **Reject:** do not integrate the rejected implementation; preserve its branch/PR and evidence if useful.
- **Repeat:** keep the cumulative branch stable and create another bounded experiment from it.

### 8. Record

Preserve the rationale so future humans and agents do not need to reverse-engineer the decision from commits or chat transcripts.

### 9. Program-level final gate

When the candidate set is resolved and all required integrations are present on the EGCA feature branch, validate the branch as a whole against the current repository baseline and release criteria. Verify that every accepted criterion is traced to the cumulative production implementation and that each required productionization delta is validated or explicitly deferred as a residual boundary.

Only after this final gate passes should the feature branch be merged into `main` or the host repository's equivalent production branch. This is the point at which the cumulative candidate architecture becomes production architecture.

Keep these states distinct in durable records:

- experiment complete;
- contract/capability adopted within its evidence boundary;
- productionization validated;
- production-ready;
- merged;
- deployed;
- operationally validated.

No state implies the next one.

## Relationship to established practices

EGCA is a synthesis, not a claim that experimental software development is new.

It borrows from:

- **Hypothesis-Driven Development** — software work framed as testable hypotheses and evidence;
- **Scientific method / empirical software engineering** — prediction, observation, revision;
- **Lean Build-Measure-Learn** — small changes designed to generate information;
- **technical and architectural spikes** — bounded implementation to reduce uncertainty;
- **evolutionary architecture** — incremental architectural change guided by feedback;
- **Architecture Decision Records** — durable rationale for important decisions.

EGCA's emphasis is specifically **capability adoption**, including source investigation, smallest useful experiments, explicit evidence gates, stable experiment identities, cumulative integration isolation, and durable agent-readable state.

## Durable state versus memory

EGCA state is not the same as agent memory or runtime checkpointing.

- **Repository truth** answers: what code and behavior currently exist?
- **EGCA project state** answers: what are we investigating, testing, integrating into the candidate architecture, and deciding, and why?
- **Agent memory** answers: what context should an agent retain across interactions?
- **Runtime checkpoints** answer: where did a long-running workflow stop and how can it resume?

A system may use all four.

## Storage adapters

The methodology does not require a particular backend.

### Google Sheets

Useful when humans and heterogeneous agents both need easy read/write access, flexible tabular views, sorting, filtering, and rapid schema changes.

### Git-tracked files

Markdown, YAML, JSON, or CSV provide a service-free, versioned, reviewable option that coding agents can edit easily. Real-world EGCA use has now exercised both Google Sheets and Git-tracked Markdown, supporting the design goal that durable project state is storage-agnostic.

### Issue/project tracker

Useful where workflow transitions, ownership, team visibility, and integrations matter more than spreadsheet flexibility.

### Database + API/MCP

Useful for larger multi-agent systems that need structured queries, relational integrity, or concurrent writes.

## Stable experiment identity

An experiment ID is a historical identifier, not a priority number.

If `E-007` becomes more urgent than `E-003`, change execution priority or dependency relationships. Do not rename either experiment. Stable IDs make decision records and later references trustworthy.

## Quality criteria for an experiment

A strong experiment:

- answers one meaningful architectural question;
- has a falsifiable hypothesis;
- declares success and rejection evidence before execution;
- minimizes unrelated production change;
- is reversible or bounded where practical;
- produces evidence beyond agent self-report;
- records negative results as useful information;
- distinguishes blocked validation from contrary evidence;
- records the artifact/environment and evidence applicability boundary;
- includes adversarial evidence for consequential assumptions;
- identifies whether a productionization delta remains;
- remains isolated from `main` until the full EGCA program is ready.

A weak experiment:

- is effectively a full feature rollout;
- has no plausible rejection condition;
- measures only whether tests are green;
- changes many architectural variables at once;
- declares success because implementation completed;
- generalizes prototype or fixture evidence to a materially different production implementation;
- relies on broad green suites without criterion-to-evidence traceability;
- rewrites the hypothesis after seeing the result;
- treats environment failure as falsification;
- merges partial EGCA capability work directly to the production branch.

## Case-study feedback loop

EGCA itself should evolve empirically. Real applications of the method are expected to expose missing states, ambiguous branch rules, inadequate evidence provenance, or unnecessary ceremony. Record those findings and revise the skill/methodology when repeated or consequential evidence justifies the change.

Observed uses have already shown two complementary outcomes:

- existing system capabilities can make a proposed new subsystem unnecessary;
- repeated experiments can justify a narrow shared abstraction while a broader generalization remains deferred.

Both outcomes are healthy. Adopt, Adapt, Reject, and Repeat are genuine decisions rather than stages on an inevitable path toward the agent's initial proposal.

## Maturity

EGCA remains experimental. It originated in a private full-stack capability-adoption program and has since been exercised in public cross-repository modernization work and in a separate production-development setting using Git-tracked Markdown. Continued case studies should be used to refine the method before treating it as stable.
