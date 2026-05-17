# Contributing to Mininglamp-OSS

Thank you for your interest in contributing! This guide applies to all repositories under the Mininglamp-OSS organization.

## Issue or Discussion?

Not sure whether to open an Issue or a Discussion? Use this guide:

### Open an Issue when:
- You found a **reproducible bug** — include version, environment, and steps to reproduce
- You have a **small, concrete feature request** — well-scoped, no API or cross-repo impact

### Open a Discussion when:
- You have a **usage question** or need help → [Q&A](https://github.com/Mininglamp-OSS/community/discussions/categories/q-a)
- You have a **significant feature idea** — changes a public API, adds a new user-facing concept, affects more than one repo, or has notable UX/architectural impact → [Ideas](https://github.com/Mininglamp-OSS/community/discussions/categories/ideas)
- You have an **early-stage idea** to share → [Ideas](https://github.com/Mininglamp-OSS/community/discussions/categories/ideas)
- You built something with Octo → [Show and tell](https://github.com/Mininglamp-OSS/community/discussions/categories/show-and-tell)
- You're not sure → open a Discussion; maintainers will convert it to an Issue if needed

👉 **Community hub:** https://github.com/Mininglamp-OSS/community

## Getting Started

1. **Fork** the repository you want to contribute to.
2. **Clone** your fork locally.
3. **Create a branch** from `main` with a descriptive name:
   ```bash
   git checkout -b feat/short-description
   ```
4. Make your changes, following the guidelines below.
5. **Push** your branch and open a **Pull Request** against `main`.

## Branch Naming

| Prefix | Purpose |
|--------|---------|
| `feat/` | New feature |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `refactor/` | Code refactoring (no behavior change) |
| `test/` | Adding or updating tests |
| `chore/` | Maintenance, CI, tooling |

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

Optional body explaining the "why" behind the change.
```

**Examples:**
- `feat(auth): add OAuth2 PKCE flow`
- `fix(api): handle null response from upstream`
- `docs(readme): update installation steps`

## Pull Request Guidelines

- **One PR, one concern.** Don't mix unrelated changes.
- **All PRs must target `main`** and be rebased onto the latest `main` before requesting review.
- **Tests are required** for bug fixes and new features. No test = not done.
- **All CI checks must pass** before a PR can be reviewed.
- **Write in English.** Titles, descriptions, comments, code, and commit messages — all in English.

## Code Style

- Follow the conventions established in each repository.
- Run the project's linter and formatter before committing.
- If the repo has a pre-commit hook or CI check, make sure it passes locally first.

## Reporting Bugs

Use the repository's **Bug Report** issue template. Include:
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, runtime version, etc.)

## Suggesting Features

> **Significant features require a Discussion before an Issue.**
> See [GOVERNANCE.md](https://github.com/Mininglamp-OSS/community/blob/main/GOVERNANCE.md) for the full process.

1. **Open a Discussion** in the [Ideas](https://github.com/Mininglamp-OSS/community/discussions/categories/ideas) category of the community repository. A structured template is pre-filled automatically. Describe the problem, your proposed solution, and alternatives you considered.
2. **Discuss and refine.** Community members and the Project Lead (see [GOVERNANCE.md](https://github.com/Mininglamp-OSS/community/blob/main/GOVERNANCE.md)) will provide feedback. Iterate until there are no unresolved blocking concerns.
3. **The Project Lead marks the outcome.** Accepted Discussions are converted to a tracking Issue in the relevant repository, linked back to the Discussion. Declined or deferred outcomes are recorded in the Discussion with a rationale — see [GOVERNANCE.md](https://github.com/Mininglamp-OSS/community/blob/main/GOVERNANCE.md) for the full decision table.
4. **The Issue is scheduled** on the [Octo Board](https://github.com/orgs/Mininglamp-OSS/projects) and implementation begins.

**What counts as “significant”?** Anything that changes a public API, adds a new user-facing concept, affects more than one repository, or has notable UX or architectural implications. Bug-adjacent improvements, small ergonomic wins, and documentation changes are “minor” and may be filed directly as Issues using the **Feature Request** template.

Not sure which path to take? Open a Discussion — the Project Lead will guide you.

## Code of Conduct

All participants are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Not sure where to start? See the [Issue or Discussion?](#issue-or-discussion) guide above, or browse the [community hub](https://github.com/Mininglamp-OSS/community).
