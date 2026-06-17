# Issue Triage Policy

This policy describes how incoming issues are triaged across the Mininglamp-OSS
organization. The **hard 7-day SLA** below binds the two busiest repositories
(`octo-server` and `octo-web`); other repositories follow it as a best-effort target.

> **Vulnerabilities are out of scope for public triage.** Suspected or undisclosed
> security vulnerabilities follow [`SECURITY.md`](../SECURITY.md) — private report to
> **security@mininglamp.com** under coordinated disclosure — **not** the public issue
> workflow described here. See [Security-sensitive issues](#security-sensitive-issues).

## Goal

Every contributor who files an issue should get a clear, timely signal that it was
seen, understood, and routed. No issue should sit unattended.

## Scope of the SLA

| Tier | Repos | Commitment |
|------|-------|------------|
| **Hard SLA** | `octo-server`, `octo-web` | No issue stays untriaged longer than **7 days** |
| **Best-effort target** | All other public repos | Same intent, no hard guarantee |
| **Exempt** | Meta-repos with no external issue intake (e.g. this `.github` repo) | Not subject to the SLA |

## Triage SLA

On the hard-SLA repos, **no issue stays untriaged for longer than 7 days.** An issue
is considered **triaged** when all of the following are true:

1. It has a `type:*` label (`type:bug`, `type:feature`, `type:security`,
   `type:chore`, `type:docs`, or `type:refactor`).
2. It has a `priority:*` label (`priority:P0`–`priority:P3`).
3. The `needs-triage` label has been **removed**.
4. If it is security-related, it has been handled per
   [Security-sensitive issues](#security-sensitive-issues) (vulnerabilities routed to
   private disclosure; non-vulnerability security work labeled `type:security`).

Newly opened, non-bot issues are auto-labeled `needs-triage` by the
`issue-welcome.yml` reusable workflow (each repo opts in via its own caller). The
triage owner clears that label as part of triage.

**Re-entry paths.** Auto-labeling only covers *newly opened* issues. **Reopened,
transferred, or imported issues must be routed back through triage** — re-apply
`needs-triage` so they reappear in the backlog. Note the backlog query below keys on
`createdAt` (original creation), so reopened/stale items need a deliberate manual pass.

## What "triage" involves

For each `needs-triage` issue, the owner:

- **Confirms reproducibility / validity.** For bug reports, sanity-check the report
  (code analysis is enough for an initial pass; deep reproduction can be deferred
  with `needs-human-verify`). If more information is needed, apply `needs-more-info`
  and ask the reporter.
- **Classifies** with a `type:*` label.
- **Sets priority** with a `priority:*` label (see below).
- **Flags newcomer-friendly work** with `good first issue` where appropriate.
- **Handles security-related reports** per the security section below.
- **Removes** `needs-triage`.

## Priority guide

| Label | Meaning | Real precedent |
|-------|---------|----------------|
| `priority:P0` | Critical — drop everything | Active outage, data loss, or an exploited vulnerability |
| `priority:P1` | High — this sprint | `octo-server #366` — no central authz layer, so a forgotten role check on a `/v1/manager` route is a silent privilege escalation |
| `priority:P2` | Medium — next sprint | `octo-server #394` (compensating delete leaves orphan group rows); `octo-server #367` (no admin-action audit trail) |
| `priority:P3` | Low — backlog | `octo-web #397` — contact search box doesn't auto-close (minor UX) |

Borderline P1-vs-P2 calls lean on blast radius and exploitability: a latent risk that
*guards* an auth fix from regression (e.g. `octo-server #353`) is P1; a consistency or
forensics gap with no active user impact is P2.

## Security-sensitive issues

**First, the hard distinction:**

- **Suspected or undisclosed vulnerabilities do _not_ go through public triage.** They
  follow [`SECURITY.md`](../SECURITY.md): a private report to **security@mininglamp.com**
  under coordinated disclosure, or a
  [GitHub Private Vulnerability Advisory](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).
  Do **not** apply a public `type:security` label to an unresolved, undisclosed vuln —
  a public, searchable `type:security` signal on a live vuln is itself a disclosure.
- **Public `type:security` is for non-vulnerability security work**: hardening,
  authorization/architecture follow-ups, audit/forensics/process gaps, and
  already-disclosed or already-fixed items.

**Containment — if a vulnerability lands as a public issue (new _or_ pre-existing):**

1. **Minimize/redact the issue body** — remove repro steps, PoC, and weaponization
   detail. Redacting *pre-existing* public issues is **in-scope for the triage owner**,
   not just new reports. (Precedent: `octo-web #330`'s body was redacted to the
   structural finding + defensive fix; full detail moved to the internal tracker.)
2. **Redirect the reporter** to private reporting per `SECURITY.md`.
3. **Consider converting** the issue to a GitHub Private Vulnerability Advisory.
4. Only then classify any residual *structural* finding with `type:security`, or close
   it in favor of the private track.

- **Never post exploit detail in public comments.**
- **Escalation:** route security-labeled issues to the **CTO** for SecurityEngineer
  scheduling. The CTO routes; a SecurityEngineer owns implementation once staffed. In
  the interim the **CTO owns security-labeled triage directly** and delegates
  implementation slices under security review — there is no coverage gap.
- **Backstop:** if the CTO is unreachable and a P0/P1 security item is approaching the
  7-day line, escalate to the **CEO**.

## Triage ownership & rotation

Ownership maps to a queryable GitHub team handle so accountability does not diffuse:

| Repo | Triage owner | Backstop |
|------|--------------|----------|
| `octo-server` | [`@Mininglamp-OSS/server-maintainers`](https://github.com/orgs/Mininglamp-OSS/teams/server-maintainers) (Backend) | [`@Mininglamp-OSS/maintainers`](https://github.com/orgs/Mininglamp-OSS/teams/maintainers) / CTO |
| `octo-web` | [`@Mininglamp-OSS/web-maintainers`](https://github.com/orgs/Mininglamp-OSS/teams/web-maintainers) (Frontend) | [`@Mininglamp-OSS/maintainers`](https://github.com/orgs/Mininglamp-OSS/teams/maintainers) / CTO |
| Security-labeled (any repo) | CTO → SecurityEngineer (once staffed) | CEO, if CTO unreachable |

**Cadence:** each owner runs a triage sweep at least **weekly**. An issue *approaches
the 7-day line* once its open `needs-triage` age reaches **5 days** — the owner clears
or escalates it before day 7. If an owner misses the line, the backstop is woken.

For repos outside the hard-SLA set, the owning team triages on a best-effort basis;
unclear ownership routes to `@Mininglamp-OSS/maintainers`.

## Checking the backlog

List untriaged issues for a repo:

```bash
gh issue list --repo Mininglamp-OSS/<repo> --label needs-triage --state open \
  --json number,title,createdAt
```

Anything with a `createdAt` older than 7 days is an SLA breach and should be cleared
immediately. Because the query keys on `createdAt`, also scan recently **reopened**
issues — re-apply `needs-triage` to any that need a fresh pass.
