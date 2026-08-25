# EGCA × Ponytail benchmark task candidate ledger

**Status:** living screening ledger; not a frozen confirmatory corpus  
**Canonical tracker:** issue #9  
**Ledger review:** issue #12  
**Independence review:** issue #13

## Rules

- Every materially evaluated candidate stays in this ledger even when rejected.
- `pilot-only` is permanent for tasks with high treatment exposure.
- `screening` means the task concept may be investigated; it is not admitted.
- No candidate becomes confirmatory until its baseline SHA, prompt, hidden tests, architectural envelope, exposure ratings, independent classification, and curation gates are frozen.
- The known Ponytail and EGCA examples below are useful calibration material precisely because they are **not** independent confirmatory evidence.

## Disposition vocabulary

- **pilot-only** — useful for harness/rubric calibration but barred from confirmatory analysis;
- **screening** — worth source investigation; no admission decision yet;
- **reject** — unsuitable; reason retained;
- **confirmatory-candidate** — passed initial curation but not final corpus freeze;
- **confirmatory-frozen** — final preregistered corpus member.

## Known / exposed candidates

| ID | Disposition | Stratum | Source | Candidate | Risk axes | Exposure | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | pilot-only | S1 over-build | `DietrichGebert/ponytail` agentic benchmark | Date-picker feature where native HTML can replace a custom component | accessibility | treatment: high | Used directly in Ponytail's published benchmark; excellent activation/size calibration, invalid as independent confirmation. |
| P-002 | pilot-only | S1 over-build | `DietrichGebert/ponytail` agentic benchmark | Color-picker feature with native platform capability | accessibility | treatment: high | Same treatment-specific exposure as P-001. |
| P-003 | pilot-only | S3 irreducible | `DietrichGebert/ponytail` agentic benchmark | Count/search-style backend endpoint where arms should converge | api-compatibility | treatment: high | Useful negative-control calibration; already part of Ponytail evidence. |
| P-004 | pilot-only | S3 irreducible | `DietrichGebert/ponytail` safety tier | Safe upload path / traversal guard | security | treatment: high | Useful safety-canary calibration; known benchmark task. |
| P-005 | pilot-only | S2 reuse | `sundayj/sundayj.github.io` × DevSculptor EGCA case | Metadata/SEO behavior where existing plugin capability must be inspected and selectively retained/adapted | cross-boundary | treatment: high; author: high | Direct EGCA case-study evidence. Use only to verify that the harness can recognize reuse + partial adaptation. |
| P-006 | pilot-only | S4 reject/defer | `sundayj/sundayj.github.io` × DevSculptor EGCA case | Search/indexing responsibility belongs outside the theme repository | cross-boundary | treatment: high; author: high | Direct EGCA case; good responsibility-boundary calibration, not independent evidence. |
| P-007 | pilot-only | S1/S3 calibration only | `Deepusleepy/ponytail-benchmark` | Running-balance / malformed-input harm-probe pattern | robustness, data-integrity | treatment: high | Independent of Ponytail maintainer but explicitly designed to evaluate Ponytail; reserve for no-harm instrument calibration. |
| P-008 | pilot-only | S1/S3 calibration only | `Deepusleepy/ponytail-benchmark` | Reference/anti-reference task pairs from PonyBench v3 | security, robustness | treatment: high | Valuable for validating our reference/anti-reference machinery; not a fresh treatment test. |

## Fresh screening pool

These entries deliberately begin as **concepts**, not frozen tasks. Source investigation may reject them. Exact prompts must not be written until the frozen baseline and repository evidence are understood.

### S1 — Over-build opportunity

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S1-01 | `pallets/flask` example/fixture at a frozen release | derived-real | Add a small export/serialization behavior where Python stdlib or an existing Flask/Werkzeug primitive may suffice and a new dependency would be tempting | dependency-choice | Is there a real, non-obvious native/existing solution and enough room for an agent to overbuild without making the task trivial? |
| C-S1-02 | `django/django` test fixture or narrowly extracted app | derived-real | Add a user-facing behavior already supported by a documented Django primitive but often reimplemented locally | dependency-choice, api-compatibility | Can the task be bounded enough to run repeatedly while still requiring repository/framework investigation? |
| C-S1-03 | small React/Vite brownfield fixture pinned from a public repo | synthetic-brownfield / derived-real | Add an interaction where browser/platform semantics can satisfy the requirement and custom state/component infrastructure is optional | accessibility | Does the native solution meet the full behavioral/accessibility contract rather than merely minimize LOC? |
| C-S1-04 | `encode/httpx`-style fixture | synthetic-brownfield | Add formatting/parsing behavior where a standard-library primitive is adequate and a custom helper hierarchy is tempting | robustness | Can hidden tests remain implementation-neutral? |
| C-S1-05 | public CLI project fixture | derived-real | Add configuration lookup where current config machinery already handles precedence and a new config subsystem would be excess | api-compatibility | Is the existing primitive discoverable but not obvious from the ticket? |

### S2 — Existing-capability reuse

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S2-01 | `pallets/flask` or extension fixture | derived-real | New endpoint behavior should reuse an existing authentication/authorization helper rather than duplicate checks | security | Can ownership and expected reuse be established from frozen tests/code without prescribing internal names in the prompt? |
| C-S2-02 | `django/django`-style app fixture | synthetic-brownfield | New normalization/validation path should reuse a canonical repository helper shared by another entry path | data-integrity | Does duplicate implementation create observable divergence that hidden regression tests can detect? |
| C-S2-03 | `pydantic/pydantic`-style fixture | synthetic-brownfield | Add a new input path that should flow through existing validation/serialization primitives | api-compatibility, robustness | Can a local duplicate pass happy path yet fail meaningful compatibility/regression checks? |
| C-S2-04 | TypeScript service fixture | synthetic-brownfield | New API call should reuse established request/error mapping rather than create a second client wrapper | cross-boundary, robustness | Is reuse an architectural fit rather than merely stylistic consistency? |
| C-S2-05 | public CLI/config project | derived-real | Add an option that should enter through existing option-resolution machinery | api-compatibility | Can the anti-reference plausibly implement the option independently while causing a deterministic inconsistency? |

### S3 — Irreducible implementation

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S3-01 | frozen FastAPI/Flask CRUD fixture not used by Ponytail | synthetic-brownfield | Add a narrowly specified endpoint requiring genuinely new transformation logic | api-compatibility | Do competent implementations converge enough that treatment should have little architectural leverage? |
| C-S3-02 | TypeScript utility package | derived-real | Implement a concrete parser/transform whose semantics require substantive new logic | robustness | Is there no hidden existing/native primitive that would turn it into S1/S2? |
| C-S3-03 | Django app fixture | synthetic-brownfield | Add a concrete query/report with specified filtering semantics and no new subsystem decision | performance | Can we deterministically grade correctness while allowing implementation freedom? |
| C-S3-04 | Python library fixture | synthetic-brownfield | Implement a state transition with explicit invariants where code cannot reasonably be replaced by configuration/reuse | data-integrity | Does the task provide a clean negative control for architectural-intervention claims? |
| C-S3-05 | frontend fixture | synthetic-brownfield | Add a bounded UI behavior requiring real interaction/state logic but no reusable/native shortcut | accessibility | Do accessibility requirements prevent fake savings while keeping architecture choice narrow? |

### S4 — Reject/defer architecture

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S4-01 | Python web-app fixture | synthetic-brownfield | Ticket suggests adding a generalized provider/registry, but frozen repository has one stable provider and no variation pressure; local extension is sufficient | dependency-choice | Can the prompt remain neutral rather than explicitly proposing the registry? |
| C-S4-02 | TypeScript frontend fixture | synthetic-brownfield | A new state-store/library is tempting for one isolated screen whose existing local state mechanism is adequate | dependency-choice | Can we prove that deferral is supported by current requirements rather than aesthetic preference? |
| C-S4-03 | public CLI fixture | derived-real | One new output format tempts a plugin architecture despite no extension contract or second consumer | api-compatibility | Is a plugin abstraction clearly premature from frozen evidence? |
| C-S4-04 | web-service fixture | synthetic-brownfield | New background-worker/service split is tempting, but workload and reliability constraints do not justify a service boundary | performance, cross-boundary | Can hidden tests verify required behavior without rewarding a monolith merely for being smaller? |
| C-S4-05 | persistence fixture | synthetic-brownfield | New table/model is proposed for information already derivable from canonical ledger/state | data-integrity | Can the anti-reference show duplicated state causing a deterministic reconciliation inconsistency? |

### S5 — Justified new architecture

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S5-01 | Python web-app fixture | synthetic-brownfield | Same validation/policy must apply across multiple independent entry paths; local duplication is demonstrably divergent, so a shared policy boundary is warranted | data-integrity, cross-boundary | Can underbuilding be detected through cross-path invariant tests without requiring one named abstraction? |
| C-S5-02 | authentication fixture | synthetic-brownfield | Authorization currently duplicated across endpoints and the task introduces another protected path; central enforcement is required to prevent an actual bypass | security, cross-boundary | Can a locally correct patch still fail an executed cross-endpoint security canary? |
| C-S5-03 | retry/idempotency fixture | synthetic-brownfield | Multiple callers perform externally visible operations and now require consistent idempotency semantics; shared coordination/state becomes necessary | concurrency, data-integrity | Is the new architecture genuinely required rather than merely cleaner? |
| C-S5-04 | TypeScript API client fixture | synthetic-brownfield | A public contract change affects several consumers and requires a compatibility translation boundary rather than repeated caller patches | api-compatibility, cross-boundary | Can hidden tests demonstrate why scattered minimal patches are insufficient? |
| C-S5-05 | persistence/reporting fixture | synthetic-brownfield | Required historical fact cannot be reconstructed from current state; new durable data/model is needed to satisfy the behavior | data-integrity | Can we prove derivation is impossible from baseline so adding persistence is evidence-backed? |

### S6 — Ambiguous/evolving brownfield

| ID | Repository family | Provenance | Candidate concept | Risk axes | Main admission question |
| --- | --- | --- | --- | --- | --- |
| C-S6-01 | Flask/Django fixture with layered request flow | synthetic-brownfield | Ticket names a view/controller symptom but repository inspection reveals canonical behavior belongs in service/domain layer used by multiple paths | cross-boundary | Are at least two initial interpretations plausible before inspection? |
| C-S6-02 | frontend + API fixture | synthetic-brownfield | UI request appears local but existing API contract and another consumer constrain the correct responsibility/shape | api-compatibility, cross-boundary | Can both over-local and over-general solutions be plausibly generated and graded? |
| C-S6-03 | import/reconciliation fixture | synthetic-brownfield | User asks to fix duplicated records; root cause may be ingestion identity/idempotency rather than downstream cleanup | data-integrity | Can repository evidence falsify the obvious cleanup-layer patch? |
| C-S6-04 | public package fixture | derived-real | Request appears to require a new helper but an adjacent package owns the canonical transformation | cross-boundary | Can responsibility be established from public baseline docs/tests rather than researcher preference? |
| C-S6-05 | async/background-processing fixture | synthetic-brownfield | Symptom suggests adding retries, but inspection may reveal transaction/ack ordering is the actual fault boundary | concurrency, data-integrity | Can the task be made deterministic enough for repeated agent runs? |

## Current balance

Fresh screening pool: **30 concepts**, five per preregistered primary stratum. None is admitted yet.

Known pilot-only pool: **8 candidates** with deliberate treatment exposure, suitable for validating activation, measurement, architectural-envelope review, and failure handling.

The fresh pool is intentionally overcomplete. We expect source investigation and curation to reject candidates; the target is not to force all 30 through.

## Next curation sequence

1. Select candidate repository families that are reproducible and inexpensive enough for repeated runs.
2. Resolve each screening concept to an exact public baseline SHA or construct a frozen synthetic-brownfield fixture.
3. Record license/build/runtime constraints.
4. Investigate the baseline without generating treatment outputs.
5. Write the architectural envelope.
6. Write a neutral user-visible prompt.
7. Implement deterministic hidden tests, reference, and anti-reference.
8. Have independent reviewers classify stratum and review the envelope.
9. Run only non-treatment sanity checks first.
10. Admit to pilot or confirmatory-candidate status only after the curation gate passes.

## Sources informing the curation design

- Ponytail agentic benchmark: real-agent task isolation and published contamination failure.
- Deepusleepy PonyBench v3 `TASKSPEC.md`: solution-neutral prompt contract, reference/anti-reference controls, hidden CORE vs implicit checks, and retained rejected candidates.
- Deepusleepy `DESIGN.md`: intention-to-treat treatment activation, harm-probe headroom, task-frame freezing, and independent reducibility tagging.

These sources inform the **measurement design**. Their task results do not count as independent evidence for EGCA.