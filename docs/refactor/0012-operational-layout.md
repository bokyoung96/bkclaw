# Operational Layout

## Desired top-level shape

The repository root should primarily contain:
- project metadata (`README.md`, `pyproject.toml`, `requirements.txt`)
- build/runtime definitions (`Dockerfile.gaejae`, `.env.example`)
- protected persona/operating-rule files
- directories (`bin/`, `scripts/`, `src/`, `docs/`, `tests/`)

## Command locations

- user-facing operational commands: `bin/`
- implementation scripts: `scripts/`
- reusable Python logic: `src/`

This keeps the repo easier to scan and reduces the chance of dumping one-off executables at root.
