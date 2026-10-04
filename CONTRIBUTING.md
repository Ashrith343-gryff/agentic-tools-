# Contributing Guidelines

Thank you for your interest in contributing to the Agentic Tool Decider! We welcome community contributions.

## Workflow

To contribute to this project, please follow these steps:

1. **Fork/clone**: Fork the repository on GitHub and clone it to your local machine.
2. **Create branch**: Create a new branch for your feature or bugfix. Name it descriptively, e.g., `feat/b01-decision-models` or `fix/typo-in-readme`.
3. **Implement issue**: Write your code. Ensure it is deterministic and works offline.
4. **Add tests**: Write `pytest` tests for your new code.
5. **Run pytest**: Ensure all tests pass by running `pytest` in the root directory.
6. **Run ruff**: Check your code style by running `ruff check .` (we use a line length of 99).
7. **Commit**: Write clear, descriptive commit messages. For example: `feat: add decision models`.
8. **Open PR**: Push your branch to your fork and open a Pull Request against the main repository. Title your PR clearly, linking to the issue if applicable, e.g., `[B01] Add decision models`.

## Branch and PR Naming Convention

- **Branches**: `feat/issue-name`, `fix/issue-name`, `docs/issue-name`
  - Example: `feat/b01-decision-models`
- **Commits**: Follow conventional commits: `type: description`
  - Example: `feat: add decision models`
- **PR Titles**: `[Issue-ID] Description`
  - Example: `[B01] Add decision models`

## Rules
- All code must be deterministic and work offline (no network required).
- NEVER include real API keys or secrets in your commits.
- Use Python 3.12 features and standard library where possible.
- The decider ONLY decides — it NEVER executes tools.
