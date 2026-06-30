Create a new Python module with proper conventions. Argument: $ARGUMENTS (module name)

1. **Branch** — create a feature branch from main:
   ```bash
   git checkout main && git pull
   git checkout -b feature/add-$ARGUMENTS
   ```
2. Create `src/wsi_py_ai/$ARGUMENTS.py` (or flat layout equivalent) with:
   - Module docstring (Google style)
   - structlog logger: `logger = structlog.get_logger("wsi_py_ai.$ARGUMENTS")`
   - Type annotations on all functions
2. Create matching test file `tests/test_$ARGUMENTS.py` with:
   - Import from the new module
   - At least one test function
3. Run `uv run ruff check --fix` and `uv run ruff format` on both files
4. Run `uv run mypy` to verify types pass
5. Run `uv run python -m pytest tests/test_$ARGUMENTS.py -v` to verify tests pass
6. **Update SPECS.md** — add module to Module Boundaries table, document public API
7. **Commit** on the feature branch with a descriptive message
