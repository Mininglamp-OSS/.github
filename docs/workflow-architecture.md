# Mininglamp-OSS — CI/CD & Automation Architecture

> **2026-06-27 update — Plane 6 notification chain removed.** The IM
> notification chain (`octo-ci-status`, `octo-issue-notify`, `octo-pr-result-notify`,
> `octo-pr-review-feed`, `octo-pr-review-feed-comment`, and the shared
> `actions/octo-notify` composite action) was decommissioned org-wide. Issue/PR
> automation now runs through cron-driven multica autopilots; CI state changes
> no longer push to IM. Sections below referring to those workflows are
> historical context only — do not use them as a target for new work.
>
> The blueprint for every automation under the organization: reusable
> workflows, their triggers, how they are versioned and distributed, and how
> local git hooks relate to (but are **not** part of) the central system.
>
> This document is the **acceptance baseline**: every new workflow PR must be
> justifiable against the invariants and planes below. If a change cannot be
> placed cleanly into one plane with a single responsibility, it is not ready.

---

## 0. Status

| | |
|---|---|
| Scope | All repositories under `Mininglamp-OSS` (currently 19) |
| Central repo | `Mininglamp-OSS/.github` (org trust root — holds all shared logic) |
| Visibility | **All repositories are public** (CodeQL/Scorecard free; fork PRs are the norm) |
| Merge strategy | **Squash and merge** (org-wide default) |
| This document | Design baseline. Implementation is staged in waves (§7); nothing here is built until its wave is approved. |

---

## 1. Invariants (the rules that keep the system orthogonal)

These are **preconditions for merging any automation change**. They are what
prevent a reusable library from rotting into overlap and waste.

1. **One workflow = one concern = one trigger semantic.** No workflow does two
   unrelated things.
2. **Reusable holds logic; caller holds trigger + secrets.** Shared logic is
   written once in `.github`. Each consumer repo carries only a thin,
   near-template caller.
3. **One source of truth per fact.** Any given quantity (PR size, coverage,
   sprint, a label namespace) is computed/written by exactly one workflow.
4. **Cost class is declared, not incidental.** Every reusable declares whether
   it runs on PR / push / schedule, its recommended `paths` filter, and whether
   it uses `concurrency: cancel-in-progress`.
5. **Fast & shallow runs per-PR; slow & deep runs on schedule.** Heavy scans
   are never attached to every PR.
6. **Parameterize across languages; never copy N files.** "lint" is one concern
   configured per language, not a pile of bespoke files.
7. **Pin everything.** Third-party actions pinned to a commit SHA with a version
   comment. Downloaded binaries verified by SHA256.
8. **A gate that must be enforced lives in CI, never only in a git hook.**
   Hooks are bypassable (`--no-verify`) and absent for external contributors.

---

## 2. Three-layer depth model

Checks are placed at the **earliest layer that adds value** and enforced at the
**most authoritative layer**. The same cheap check may run at L0 (advisory) and
L1 (gate) — that is not waste; it saves the push→wait→fail→repush round-trip.
Only duplicating *expensive* work across layers is waste.

| Layer | Where | Properties | Belongs to central system? |
|---|---|---|---|
| **L0 — local git hooks** | Developer machine, pre-commit / pre-push | Instant feedback, **bypassable**, **absent for fork contributors** | **No** — see §6 |
| **L1 — PR CI** | Remote, enforced by org rulesets | Authoritative, clean env | **Yes** |
| **L2 — scheduled CI** | Remote, time-driven | Heavy, decoupled from PR latency | **Yes** |

**Consequence of all-public + fork-normal:** for external contributions L0 does
not exist, so **L1 is the only real defense**. No required check may depend on a
hook being installed.

---

## 3. The six orthogonal planes

Each plane owns one question. A new workflow must declare its plane and must not
contend for another workflow's source of truth.

| Plane | Question it answers | Workflows |
|---|---|---|
| **1 — Language CI / correctness** | "Is the code correct?" | `reusable-go-quality`, `reusable-node-quality` |
| **2 — Security** | "Is it safe?" | `reusable-codeql`, `reusable-docker-lint`, `reusable-dependency-review`, `reusable-secret-scan` |
| **3 — Supply chain / release** | "How is it shipped?" | `reusable-release-drafter`, `reusable-release-publish` |
| **4 — Repository governance** | "Is the repo tidy & well-formed?" | `reusable-history-check`, `reusable-pr-labeler`, `reusable-stale`, `reusable-pr-title-lint`, `workflow-sanity` |
| **5 — Project board** | "Project management" | `auto-add-to-project`, `reusable-check-sprint` |
| **6 — Community & notification** | "How do we talk to humans?" | `issue-welcome` (the rest of Plane 6 — `octo-ci-status` / `octo-issue-notify` / `octo-pr-result-notify` / `octo-pr-review-feed` / `octo-notify` — was removed 2026-06-27) |

### Legend for state below
- ✅ exists today, keep as-is
- 🔧 exists, needs change (see notes)
- ➕ new
- 🔁 rebuild (was removed by #65)

---

## 4. Per-plane design

### Plane 1 — Language CI / correctness

State: 🔁 **rebuild** (`reusable-go-quality` + `reusable-node-quality` were
removed by #65 on 2026-06-06 because the T15 consumer opt-in PRs were all
closed — nobody adopted them). Rebuild is approved **on the condition that they
are distributed by org rulesets (§5), not consumer opt-in**, which is what
caused the original wind-down.

- `reusable-go-quality`: `golangci-lint` (+`gosec`) → test (`-race -shuffle`) →
  coverage → diff-coverage (octocov). Optional MySQL/Redis services.
  **Simpler than T15: a single quality entry point, not a sprawl of jobs.**
- `reusable-node-quality`: typecheck → lint → test → build → coverage.
- Trigger: PR + push, **filtered by language `paths`**, with
  `concurrency: cancel-in-progress`.
- **Every job carries `timeout-minutes`** (the gap that the removed versions
  had — must not recur on rebuild).

### Plane 2 — Security

The deliberate split that avoids overlap and per-PR waste:

| Tool | Layer / cadence | Role |
|---|---|---|
| `golangci-lint` + **`gosec`** | L0 + **per-PR** (in Plane 1) | Breadth fast-screen; covers ~90% of Go security (injection, weak crypto, hardcoded creds) in seconds |
| `reusable-codeql` 🔧 | **weekly `schedule`**, **only server/im/web high-risk repos** | Depth: cross-function taint tracking (injection/SSRF chains) gosec cannot see. **Re-positioned off per-PR / off all-repos.** |
| `reusable-docker-lint` ✅ | per-PR, `paths`-filtered | hadolint + shellcheck |
| `reusable-dependency-review` ➕ | per-PR, all repos | License + known-vuln gate on dependency changes (free on public repos) |
| `reusable-secret-scan` ➕ | per-PR (L1), all repos | gitleaks **binary, downloaded + SHA256-verified** (reuse the hadolint/actionlint pattern). **Not** `gitleaks-action` (org license). |

**Secret scanning is three layers, each covering the others' blind spots:**

| Layer | Mechanism | Covers |
|---|---|---|
| Platform | GitHub native **push protection** (free, public) | Known vendor secret patterns; works for everyone incl. external contributors; zero maintenance |
| L0 | gitleaks in local hook (per-repo, §6) | Custom rules (e.g. `OCTO_BOT_TOKEN`, `PROJECT_TOKEN` formats) + pre-push instant feedback (a secret is leaked the moment it is pushed → L0 is strictly better than CI here) |
| L1 | `reusable-secret-scan` | Authoritative gate; the **only** secret defense for fork contributors who have no L0 |

### Plane 3 — Supply chain / release

State: ✅ keep `reusable-release-drafter`, `reusable-release-publish`.

- Squash + PR-title means **release notes are generated from PR titles** — this
  ties Plane 3 to `reusable-pr-title-lint` (Plane 4): title quality is doubly
  load-bearing.
- Future, only for repos that ship binaries/images: SBOM (syft) + signing
  (cosign). Not in scope until such a repo needs it ("pragmatic increment").

### Plane 4 — Repository governance

- ✅ `reusable-history-check` (orphan-branch / no-common-ancestor rejection)
- ✅ `reusable-pr-labeler` (**sole owner** of `size/*` and
  `dependencies-changed` labels)
- ✅ `reusable-stale` (**sole owner** of the `stale` label)
- ✅ `workflow-sanity` (actionlint + no-tabs; already scans `.github/actions/**`,
  anticipating the composite in Plane 6)
- ➕ `reusable-pr-title-lint`: enforces Conventional Commits **on the PR title**.
  CONTRIBUTING already requires Conventional Commits but nothing enforces it.

**Why pr-title-lint cannot be replaced by a commit-msg hook (squash analysis):**

| Object | Checked by | Under squash merge |
|---|---|---|
| Commit message | commit-msg hook | **Squashed away** → checking it is pure friction; **commit-msg hook is NOT adopted** |
| PR title | `reusable-pr-title-lint` | **Becomes the squash commit subject = the main-branch history** → the sole authoritative guard, **required** |

→ Squash lets us **delete the entire commitlint line of work**; pr-title-lint
stays as the single guard. (Under merge/rebase the conclusion would flip — a
"lint PR commits" CI check would be needed instead. We are squash, so it is not.)

### Plane 5 — Project board

State: ✅ keep `auto-add-to-project`, `reusable-check-sprint` unchanged.

- The **one** intentional shared-state coupling in the whole system:
  `auto-add-to-project` **writes** Sprint (inherits from a linked issue onto the
  PR board item, only when absent); `reusable-check-sprint` **reads & validates**
  it. Write-once / read-validate, idempotent — documented, not a conflict.

### Plane 6 — Community & notification

State: 🔧 **collapse all outbound notification into one action.**

- ✅ keep `issue-welcome`. (`reusable-pr-contributor-welcome` was **removed**
  org-wide — first-time PR welcome retired; greeting/onboarding is handled
  elsewhere.)
- ➕ `.github/actions/octo-notify` (**single composite action — the org's only
  outbound transport**): shared core is "HTTP POST with retry/backoff
  (429/5xx + Retry-After) + sanitize". Two modes, enabled independently by which
  inputs are supplied:
  - **IM mode** (`im-message` + `im-group-id` + token): send to Octo IM
    (allowlisted base URL).
  - **Webhook mode** (`webhook-url` (secret) + payload): POST to an external
    endpoint (e.g. the triage agent).
  Replaces the ~50-line Python block copy-pasted across all four IM workflows
  (`ALLOWED_API_BASES` appeared 4×, already drifting).
- 🔧 consumers of `octo-notify`:

  | Workflow | IM mode | Webhook mode |
  |---|:--:|:--:|
  | `octo-issue-notify` (was `octo-issue-feed`, **renamed**) | ✅ | ✅ triage webhook |
  | `octo-pr-result-notify` | ✅ | — |
  | `octo-pr-review-feed` | ✅ | — |
  | `octo-ci-status` | ✅ | — |

- **Invariants preserved on merge:**
  1. **event→message mapping stays in each workflow**, never in the action —
     the action does transport only, knows nothing of issue-vs-PR. This is what
     keeps a single action from becoming a junk-drawer (invariant #1).
  2. **IM and webhook share one unified event set** (`[opened]`, see §4a) — both
     fire on the same trigger inside `octo-issue-notify`. No per-step event
     filtering needed.
- Trade-off (acknowledged): one action with two POST branches is slightly less
  single-purpose than a pure-IM action, but they share ~80% core and the mapping
  logic is kept out at the workflow layer — saving a component outweighs one
  branch.

---

## 4a. Issue Triage (cross-plane concern — being redesigned)

Issue triage spans planes 4/5/6. It currently **emerged** from independent
workflows rather than being designed, and its core function — **classification**
— is missing. This section is the redesign baseline.

### Current state (measured across 25 repos, 2026-06)

The triage lifecycle has 6 stages. Coverage today:

| Stage | Goal | Central reusable | State |
|---|---|---|---|
| 1 Welcome | Greet new issue, guide info | `issue-welcome` | ✅ |
| 2 Add-to-board | Add to Octo Board + set Module | `auto-add-to-project` | ✅ (Module via **hardcoded repo→module table**) |
| 3 Notify | Push to IM issue-feed | `octo-issue-feed` | ✅ |
| 4 **Classify** | Label by type/module/priority | **— none —** | ❌ **the core of triage is absent** |
| 5 Route | Assign / link sprint | — (PR-only via auto-add) | ❌ for issues |
| 6 Lifecycle | stale + close | `reusable-stale` | ✅ |

**Coverage is two worlds:**
- **Octo product line (21 repos)** — welcome/auto-add/issue-feed/stale four-pack
  is ~100% consistent (good template propagation). These get full triage.
- **Out of scope (DECIDED):** issue automation serves the **product line only**.
  The following are **excluded** and any existing issue automation is **removed**:
  - `.github`, `community` — infrastructure / meta repos. **Remove** their
    welcome / auto-add / issue-notify / stale callers (full exit, incl. stale).
    *Trade-off accepted:* `community` (the community hub) loses auto-board / IM /
    welcome / stale on its issues — manual ops henceforth; reversible later.
  - `openclaw`, `hermes-agent` — independent sub-projects with their own
    ecosystems. Already outside the four-pack. `openclaw`'s own `stale.yml` is
    self-managed — **leave it alone** (not part of org triage).
  - `cc-channel-octo`, `hermes-channel-octo`, `octo-website` — currently bare /
    no triage; left as-is (not onboarded).

This establishes a clean boundary: **issue automation is for the product line;
meta repos and independent projects govern themselves.**

**Three structural problems (verified):**
1. **All 76 triage callers pin `@main`** (76/76). The §5 supply-chain risk is
   not theoretical here — one bad `.github` commit alters issue
   welcome/board/notify across 21 repos instantly. Triage is the
   first-impression surface for external contributors; errors here cost most.
   → Fixed by re-pinning to `@v1` during this redesign (Wave 2).
2. **No issue classification exists.** `pr-labeler` is PR-only. Issue labels come
   solely from template presets (`bug_report.yml` → `labels:["bug"]`) + humans.
   `issue-welcome`'s "bug vs feature" branch therefore relies on hardcoded
   template labels, not content — the triage *brain* is missing.
   → Fixed by the agent webhook (this section).
3. **Trigger drift.** `issue-welcome` fires on `[opened]`; `octo-issue-feed` on
   `[opened, reopened]`. No unified triage trigger contract.
   → Fixed by unifying on `[opened]` (this section).

### Decision: classification is fully externalized to a triage agent

**The classification brain is NOT implemented in workflows.** Issue events are
forwarded to an external **triage agent** via webhook
(`dev.xming.ai/.../autopilots/...`). The agent owns all triage logic (labeling,
classification, routing). This is **Octo dogfooding its own product thesis** —
"put an AI agent into the collaboration layer to do triage."

Consequence — no triage logic lives in any workflow. The webhook POST is added
as the **webhook mode of `octo-issue-notify`** (the renamed `octo-issue-feed`),
so the same issue workflow that already pushes IM now also forwards to the agent:

```
issue event → octo-issue-notify → [IM mode] Octo IM
                                 → [webhook mode] POST agent → agent labels/comments
```

This **eliminates** the previously-considered `issue-classify` composite action,
the classify→label→board job orchestration, all LLM key/prompt/fallback handling,
**and** a separate forwarder workflow — the capability folds into the existing
issue notification workflow via `octo-notify`'s webhook mode.

### Governing principle

Separate **reliable / instant / deterministic / GitHub-native facts** from
**intelligent / async / content-derived enrichment**. The agent is a single
**external** dependency: it should own only what nothing else can do
(classification), and reliability-critical native primitives must never sit on
its critical path. The agent is scoped as a *triage* agent (classify + route) —
greeting, IM notification and board writes are out of its remit.

→ **The agent's contract: it emits LABELS and a triage COMMENT on the issue
(its classification rationale — why these labels, what info is missing, repro
adequacy, suspected duplicate). It does NOT send IM notifications and does NOT
write to the project board.**

### Replacement matrix — DECIDED

| Existing | Decision | Reason |
|---|---|---|
| `issue-welcome` | ✅ **KEEP native** | First-impression for external contributors must be instant + reliable; cannot depend on external agent uptime. **Orthogonal to the agent comment**: welcome = deterministic emotional greeting + generic guidance (thanks, links, community); agent comment = intelligent, possibly-delayed triage verdict (what this issue is missing, how it's classified). Both coexist without redundancy. |
| `octo-issue-feed` → `octo-issue-notify` | 🔧 **RENAME + extend** | Keeps native IM push (survives agent downtime); **gains webhook mode** that forwards the event to the triage agent. No separate forwarder workflow. |
| `auto-add-to-project` (board add + Module) | ✅ **KEEP native** | Board add needs `PROJECT_TOKEN` (privileged) — do **not** expand org-project write to an external agent. Repo→module mapping is deterministic & reliable. |
| `auto-add` **PR path** | ✅ **KEEP** | Plane-5 PR flow, orthogonal to issue triage. |
| `reusable-stale` | ✅ **KEEP** | `schedule`-triggered lifecycle, different trigger semantic. |
| classification | ➕ **via webhook mode** | The one missing capability, added with **zero new workflows** — folded into `octo-issue-notify`. Agent contract scoped (label + triage comment; no notify, no board) → bounded, reliable. |

**Net workflow count: unchanged (3 issue-triggered workflows).** Classification
is added without a new file by reusing `octo-notify`'s webhook mode inside the
renamed issue workflow. This is the strongest form of "minimize": new capability,
no new component. Putting classification on the agent does **not** move IM onto
the agent's critical path — IM stays native, so notification survives agent
downtime.

**Future simplification (not now):** the agent emits content-based `module:*`
labels (more accurate than the repo→module **hardcoded table** in `auto-add`,
e.g. a CLI issue filed in octo-server). Once the agent's module label proves
reliable, the hardcoded table can be **retired** and `auto-add` consumes the
label. No workflow-count change; removes one maintenance burden.

### Event granularity — DECIDED: `[opened]` (IM and webhook unified)

Single criterion: *does this event genuinely warrant triage?* IM and webhook
subscribe to the **same** set.

| Event | Subscribe? | Reason |
|---|:--:|---|
| `opened` | ✅ | The point of triage: a new, unknown issue. Highest value for both classification and team awareness. |
| `reopened` | ❌ | The issue is **already known and was triaged at open time**; reopen rarely changes type/module. Reopen is a **deliberate human action** (usually a maintainer) — a person is already in the loop, which is exactly when AI triage is *not* needed. Agent would re-post a near-identical verdict (noise). IM value of "#X reopened" is weak. **(Narrows current `octo-issue-feed`, which is `[opened, reopened]` — intended behavior change.)** |
| `edited` | ❌ | Most edits (typo/format/maintainer tweak) don't change classification; firing per-edit is low signal-to-noise for triage and pure noise for IM. |
| `labeled` / `unlabeled` | ❌ | **Feedback loop**: agent labels → labeled event → fire → agent labels… |
| `issue_comment` | ❌ | High volume + loop risk; not needed initially. |

**Self-consistency:** with `[opened]` only, no agent action (label/comment) can
re-trigger the workflow — the agent does not open issues. No loop possible.

**Known optional extension (not now):** first-time contributors often open a thin
issue then immediately edit to complete it; with `opened`-only the agent triages
the thin version and won't re-read after completion. If this proves painful,
`edited` is the one event worth adding — but it brings edit-noise to IM too (the
sets stay unified). Deferred: adding an event later is a cheap increment; start
minimal.

### Endpoint topology — DECIDED

Single unified webhook URL; the JSON payload carries `repo` / `issue` / `action`
and the agent disambiguates. Simplest distribution: one URL + one shared auth
secret org-wide.

### Webhook auth & egress — DECIDED

- **Request auth**: none. A plain `POST` to the autopilot URL; the `awt_...` token
  in the URL path is the capability (capability-based auth).
- **But the URL is therefore a secret.** Repos are public — hardcoding the URL in
  a public workflow YAML would expose it to the world, letting anyone forge issue
  payloads (burn agent quota; trick the agent into labeling/commenting arbitrary
  issues). Therefore:
  > **Store the URL as an org-level secret (e.g. `TRIAGE_WEBHOOK_URL`); the caller
  > passes it via `secrets:` and the reusable reads
  > `${{ secrets.TRIAGE_WEBHOOK_URL }}`. NEVER hardcode it in public YAML.**

  Same distribution mechanism as `OCTO_BOT_TOKEN` / `PROJECT_TOKEN` — zero new
  machinery. No-auth-header (per decision) and URL-not-leaked (public-repo
  baseline) are not in conflict.
- **Egress scope**: the issue payload (title/body — may contain user-pasted
  secrets) leaves to an external domain (`dev.xming.ai`). This is intended
  (first-party triage agent). The webhook step executes nothing (no injection risk
  on our side); the **agent** owns its own prompt-injection defense.

### Open questions

All §4a design decisions are resolved. Remaining items are sequencing only:

- **Depends on Wave 1**: `@v1` re-pinning needs the real `v1` tag to exist first
  (§5 versioning). The triage redesign therefore lands in Wave 2, after the
  versioning foundation.

§4a is otherwise complete and ready to implement on approval.

---

## 5. Foundation: versioning & distribution (P0 — everything rests on this)

The reason this central repo exists was undermined: it was not giving consumers a
stable, auditable version to pin to. **Wave 1 (in progress) fixes this.**

**Original broken state (verified):**
- `v1` and `v2` both pointed to the same commit (#31) — major tags meaningless.
- Both tags lagged far behind `main` (29 commits) — fixes only on `main`.
- Every real caller pinned `@main`; the only `@v1` strings were usage examples.

**Pinning consumers to a movable `@main` is a supply-chain anti-pattern** for a
trust root that holds secrets across ~21 repos: one bad commit to `main` hits all
of them instantly, with no rollback anchor and no audit of which repo runs what.

**Resolution (Wave 1):**
1. **SemVer**: immutable `vX.Y.Z` tags + a rolling `vX` major alias. `v1.0.0` cut
   from current `main`; `v1` rolls to it; the meaningless `v2` is deleted.
2. **All callers pin rolling `@v1`** (full migration); usage docs unified.
3. **Release automation**: `.github/workflows/release.yml` moves the `vX` alias
   and creates/updates the GitHub Release on every `vX.Y.Z` tag push (stable
   releases only; pre-releases do not advance the alias).
4. **Rename via shim**: `octo-issue-feed.yml` → `octo-issue-notify.yml` (canonical).
   During transition the old path was a thin pass-through shim. **Resolved in
   v1.1.0**: all callers migrated to `octo-issue-notify.yml@v1`, the shim has zero
   consumers and was removed.
5. **Distribution = "both" model:**
   - **Enforced gates** (history-check, check-sprint, dependency-review,
     secret-scan, language quality) → org **required workflows / rulesets**, so
     no per-repo opt-in is needed. *This is what fixes the #65 failure mode.*
   - **Optional pieces** → `.github/workflow-templates/` starter workflows for
     one-click scaffolding of new repos, keeping callers uniform.

**Internal-ref isolation — RESOLVED in v1.1.0:** the reusables' own internal
`uses:` (the notify workflows → `octo-notify`) now pin `@v1`, not `@main`. A
`@v1` caller therefore gets a fully version-frozen graph (workflow *and* its
transport action), closing the partial isolation leak that existed at v1.0.0.
(They could not be `@v1` at v1.0.0 because the prior `v1`/#31 snapshot predated
the `octo-notify` action from #66; once `v1` rolled onto a commit containing it,
the refs were tightened and `v1.1.0` cut.)

---

## 6. Local git hooks (L0) — explicitly NOT part of the central system

Git hooks are **single-repo, local developer DX**. They invoke commands the repo
**already defines** (its own `gofmt`, `prettier`, `gitleaks`). There is **no
shared logic to centralize** — unlike reusable workflows, which share GraphQL/IM/
sprint logic across repos.

Therefore:
- Hooks are **owned by each repository**, committed in that repo, and travel with
  it. `.github` does **not** version, enforce, or centrally host them.
- The framework need not even be uniform across repos — there is nothing to share
  between them. A repo may use lefthook, husky, or pre-commit as it prefers.
- `.github` may offer a **documentation example / optional starter** only.
- Their entire value is local: fewer format/secret mistakes before push. Purely
  **advisory**.

**The single principle the central blueprint records about L0:**

> Repositories are encouraged to add a local pre-commit/pre-push hook for fast
> feedback (format, changed-file lint, gitleaks). But **every rule that must be
> enforced has an equivalent gate in CI**, because hooks are bypassable and fork
> contributors do not have them.

Recommended (non-binding) L0 contents:
- pre-commit: format, changed-file lint, **gitleaks** (custom rules), basic
  hygiene (trailing whitespace / EOF / large files).
- pre-push: build + fast unit tests.
- **Not** commit-msg (squash makes it noise); **not** heavy scans (schedule CI).

> Note: earlier design iterations explored centralizing hooks via lefthook
> `remotes:` / `@v1`. **Rejected** — it imposed central-governance overhead on an
> object that has no shared logic. Hooks stay per-repo and self-governed.

---

## 7. Implementation waves (each independently verifiable)

Nothing is built ahead of its wave's approval.

1. **Wave 1 — Foundation (P0):** versioning (immutable `vX.Y.Z` + rolling `vX`),
   release-alias workflow, rulesets skeleton. *Without this, everything else is
   loose.*
2. **Wave 2 — Zero-risk increments:** `octo-notify` composite (IM + webhook
   modes) + refit the 4 notification workflows; rename `octo-issue-feed` →
   `octo-issue-notify` and add triage webhook mode (callers re-pinned `@main` →
   `@v1` in the same change); `reusable-dependency-review`;
   `reusable-secret-scan`; `reusable-pr-title-lint`.
3. **Wave 3 — Rebuild (overrides #65, confirmed):** slimmed `reusable-go-quality`
   + `reusable-node-quality`, distributed via rulesets (not opt-in).
4. **Wave 4 — Re-position:** CodeQL → weekly schedule, scoped to high-risk repos
   only.
5. **Wave 5 — Consistency:** unify runner (`ubuntu-24.04`) and `actions/checkout`
   pins (Dependabot convergence); starter workflow templates; documentation.

---

## 8. Coverage matrix (repo archetype × plane)

⚠️ Languages for mobile / adapters / matter / speech / smart-summary are
**inferred** — confirm before Wave 3/4 implementation.

| Repo archetype | Lang CI | dep-review | secret-scan | CodeQL (weekly) | pr-title | release | board | IM |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Go service (server/im/fleet) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Go lib/CLI (lib/cli/version-sync) | ✅ | ✅ | ✅ | ❌ (gosec suffices) | ✅ | ✅ | ✅ | ✅ |
| Web/TS (web/admin) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mobile (ios/android) | self-managed | ✅ | ✅ | ❌ (lang unsupported) | ✅ | self | ✅ | ✅ |
| Adapters (adapters/channel×2) | by language | ✅ | ✅ | by language | ✅ | ✅ | ✅ | ✅ |
| Infra (.github/community/deployment) | n/a | ✅ | ✅ | ❌ | ✅ | n/a | ✅ | partial |

---

## 9. Single-source-of-truth audit (no contention)

| Fact | Sole owner | Notes |
|---|---|---|
| `size/*`, `dependencies-changed` labels | `reusable-pr-labeler` | |
| `stale` label | `reusable-stale` | |
| Sprint value | `auto-add-to-project` (write) → `reusable-check-sprint` (read) | Only intentional shared-state coupling; idempotent |
| main-branch history quality | `reusable-pr-title-lint` | Squash → PR title is the record |
| Outbound transport (IM + webhook) | `actions/octo-notify` | Mappings stay per-workflow |

---

*Maintained by @Mininglamp-OSS/maintainers. Changes to this document follow the
same review path as workflow changes (CODEOWNERS).*
