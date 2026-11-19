---
name: release-verification
description: "Use after a release, publication, or deployment to verify the delivered artefact and observe the affected surfaces until the observation window is clean. Covers release identity, surface evidence, finding classification, observation cadence, and partial-verification reporting."
---

Regard a successful merge, publish, or deploy command as the commencement of verification, not its conclusion.
- Establish the release identity first: repository, version, immutable tag commit, merge commit, deployment target, and every affected delivery surface; derive each from registry, provider, or deployment metadata rather than the current branch or the latest build.
- Verify what users receive, per surface:
  - Source and CI: the tag resolves to the shipped commit, and that commit's checks have concluded, including late failures.
  - Published package: the exact registry version, the intended distribution tag, the artefact contents, and a smoke execution from an isolated directory.
  - Hosted service: the live alias serves the intended deployment, health signals are sound, and the changed path works via the real authenticated interface.
  - Installed client: the registration or cache in effect rather than the marketplace copy, plus a fresh connection to the running process.
- Classify every finding as a release regression, a pre-existing defect, an operational failure, or a transient signal; support each classification with its own evidence.
- Observe the requested window; absent a request, observe until 30 minutes after the first public availability. Poll changing checks every 30-60 seconds and steady signals every 2-5 minutes, and limit each individual wait so the session remains responsive.
- Treat publication lag, an unavailable interface, and a warning as distinct states: a pending exact-version lookup is not a failure, and an unreachable interface is a coverage gap rather than evidence of health.
- Monitoring confers no additional authority; prepare and validate a concrete correction prior to requesting any authorisation for another release, rollback, migration, or external announcement.
- Complete only when the relevant checks have concluded, the delivered artefacts and affected paths pass, no actionable regression remains, and the window is satisfied.
- Report as partially verified, naming the coverage gap and its next action, when a required check remains incomplete; distinguish an externally blocked operational follow-up from verified product health.