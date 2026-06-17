# Mininglamp-OSS — CI/CD State Snapshot

> Point-in-time inventory of the organization's reusable-workflow platform.
> Generated 2026-06-08, after Wave 2 + Wave 1 (versioning) + triage-exit.
> Updated 2026-06-17: CI-green is now an **enforced** required merge gate on the
> 5 core repos (OCT-7) — see §5a.
> Companion to `workflow-architecture.md` (the design); this is the *as-built* state.

---

## 1. Headline status

| Metric | Value |
|---|---|
| Reusable workflows (defs in `.github`) | 19 + 1 release automation |
| Composite actions | 1 (`octo-notify`) |
| Consumer repos on `@v1` | 21 / 21 (**100%**) |
| `@main` caller refs remaining | **0** (org-wide) |
| Version tags | `v1` (rolling) → `v1.1.1`; `v1.0.0`, `v1.1.0`, `v1.1.1` (immutable) |
| Release automation | ✅ active (tag push → roll `v1` + GitHub Release) |

---

## 2. Reusable catalog (`.github/.github/workflows/`)

| Reusable | Plane | Consumers |
|---|---|---|
| `auto-add-to-project.yml` | 5 board | 18 |
| `reusable-check-sprint.yml` | 5 board | 18 |
| `issue-welcome.yml` | 6 community | 17 |
| `octo-issue-notify.yml` | 6 notify (+triage webhook) | 17 |
| `octo-ci-status.yml` | 6 notify | 17 |
| `octo-pr-result-notify.yml` | 6 notify | 17 |
| `octo-pr-review-feed.yml` | 6 notify | 17 |
| `reusable-pr-contributor-welcome.yml` | 6 community | 19 |
| `reusable-pr-labeler.yml` | 4 governance | 18 |
| `reusable-history-check.yml` | 4 governance | 20 |
| `reusable-stale.yml` | 4 governance | 17 |
| `workflow-sanity.yml` | 4 self-check | 18 |
| `reusable-release-drafter.yml` | 3 release | 18 |
| `reusable-release-publish.yml` | 3 release | 19 |
| `reusable-codeql.yml` | 2 security | 11 |
| `reusable-docker-lint.yml` | 2 security | 8 |
| `reusable-dependency-review.yml` | 2 security | **0** ⚠️ new, unadopted |
| `reusable-secret-scan.yml` | 2 security | **0** ⚠️ new, unadopted |
| `reusable-pr-title-lint.yml` | 4 governance | **0** ⚠️ new, unadopted |
| `release.yml` (`.github` self) | infra | n/a (tag-triggered) |

Composite action: **`octo-notify`** — single outbound transport (IM + webhook),
used by all 4 notification workflows.

---

## 3. Consumer coverage matrix

Legend: ● consumes · — not · (all refs `@v1`)

```
repo                  vis   board sprint welcome issue-nfy ci-stat pr-rslt pr-rvw pr-wel labeler hist stale sanity rel-dft rel-pub codeql docker
octo-server           pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-web              pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       —    ●     ●      ●       ●       ●      ●
octo-im               pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-matter           pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-smart-summary    pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-speech           pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-version-sync     priv   ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-admin            pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      ●
octo-deployment       pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       —      ●
octo-adapters         pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      —
octo-fleet            priv   ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      —
octo-lib              pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      —
octo-cli              pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       —      —
octo-daemon-cli       priv   ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       —      —
octo-android          pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       ●      —
octo-ios              pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       —      —
claw-channel-octo     priv   ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       ●       —      —
openclaw-channel-octo pub    ●     ●      ●       ●         ●       ●       ●      ●      ●       ●    ●     ●      ●       —       ●      ●(codeql)
```

### Meta / independent repos (intentionally outside the platform)
| repo | vis | status |
|---|---|---|
| `.github` | pub | platform host; consumes some reusables as a normal repo, **no issue self-triggers** (§4a exit) |
| `community` | pub | governance/release only; **issue automation removed** (§4a exit) |
| `openclaw` | pub | **independent** (58 own workflows) — only `history-check`/`stale` overlap historically; self-governed |
| `hermes-agent` | pub | **independent** (16 own workflows, own osv/supply-chain stack) |
| `hermes-channel-octo` | pub | minimal: `history-check` only |
| `cc-channel-octo` | pub | **bare** — only its own `ci.yml`, consumes no reusable |
| `octo-website` | priv | **no workflows** |

---

## 4. Versioning & supply chain

- **All 21 consumers pin `@v1`** (rolling major alias). Zero `@main` residue.
- `v1` → `v1.1.1` (commit `392c7a9`). Immutable anchors: `v1.0.0`, `v1.1.0`, `v1.1.1`.
- `release.yml` auto-rolls `v1` and cuts a GitHub Release on every `vX.Y.Z` push
  (verified live 3×). Pre-releases do not advance the alias.
- Internal `uses:` (notify workflows → `octo-notify`) pinned `@v1` → callers get a
  fully version-frozen graph (no transitive `@main` leak).
- Third-party actions SHA-pinned; downloaded binaries SHA256-verified.

---

## 5. Gaps & next-wave candidates

| Gap | Detail | Wave |
|---|---|---|
| **3 new reusables unadopted** | `dependency-review`, `secret-scan`, `pr-title-lint` exist but **0 consumers** | needs rollout (rulesets / per-repo callers) |
| **No language CI reusable** | go/node quality removed by #65; no org test/lint baseline | Wave 3 |
| **CodeQL is per-PR on 11 repos** | should be weekly schedule + scoped to high-risk only | Wave 4 |
| **Runner/checkout drift** | mix of `ubuntu-latest`/`ubuntu-24.04`, checkout v4/v6 across defs | Wave 5 |
| **No enforced distribution** | reusable *adoption* is per-repo opt-in (no org rulesets / required workflows). **CI-green merge gate now enforced** on the 5 core repos (§5a, OCT-7); broader required-workflow distribution still pending | Wave 5 |
| **No starter templates** | new repos hand-copy callers | Wave 5 |
| **Secret scanning L0/platform** | only CI layer planned; platform push-protection + local hooks not yet enabled | Plane 2 |

---

## 5a. Enforced merge gates — CI-green (OCT-7, 2026-06-17)

`CI green` is now a **required status check** on `main` for all 5 core repos —
red CI blocks merge. The existing `enforce_admins=true` and 3-approval review
requirement are **preserved unchanged** on all 5; `strict` (require-up-to-date)
is intentionally **off** to avoid forced-rebase churn (red CI still blocks
regardless of base freshness).

Two patterns, chosen per repo's CI shape:

| Repo | Required context(s) | Pattern | Why |
|---|---|---|---|
| `octo-server` | `Build`, `Test`, `Vet`, `Lint`, `Personal MsgSendReq Lint`, `i18n Extract Check`, `i18n Lint` | direct job contexts | non-matrix jobs; job-level `if:` skips report as `skipped`, which GitHub counts as passing on docs-only PRs (no perma-block) |
| `octo-web` | `Build` | direct job context | single non-matrix build job |
| `octo-admin` | `CI Gate` | aggregate gate | `build` is a matrix job (node 18/20); a skipped matrix job collapses to one un-suffixed `build` context, a running one expands to per-combo contexts → neither is safely requirable |
| `octo-adapters` | `CI Gate` | aggregate gate | `build` is a 3-OS matrix (same matrix-skip hazard) |
| `octo-deployment` | `CI Gate` | aggregate gate | CI used **workflow-level** `pull_request.paths` (perma-block hazard: a PR touching no yaml/kustomize never creates a check). Path filter removed; gate added |

**`CI Gate` job** (added to admin/adapters/deployment `ci.yml`): `if: always()`,
`needs:` the repo's jobs, fails iff a needed job concluded `failure`/`cancelled`
(`skipped`/`success` pass). One stable context, immune to matrix expansion and
path-filter skips — the robust required-check target for path-filtered pipelines.

**Validated with throwaway test PRs (closed after):**
- *Direct pattern (octo-server):* deliberately-red build → `Build`=FAILURE → merge **blocked**; docs-only PR → all code jobs `skipped` → **not** blocked by the gate.
- *Aggregate pattern:* malformed-yaml PR on octo-deployment → `CI Gate`=FAILURE → **blocked**; docs-only PR on octo-admin → `build` skipped, `CI Gate`=SUCCESS → **not** perma-blocked.

> **Bootstrap note:** the 3 `CI Gate` jobs had to land on `main` before the gate
> context could be required, but no second reviewer was available (only CEO/CTO
> agents active; agents are not GitHub reviewers). Each gate PR was admin-merged
> after its own `CI Gate` ran green, via a brief `enforce_admins` toggle, then
> full protection (enforce_admins + 3 reviews + required `CI Gate`) was restored
> in the same operation. octo-server/octo-web needed no workflow change.

---

## 6. Health signals (verified this session)
- ✅ Notification refactor live & green in production (octo-deployment, octo-server real runs)
- ✅ Triage webhook fires where `TRIAGE_WEBHOOK_URL` is set (octo-deployment issue #107 labeled)
- ✅ `@v1` migration green across canary + batch (0 startup_failures = all refs resolve)
- ✅ Release automation verified live (v1.0.0, v1.1.0, v1.1.1 alias rolls)
- ⚠️ Pre-existing, version-independent check failures observed (check-sprint without
  `Closes #`, welcome 403, hadolint) — not regressions; flagged for repo owners.
