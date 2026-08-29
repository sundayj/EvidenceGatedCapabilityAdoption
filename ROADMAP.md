# EGCA Roadmap

This roadmap tracks methodology, packaging, distribution, and validation work that is useful but not yet part of EGCA's stable core contract.

## Distribution and lifecycle

### Versioned skill releases

- [x] Add explicit skill version metadata.
- [x] Add a changelog and migration notes.
- [x] Allow an installed EGCA skill to check the canonical repository for a newer version.
- [x] Allow an agent to apply an update only after presenting the proposed version/commit and obtaining explicit user approval.
- [x] Refuse silent, background, or self-triggered mutation of the installed skill.
- [ ] Publish immutable tagged releases and signed/checksummed release artifacts; move the updater from the experimental `main` channel to release artifacts once that release process exists.
- [ ] Add CI that verifies the root compatibility copy and installable skill package stay synchronized where their contracts overlap.

### Plugin distribution

Preferred long-term distribution is a versioned EGCA plugin containing the EGCA skill. The standalone skill remains useful for development, repository-local use, and environments that support Agent Skills but not OpenAI plugins.

- [ ] Package EGCA as a skill-only plugin.
- [ ] Validate installation and invocation in both ChatGPT and Codex surfaces that support plugins.
- [ ] Submit/publish through the supported Plugin Directory path when public developer distribution is available to this project.
- [ ] Document workspace/admin installation policies and permission boundaries.
- [ ] Keep plugin packaging thin: the canonical methodology and skill source remain in this repository.

Target distribution model:

```text
GitHub repository (canonical source)
        |
        +--> repository-scoped skill copy (project-pinned)
        |
        +--> standalone Agent Skill installation
        |
        +--> versioned EGCA plugin (preferred user distribution)
```

### Reproducible active programs

- [ ] Add an `egca_methodology_version` field to the canonical durable-state schema/templates.
- [ ] Define upgrade semantics for an active EGCA program: a global skill update must not silently rewrite the methodology version governing an existing program.
- [ ] Record methodology migrations as explicit program decisions when a material EGCA upgrade is adopted mid-program.

## EGCA governing EGCA

Significant methodology changes should themselves follow an evidence-gated change record:

1. identify the weakness or new requirement;
2. state the proposed methodology change;
3. define the expected improvement and compatibility impact;
4. cite evidence or validation supporting the change;
5. record rejected alternatives and unresolved risk;
6. classify the release impact (patch/minor/major);
7. provide migration instructions when needed.

The repository should therefore become a longitudinal case study of EGCA's own evolution rather than merely a static specification.

## Validation

- [ ] Expand independent, repeatable benchmark coverage beyond longitudinal case studies.
- [ ] Test multi-agent and team-scale workflows.
- [ ] Test update behavior across Linux, macOS, Windows, and managed Codex environments.
- [ ] Add adversarial update tests: moved branch head, malformed manifest, network failure, partial copy, unexpected local modifications, and rollback.
