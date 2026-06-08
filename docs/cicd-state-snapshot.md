# Mininglamp-OSS — CI/CD State Snapshot

> Point-in-time inventory of the organization's reusable-workflow platform.
> Generated 2026-06-08, after Wave 2 + Wave 1 (versioning) + triage-exit.
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
| **No enforced distribution** | adoption is per-repo opt-in; no org rulesets / required workflows | Wave 5 |
| **No starter templates** | new repos hand-copy callers | Wave 5 |
| **Secret scanning L0/platform** | only CI layer planned; platform push-protection + local hooks not yet enabled | Plane 2 |

---

## 6. Health signals (verified this session)
- ✅ Notification refactor live & green in production (octo-deployment, octo-server real runs)
- ✅ Triage webhook fires where `TRIAGE_WEBHOOK_URL` is set (octo-deployment issue #107 labeled)
- ✅ `@v1` migration green across canary + batch (0 startup_failures = all refs resolve)
- ✅ Release automation verified live (v1.0.0, v1.1.0, v1.1.1 alias rolls)
- ⚠️ Pre-existing, version-independent check failures observed (check-sprint without
  `Closes #`, welcome 403, hadolint) — not regressions; flagged for repo owners.
