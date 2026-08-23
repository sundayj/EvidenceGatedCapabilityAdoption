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

The experiment exists to reduce uncertainty, not to disguise a production rollout as research.

### 5. Evidence

Question: **What actually happened?**

Use evidence appropriate to the capability: tests, performance measurements, UX observation, operational behavior, maintenance complexity, review findings, failure modes, or other measurements.

### 6. Evidence gate

Question: **Does the observed evidence justify adoption?**

Compare actual results with the predeclared success and rejection criteria.

### 7. Decision

Choose one:

- **Adopt**
- **Adapt**
- **Reject**
- **Repeat**

### 8. Record

Preserve the rationale so future humans and agents do not need to reverse-engineer the decision from commits or chat transcripts.

## Relationship to established practices

EGCA is a synthesis, not a claim that experimental software development is new.

It borrows from:

- **Hypothesis-Driven Development** — software work framed as testable hypotheses and evidence;
- **Scientific method / empirical software engineering** — prediction, observation, revision;
- **Lean Build-Measure-Learn** — small changes designed to generate information;
- **technical and architectural spikes** — bounded implementation to reduce uncertainty;
- **evolutionary architecture** — incremental architectural change guided by feedback;
- **Architecture Decision Records** — durable rationale for important decisions.

EGCA's emphasis is specifically **capability adoption**, including source investigation, smallest useful experiments, explicit evidence gates, stable experiment identities, and durable agent-readable state.

## Durable state versus memory

EGCA state is not the same as agent memory or runtime checkpointing.

- **Repository truth** answers: what code and behavior currently exist?
- **EGCA project state** answers: what are we investigating, testing, and deciding, and why?
- **Agent memory** answers: what context should an agent retain across interactions?
- **Runtime checkpoints** answer: where did a long-running workflow stop and how can it resume?

A system may use all four.

## Storage adapters

The methodology does not require a particular backend.

### Google Sheets

Useful when humans and heterogeneous agents both need easy read/write access, flexible tabular views, sorting, filtering, and rapid schema changes.

### Git-tracked files

Markdown, YAML, JSON, or CSV provide a service-free, versioned, reviewable option that coding agents can edit easily.

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
- records negative results as useful information.

A weak experiment:

- is effectively a full feature rollout;
- has no plausible rejection condition;
- measures only whether tests are green;
- changes many architectural variables at once;
- declares success because implementation completed;
- rewrites the hypothesis after seeing the result.

## Maturity

EGCA v0.1 is intentionally experimental. The initial workflow emerged from a real capability-adoption program in a private full-stack application. The method should be tested on unrelated initiatives before being treated as stable.