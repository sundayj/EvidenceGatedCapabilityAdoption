# Your first EGCA program

Start by talking through an idea with ChatGPT or Codex. Ask whether the idea
would benefit from EGCA before starting a program. Then let Codex investigate,
keep the tracker current, and run the bounded work it has authority to do.

This practice example uses a throwaway Git repository with a local commit and
no remote. Imagine a release helper is matching whole tags by substring and
can mistake `alphabet` for `alpha`. The tiny fixture stands in for a larger
adoption question. If the real project only needs an obvious, well-tested
one-line fix, don't start an EGCA program just because this walkthrough does.

Use the [README install steps](https://github.com/sundayj/EvidenceGatedCapabilityAdoption#install-in-codex-no-python-required)
if the skill is not installed. The image below shows actual local discovery
output rendered for readability, not the composer UI. The conversations that
follow are illustrative, not a transcript of a user session.

![Codex lists evidence-gated-capability-adoption as enabled from the project skill folder.](images/codex-skill-discovery.png)

## 1. Brainstorm, then ask if it's an EGCA fit

**You:** Our release helper checks tags by substring. I think we should match
whole tags instead, but I'd like to see whether that changes behavior callers
rely on. Is this a good fit for EGCA?

**Agent:** If every caller already expects exact tags and tests prove it, just
fix the bug. If callers might deliberately rely on prefixes or substrings,
EGCA fits: investigate those callers, then use a small experiment to see
whether exact matching preserves the behavior we want. For the practice run
we can test `alpha`, `alphabet`, and `beta` without touching a real release.

You can brainstorm in ChatGPT and carry the idea to Codex. In Codex, select
`$evidence-gated-capability-adoption` in the composer before starting the program.

## 2. Ask Codex to start the program

**You:** Start an EGCA program for this in my scratch repo. Reuse the tracker
if one already exists; otherwise pick a sensible place. Keep it local.

**Codex:** No existing tracker found. I saved TAG-MATCH in
`docs/egca/tag-match/` and recorded `feature/egca-tag-match` as its integration
branch. The tracker includes the baseline, the pinned EGCA version and
source revision, and candidate C-001. E-001 is **Planned**: matching
`alpha` should return exactly `alpha`, never `alphabet`. No adoption
decision yet.

Codex should inspect the actual project before settling on the tracker or
experiment. Here, repository Markdown is a sensible default, not a required
configuration. The checkpoint should come from reading back the saved
tracker. If the exact governing revision cannot be determined, Codex should
identify what is missing rather than invent a pin.

## 3. Tell Codex to start implementation

**You:** Go ahead and start implementation. Keep it in the scratch repo
and update the tracker as you go. Don't push, merge, or deploy anything.

**Codex:** I ran E-001 on an experiment branch based on the program branch.
The substring baseline returned `alpha` and `alphabet`; the whole-line
candidate returned only `alpha`. The fixture passed. E-001 is **Validating**.
I saved the test command, outputs, and provenance in the linked fixture report
under criteria revision `tag-match-v1`. I recommend **Adopt** for exact,
case-sensitive matching within this fixture boundary. That is a recommendation, not an adoption or release decision;
no integration or deployment was performed.

The agent owns ordinary implementation, iteration, evidence capture, and
tracker updates within the permitted scope. It derives the applicable
versioned execution mandate from the governing instructions and checks the
evidence gate before an authoritative transition. A request to start is not
blanket permission to change scope, grant access, or merge. If a policy or
system reserves a permission, approval, or decision for you, the agent asks
only for that specific action. If required evidence or authority remains
unavailable, it records the blocker and continues authorized work where
possible. A passing fixture is not independent validation and doesn't
establish behavior for other callers or environments. See the
[experiment record](../templates/experiment-template.md).

## 4. Check that a fresh session can resume

Open a new Codex session in the same project without copying the old
conversation into it. Select the skill and ask:

**You:** Pick up the tag-matching program from the tracker. Before changing
anything, tell me what we've verified and what you'd do next.

**Codex:** I found C-001 and E-001 (**Validating**) under
criteria revision `tag-match-v1` and the original EGCA version and source
commit. I opened the linked fixture report. Its saved output shows that the baseline matched two lines and
the candidate one. The result supports the recorded criterion only for
this fixture. The tracker records a recommendation, not a final decision;
the applicable decision gate is next. I changed nothing.

Compare the returned IDs, status, criteria revision, governing version and
revision, and evidence link with the original tracker. If the new session
has to recreate a record or can't open the evidence, the persistence check
didn't pass. This is an independent read-back of stored state, not independent
validation of the experiment's result. Handoff to another machine needs an
authorized way to transfer both the tracker and the evidence.

## Choose a different storage backend

If you need a specific backend, name it when you ask Codex to start the
program. Otherwise, let it find and reuse the existing tracker or choose a
simple authorized location before creating any records. EGCA does not
install storage connectors or define a universal config file. A path, document URL,
workbook/tab, or approved database workspace identifies the state; the host
supplies access and any connector.

| Backend | Example instruction when starting the program | Verify before using it |
| --- | --- | --- |
| Git-tracked Markdown (default for the tutorial) | Use only `docs/egca/tag-match/` on the integration branch. Link files by record ID. | Verify the branch and relative links. To resume on another machine, the permitted commit/transfer must exist first. |
| Google Docs | Use this **existing, approved** document: <document URL>. Use an overview and sections labeled by stable ID. | Resolve the exact document; read back the added section by ID. Preserve unrelated edits and version history. |
| Google Sheets or another spreadsheet | Use this **existing, approved** workbook: <workbook URL>. Map records to tabs and join by ID, not by row number. | Verify the exact workbook/tab and one read-back by ID after sorting or filtering. Retain prior decisions and link evidence. |
| An existing database | Use the **approved sandbox only**: <connector, database/schema or API workspace>. Map program, candidate, experiment, decision, and evidence references to existing records. | Resolve the exact environment, use scoped access, confirm safe stored revisions and no duplicate IDs on retry. Use transactional writes or equivalent conflict guards where supported. |
| Other durable store (for example, an issue tracker) | Use <project and tracker location>. Map records to linked issues or supported objects with stable IDs. | Verify links, access from a fresh session, permissions, and revision/history support. |

For any alternative, use the same canonical target in the fresh-session
check. Use the [tracker schema](../templates/tracker-schema.md)
to map the overview, candidate backlog, investigations, experiments, evidence,
and decisions. Use a linked, append-only ledger when required. Keep rejected
results, the methodology pin, and evidence provenance. Prefer references over
copying private evidence into shared stores. Do not paste credentials into
prompts or trackers.

```text
Use [backend + exact location] as TAG-MATCH's only source of truth.
Resolve it read-only first and show the record mapping. If I have authorized
writes to this practice target, save the initial program records there and read them
back by their stable IDs, preserving unrelated records. If access or safe writes are
missing, name the blocker and do not create a fallback tracker.
```

Read back the records in a fresh session before relying on that target. An
accessible document, spreadsheet row, or database record stores evidence; it does not
by itself satisfy a transition mandate. Keep this exercise in a disposable
target and do not set up new infrastructure just to try the skill.
