# Contributing to Mininglamp-OSS

Thank you for your interest in contributing! This guide applies to all repositories under the Mininglamp-OSS organization.

## Getting Started

## Issue or Discussion?

Not sure whether to open an Issue or a Discussion? Use this guide:

### Open an Issue when:
- You found a **reproducible bug** — include version, environment, and steps to reproduce
- You have a **concrete feature request** — need is clearly defined with a specific use case

### Open a Discussion when:
- You have a **usage question** or need help → [Q&A](https://github.com/Mininglamp-OSS/community/discussions/categories/q-a)
- You have an **early-stage idea** to share → [Ideas](https://github.com/Mininglamp-OSS/community/discussions/categories/ideas)
- You built something with Octo → [Show and Tell](https://github.com/Mininglamp-OSS/community/discussions/categories/show-and-tell)
- You're not sure → open a Discussion; maintainers will convert it to an Issue if needed

👉 **Community hub:** https://github.com/Mininglamp-OSS/community


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

Use the repository's **Feature Request** issue template. Describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

## Code of Conduct

All participants are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

If you're unsure about anything, open a discussion or issue — we're happy to help.
