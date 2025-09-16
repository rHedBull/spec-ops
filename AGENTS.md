# Repository Guidelines

## Project Structure & Module Organization
Core CLI logic lives in `src/specify_cli`, exposing the `specops` Typer app defined in `__init__.py`. Shell automation for task and milestone workflows sits in `scripts/`, while reusable authoring templates are stored under `templates/`. Long-form guidance and DocFX content are in `docs/`, reference materials for agent memories reside in `memory/`, and rich media assets live in `media/`. Keep new modules colocated with their domain resources so bootstrapped projects inherit a coherent layout.

## Build, Test, and Development Commands
Install dependencies with `uv sync`, which pins toolchains via `pyproject.toml` and `uv.lock`. Run the CLI locally using `uv run specops --help` to sanity-check command registration. Exercise the bootstrap flow with `uv run specops init demo --here --ai claude --ignore-agent-tools`, swapping agent flags as needed. Convenience scripts in `scripts/` are executable with `bash scripts/update-task-status.sh` (or similar) and should remain POSIX-compliant.

## Coding Style & Naming Conventions
Follow PEP 8 defaults: four-space indentation, `snake_case` for functions, `PascalCase` for Typer command classes, and uppercase module constants. Prefer type hints and keep Rich/typer output formatting centralized through helper functions rather than scattered print statements. When updating templates or memory files, preserve the concise, agent-ready tone and avoid introducing non-ASCII characters unless already present.

## Testing Guidelines
There is no packaged test suite yet, so each change must be validated by exercising the CLI commands above and confirming generated project scaffolding looks correct. When adding automated coverage, place tests under `tests/` and use `pytest` with `typer.testing.CliRunner` to simulate command invocations. Keep fixtures lightweight and mirror real template paths so regressions surface early. Document notable manual verification steps in the pull request for future automation.

## Commit & Pull Request Guidelines
Commits follow a Conventional Commits style (`feat:`, `fix:`, etc.), so use the imperative mood and scope prefixes where helpful. Group related work into focused commits, run `uv run specops --help` before staging, and update docs or templates alongside behavior changes. Pull requests should describe the scenario, list manual or automated checks, and link any relevant issues; screenshots or terminal captures are encouraged when they explain CLI UX changes. Review CONTRIBUTING.md and SECURITY.md before proposing substantial process updates.

## Agent & Template Updates
Changes that affect AI agent workflows must update the matching files in `templates/` and any supporting guidance in `memory/constitution.md`. Call out downstream impacts on bootstrap flows or generated documentation so maintainers can refresh published artifacts promptly.
