# Repository Guidelines

## Project Structure & Module Organization
- `src/` contains the feature engineering, model utilities, evaluation, and configuration modules that power training and inference.
- `training/main.py` runs the end-to-end pipeline; `training/modular/` holds entry points for partial workflows, and `training/train_terminal.py` supports CLI-driven sessions.
- `api/app.py` and `api/prediction.py` expose the prediction service; launch artifacts live in `models/deployed/`.
- `scripts/` provides ready-made helpers such as `batch_predict.py` and `predict_single.py` for ad-hoc predictions.
- `data/raw/`, `data/processed/`, and `data/features/` store staged datasets; keep large or private inputs out of version control.
- `tests/` organizes fixtures, integration checks, and coverage tooling; refer to `docs/` for environment guides and deployment notes.

## Build, Test, and Development Commands
- Install runtime dependencies with `python -m pip install -r requirements.txt`; use virtual environments to isolate toolchains.
- Run the full training pipeline via `python training/main.py --run-all`, or limit scope with flags such as `--data`, `--features`, or `--train --optimize`.
- Start the FastAPI service locally using `uvicorn api.app:fastapi_app --reload --host 0.0.0.0 --port 8000` once a model exists in `models/deployed/`.
- Batch prediction utilities: `python scripts/batch_predict.py --input data/raw/sample.csv --output results/predictions.csv`.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and descriptive snake_case identifiers for functions, variables, and module filenames.
- Keep classes in PascalCase (`AdvancedPreprocessor`) and constants in UPPER_SNAKE_CASE, mirroring existing patterns in `src/config.py`.
- Format with `black` (default 88-character line width) and align imports using `isort`; lint with `flake8` before opening a PR.
- Adopt type hints when extending core modules and run `mypy src` to maintain static typing coverage where annotations already exist.

## Testing Guidelines
- Default test launcher: `python tests/run_tests.py`; target individual modules with `python tests/run_tests.py test_features`.
- Coverage gate is 80% (`pytest.ini`), enforced by `bash tests/run_coverage.sh`, which also generates HTML and XML reports under `htmlcov/` and `coverage.xml`.
- Name test files `test_*.py`, classes `Test*`, and functions `test_*`; use markers like `@pytest.mark.integration` or `@pytest.mark.slow` to categorize workload.
- Prefer fixtures from `tests/fixtures/` for dataset stubs, and add new fixtures there to keep deterministic behavior across CI and local runs.

## Commit & Pull Request Guidelines
- Write imperative, descriptive commit subjects (`Add Paperspace folder structure auto-creation guide`) capped near 72 characters; include scoped bodies for context.
- Reference related issues with `Fixes #123` when relevant, and squash noisy checkpoints or generated files before committing.
- PRs should outline intent, testing evidence (`Tests: python tests/run_tests.py`), and attach metrics or screenshots for model or API changes.
- Ensure CI passes, request review from domain owners (training, API, or tooling), and update documentation or notebooks affected by the change set.

## Security & Configuration Tips
- Store secrets (API keys, database URLs) in environment variables or `.env` files excluded from git; `MODEL_PATH` controls which artifact the API loads.
- Validate external datasets for PII before placing them in `data/raw/`; prefer encrypted storage for commercial data dumps.
- Monitor large artifacts in `models/` and `results/`; use Git LFS or external storage to prevent repository bloat.
- When deploying, review `setup/` scripts for environment-specific hardening steps and update them if infrastructure requirements change.
