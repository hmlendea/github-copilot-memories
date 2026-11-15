---
name: agent-instruction-coaching
description: Use when proposing evidence-backed improvements to another agent's instructions, skills, or tool descriptions. Covers trajectory-based evidence, mandatory review gating, dimension limits, and single-run separation of analysis from application.
---

Coach a distinct agent by examining its recent execution record, identifying recurring behavioural patterns, and proposing the most compact durable modification to its instruction file, an existing skill, or a tool description. Never coach the active agent; self-examination is excluded.

## Load-Bearing Principles

- **Trajectories, not aggregate scores, constitute the load-bearing evidence.** A summary metric conceals the sequence of decisions that produced an outcome.
- **Modifications apply only from a reviewed diff after an accepted interaction.** Never substitute an immediate in-session modification for the review gate.

## Applicability

- **Use when:** an assignment requests analysis, coaching, or evaluation of a specific agent, a routine supplies a bounded collection of agents for examination, or a maintainer requests an evidence-backed proposal to refine an agent's instructions or skills.
- **Do not use when:** the designated agent is the executing agent, the request concerns product source code or shared infrastructure rather than agent configuration, or the request demands immediate unrereviewed modification.

## Required Inputs

- **targetAgentId:** the agent under examination; must not equal the executing agent's identifier.
- **windowHours or issueCount:** the examination window, defaulting to the most recent ten completed assignments or the preceding seventy-two hours, whichever is broader. Cap the examination at twenty-five assignments to preserve a bounded context.

Optional inputs:

- **focus:** a free-text indication of the dimension to emphasise (for example, insufficient verification or delayed escalation), biasing pattern identification toward that dimension.
- **replayIssueIds:** an explicitly designated collection of historical assignments serving as the evaluation benchmark. In its absence, select three to five representative recent assignments.

## Mandatory Constraints

Every proposal must satisfy all of the following conditions:

- **Separate application:** analysis and application execute in distinct runs. Deliver a diff together with an application plan; a human or the overseeing authority accepts it through an explicit interaction before any modification occurs.
- **Dimension limits:** a skill file must not exceed 15 KB; a tool description must not exceed 500 characters; the agent instruction file may expand by at most twenty per cent per proposal. Requirements beyond these limits demand separate proposals.
- **Evidence or omission:** every proposed rule cites at least one concrete quotation or assignment identifier from the examined agent's recent record. Absent evidence, omit the rule.
- **Bounded scope:** propose modifications only to the target agent's instructions, its skills, or its tool descriptions. Never propose modifications to source code the agent does not own or to shared infrastructure.

## Reporting

Deliver the identified patterns, the evidence supporting each observation, the proposed compact diff, the affected files, and the required acceptance interaction. State explicitly that no modification has yet been applied.
