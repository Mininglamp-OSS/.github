# OCTO Architecture Overview

> A map of the Mininglamp-OSS repositories: what each one does, how they fit
> together, and where to start reading if you want to contribute.
>
> New here? Read the [org profile](https://github.com/Mininglamp-OSS) for *what
> OCTO is* and the [Contributing Guide](../CONTRIBUTING.md) for *how to send a
> PR*. This document is *how the system is built*.

OCTO is an open-source, AI-native team-collaboration platform where humans and
AI agents share the same channels, threads, and tasks. The codebase is split
into many focused repositories rather than one monolith, organized into the
layers below.

---

## The 10,000-foot view

```
                        ┌────────────────────────────────────────┐
        Clients         │  octo-web   octo-ios   octo-android      │
   (humans + agents)    │  octo-admin   octo-chrome-extension      │
                        └───────────────────┬────────────────────┘
                                            │ REST + WebSocket
                        ┌───────────────────▼────────────────────┐
        Core backend    │  octo-server  ── octo-fleet (orchestr.) │
                        │  octo-im (WuKongIM real-time messaging)  │
                        │  shared foundation: octo-lib             │
                        └───────────────────┬────────────────────┘
                                            │
       Supporting       ┌───────────────────▼────────────────────┐
       services         │ octo-matter  octo-smart-summary          │
                        │ octo-speech  octo-search-indexer         │
                        └───────────────────┬────────────────────┘
                                            │ channel plugins / adapters
                        ┌───────────────────▼────────────────────┐
       Agent &          │ octo-adapters  openclaw(-channel-octo)   │
       integration      │ cc-channel-octo  claw-channel-octo       │
       layer            │ hermes-agent(-channel-octo)  multica     │
                        │ octo-cli  octo-daemon-cli  octo-version- │
                        │ sync                                     │
                        └───────────────────┬────────────────────┘
                                            │
       Ops & community   octo-deployment · octo-website · community · .github
```

---

## Layer by layer

### Core backend (Go)

| Repo | Role |
|------|------|
| [octo-server](https://github.com/Mininglamp-OSS/octo-server) | The control plane. REST & WebSocket APIs, Lobster (AI agent) orchestration, and the WuKongIM real-time messaging control layer. **Start here** to understand the API contract clients depend on. |
| [octo-fleet](https://github.com/Mininglamp-OSS/octo-fleet) | Runtime & bot orchestration, split out of octo-server. Manages agent/bot lifecycle and runtime. |
| [octo-im](https://github.com/Mininglamp-OSS/octo-im) | The IM brand/layer built on WuKongIM — "more than just IM." |
| [octo-im-plugins](https://github.com/Mininglamp-OSS/octo-im-plugins) | Official plugin collection for WuKongIM. |
| [octo-lib](https://github.com/Mininglamp-OSS/octo-lib) | Shared Go foundation: protocol types, crypto primitives, storage adapters, HTTP framework, event bus, worker pool. Most Go services import this. |

### Clients

| Repo | Role |
|------|------|
| [octo-web](https://github.com/Mininglamp-OSS/octo-web) | Web + desktop (Electron) client. One React + TypeScript codebase shipping both browser and PC surfaces. **The primary frontend.** |
| [octo-admin](https://github.com/Mininglamp-OSS/octo-admin) | Admin console — manage tenants, users, spaces, channels, and agents. React + Vite + Ant Design. |
| [octo-ios](https://github.com/Mininglamp-OSS/octo-ios) | iOS client (Objective-C). |
| [octo-android](https://github.com/Mininglamp-OSS/octo-android) | Android client (Java). |
| [octo-chrome-extension](https://github.com/Mininglamp-OSS/octo-chrome-extension) | Browser extension (Cmd+K) — pull web content into OCTO with context. |

### Supporting services (Go)

| Repo | Role |
|------|------|
| [octo-matter](https://github.com/Mininglamp-OSS/octo-matter) | Task & matter service — REST API, timeline tracking, LLM-powered extraction. |
| [octo-smart-summary](https://github.com/Mininglamp-OSS/octo-smart-summary) | LLM conversation summarisation — turns chats/threads into structured briefs. Any OpenAI-compatible backend. |
| [octo-speech](https://github.com/Mininglamp-OSS/octo-speech) | Speech-to-text microservice — multi-engine ASR (Gemini/GPT/Qwen) with context-aware correction. |
| [octo-search-indexer](https://github.com/Mininglamp-OSS/octo-search-indexer) | Message search — Kafka consumer + Elasticsearch bulk writer + Chinese tokenization. |

### Agent & integration layer

| Repo | Role |
|------|------|
| [octo-adapters](https://github.com/Mininglamp-OSS/octo-adapters) | Bridges AI agents, IM platforms, and external services into OCTO via OpenClaw channels and WebSocket. |
| [openclaw](https://github.com/Mininglamp-OSS/openclaw) | Personal AI assistant runtime — "the lobster way." |
| [openclaw-channel-octo](https://github.com/Mininglamp-OSS/openclaw-channel-octo) | OpenClaw channel plugin for OCTO. |
| [cc-channel-octo](https://github.com/Mininglamp-OSS/cc-channel-octo) | Bridges Claude Code (Claude Agent SDK) to OCTO IM as an independent Node.js gateway. |
| [claw-channel-octo](https://github.com/Mininglamp-OSS/claw-channel-octo) | OCTO channel plugin for WorkBuddy Claw. |
| [hermes-agent](https://github.com/Mininglamp-OSS/hermes-agent) / [hermes-channel-octo](https://github.com/Mininglamp-OSS/hermes-channel-octo) | The Hermes agent and its OCTO channel plugin (Python). |
| [multica](https://github.com/Mininglamp-OSS/multica) | Managed-agents platform — assign tasks, track progress, compound skills. *(Note: licensed under a modified Apache-2.0 — see its LICENSE.)* |
| [octo-cli](https://github.com/Mininglamp-OSS/octo-cli) | Metadata-driven CLI for agent bots — 48 operations, structured JSON I/O, non-interactive. |
| [octo-daemon-cli](https://github.com/Mininglamp-OSS/octo-daemon-cli) | Local runtime reporter — detects installed agent CLIs, reports status, supports remote upgrades. |
| [octo-version-sync](https://github.com/Mininglamp-OSS/octo-version-sync) | Upstream version aggregator — scans releases, drives daemon/plugin remote upgrades. |

### Ops, web presence & community

| Repo | Role |
|------|------|
| [octo-deployment](https://github.com/Mininglamp-OSS/octo-deployment) | Production Kubernetes manifests — Kustomize bases, overlays, secret templates, and a `setup.sh` one-command path. **Start here to run OCTO locally or in a cluster.** |
| [octo-website](https://github.com/Mininglamp-OSS/octo-website) | Official website. |
| [community](https://github.com/Mininglamp-OSS/community) | Community hub — discussions, Q&A, governance. |
| [.github](https://github.com/Mininglamp-OSS/.github) | Org profile, shared health files, issue/PR templates, reusable CI/CD workflows, and this doc. |

---

## Request flow (typical message)

1. A user or agent sends a message from a **client** (`octo-web` / mobile) over
   WebSocket.
2. **octo-server** authenticates, applies authorization, and hands real-time
   delivery to the **WuKongIM** layer (`octo-im`).
3. Messages are indexed asynchronously by **octo-search-indexer** (via Kafka)
   for search.
4. Agent participation is orchestrated by **octo-fleet**; external agents reach
   OCTO through the **channel plugins / adapters** layer.
5. Supporting services (**octo-matter**, **octo-smart-summary**, **octo-speech**)
   enrich threads with tasks, summaries, and transcription.

---

## Where to start as a contributor

| If you want to… | Look at |
|-----------------|---------|
| Run OCTO locally | [octo-deployment](https://github.com/Mininglamp-OSS/octo-deployment) (`setup.sh`) |
| Work on the backend API | [octo-server](https://github.com/Mininglamp-OSS/octo-server) → its `QUICKSTART.md` |
| Work on the web/desktop UI | [octo-web](https://github.com/Mininglamp-OSS/octo-web) → its `DEVELOPMENT.md` |
| Build an agent integration | [octo-adapters](https://github.com/Mininglamp-OSS/octo-adapters) + a channel plugin |
| Pick a starter task | Filter any repo by the [`good first issue`](https://github.com/search?q=org%3AMininglamp-OSS+label%3A%22good+first+issue%22+state%3Aopen&type=issues) label |

All standard repos are licensed **Apache-2.0** (multica uses a modified
Apache-2.0; see its LICENSE). Each repo carries its own `README`, `CONTRIBUTING`,
`SECURITY`, and `CODE_OF_CONDUCT`; org-wide defaults live in
[.github](https://github.com/Mininglamp-OSS/.github).
