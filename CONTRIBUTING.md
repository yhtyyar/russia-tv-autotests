# Contributing to russia-tv-tests

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Install dependencies:
   ```bash
   uv sync --extra dev
   uv run playwright install
   ```

## How to Add a New Test

### Unit Test

1. Create `tests/unit/test_<module>.py`
2. Use `pytest` and follow the existing naming conventions:
   - `Test<ClassName>` for test classes
   - `test_<action>_<condition>` for test methods
3. Run with `uv run pytest tests/unit/ -v`

### Integration Test

1. Create `tests/integration/test_api_<resource>.py`
2. Use `httpx.AsyncClient` and the existing API clients in `api/`
3. Mark with `@pytest.mark.integration`
4. Run with `uv run pytest tests/integration/ -v`

### E2E Test

1. Create `tests/e2e/test_<feature>.py`
2. Use the `page` fixture from `conftest.py`
3. Reuse Page Objects from `pages/`
4. Mark with `@pytest.mark.e2e`
5. Run with `uv run pytest tests/e2e/ -v`

## Code Style Guidelines

- **Type hints**: All public methods must have type annotations
- **Docstrings**: Google style (`Args`, `Returns`, `Raises`)
- **Ruff**: Run `uv run ruff check .` and `uv run ruff format .`
- **MyPy**: Run `uv run mypy .`
- **Bandit**: Run `uv run bandit -r api/ core/ pages/ utils/ config/`

## Git Workflow

1. Create a feature branch from `master`:
   ```bash
   git checkout -b feat/<short-description>
   ```
2. Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(api): add new endpoint test`
   - `fix(e2e): stabilize flaky navigation test`
   - `docs(readme): update installation instructions`
3. Push your branch and open a Pull Request
4. Ensure CI passes before requesting review

## Code Review Process

- All PRs require at least one approval
- CI must be green (unit, integration, lint jobs)
- E2E tests run on Chromium and Firefox matrices
