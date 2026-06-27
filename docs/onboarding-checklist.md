# Onboarding a repo to the Mininglamp-OSS CI/CD platform

> How to wire a repository into the org's reusable-workflow platform.
> Fastest path: GitHub → Actions → "New workflow" → pick an **Octo —** starter
> (these live in `.github/workflow-templates/`), or copy the snippets below.
> All callers pin the rolling `@v1` alias.

## Prerequisites (do these first)

| # | Requirement | Why |
|---|---|---|
| 1 | **Enable Dependency Graph** (Settings → Code security) | `reusable-dependency-review` hard-fails without it |
| 2 | Secrets available: `PROJECT_TOKEN` | board writes |

## Starter templates (recommended)

Pick from Actions → New workflow:
- **Octo — Security suite** — weekly CodeQL + per-PR dependency-review + secret-scan (set `language`)
- **Octo — Repo governance** — history-check, pr-title-lint, labeler, stale
- **Octo — Release drafter** — rolling draft release

## Known gotchas

1. **`pull_request_target` callers have a one-PR delay.** pr-title-lint, labeler,
   pr-welcome, check-sprint, pr-review read the workflow definition from the
   *base* branch — they do not run on the PR that first adds them. They take
   effect on the next PR after merge.
2. **CodeQL is weekly-only + high-input-surface repos only.** Don't add per-PR
   CodeQL; per-PR breadth is your own CI's `gosec`/`eslint`. Library/tool/mobile
   repos don't run CodeQL at all.

## Security tiering (which repos get what)

| Tier | Repos | CodeQL | dep-review | secret-scan |
|---|---|---|---|---|
| High input-surface | services, web, channel adapters, smart-summary, speech | ✅ weekly | ✅ | ✅ |
| Low input-surface | libraries, internal tools, mobile | ❌ | ✅ | ✅ |

## Out of scope (do NOT onboard issue automation)
Meta/infra repos (`.github`, `community`) and independent projects
(`openclaw`, `hermes-agent`) are intentionally outside issue automation — see
`workflow-architecture.md` §4a.
