# Issue Triage Policy

This policy applies to all repositories under the Mininglamp-OSS organization. It
defines how incoming issues are triaged, the service-level agreement (SLA) we hold
ourselves to, and who owns triage for the two busiest repositories
(`octo-server` and `octo-web`).

## Goal

Every contributor who files an issue should get a clear, timely signal that it was
seen, understood, and routed. No issue should sit unattended.

## Triage SLA

> **No issue stays untriaged for longer than 7 days** on the busiest repos
> (`octo-server`, `octo-web`). Other repos follow the same rule on a best-effort basis.

An issue is considered **triaged** when all of the following are true:

1. It has a `type:*` label (`type:bug`, `type:feature`, `type:security`,
   `type:chore`, `type:docs`, or `type:refactor`).
2. It has a `priority:*` label (`priority:P0`–`priority:P3`).
3. The `needs-triage` label has been **removed**.
4. If it is security-sensitive, it is labeled `type:security` and escalated to the
   CTO for SecurityEngineer scheduling (see [Security-sensitive issues](#security-sensitive-issues)).

Newly opened issues are auto-labeled `needs-triage`. The triage owner clears that
label as part of triage.

## What "triage" involves

For each `needs-triage` issue, the owner:

- **Confirms reproducibility / validity.** For bug reports, sanity-check the report
  (code analysis is enough for an initial pass; deep reproduction can be deferred
  with `needs-human-verify`). If more information is needed, apply `needs-more-info`
  and ask the reporter.
- **Classifies** with a `type:*` label.
- **Sets priority** with a `priority:*` label (see below).
- **Flags newcomer-friendly work** with `good first issue` where appropriate.
- **Routes security-sensitive issues** to the CTO (see below).
- **Removes** `needs-triage`.

## Priority guide

| Label | Meaning | Examples |
|-------|---------|----------|
| `priority:P0` | Critical — drop everything | Active outage, data loss, exploited vulnerability |
| `priority:P1` | High — this sprint | Privilege-escalation risk, regression guard for an auth fix, broken core flow |
| `priority:P2` | Medium — next sprint | Data-consistency edge cases, availability hardening, forensics/audit gaps |
| `priority:P3` | Low — backlog | Minor UX bugs, refactors, misleading docs, ergonomic wins |

## Security-sensitive issues

Issues touching authentication, authorization, secrets, audit/forensics, trust
boundaries, or supply chain are **security-sensitive**.

- Label them `type:security` and set a priority.
- **Escalate to the CTO** for SecurityEngineer scheduling. Do not assign a fix as part
  of routine triage.
- **Do not post exploit detail in public comments.** Keep the discussion at the
  classification level; detailed analysis goes through the CTO / SecurityEngineer
  channel.

## Triage ownership & rotation

| Repo | Triage owner | Backstop |
|------|--------------|----------|
| `octo-server` | **Backend** engineer | CTO |
| `octo-web` | **Frontend** engineer | CTO |
| Security-labeled issues (any repo) | **CTO** → SecurityEngineer | — |

**Cadence:** each owner runs a triage sweep of their repo at least **weekly**, and
whenever a `needs-triage` issue approaches the 7-day line. The CTO is the escalation
point and covers when an owner is unavailable.

For other repos, the owning engineer for that service triages on a best-effort basis;
unclear ownership is routed to the CTO.

## Checking the backlog

List untriaged issues for a repo:

```bash
gh issue list --repo Mininglamp-OSS/<repo> --label needs-triage --state open \
  --json number,title,createdAt
```

Anything with a `createdAt` older than 7 days is an SLA breach and should be cleared
immediately.
