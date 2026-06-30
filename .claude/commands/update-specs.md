Update SPECS.md to reflect the current state of the project. Argument: $ARGUMENTS (optional: specific section to focus on)

Follow this workflow:

1. **Read current state** — gather facts from these sources:
   - `pyproject.toml` — name, version, description, dependencies, Python version
   - `uv.lock` — actual resolved dependency versions
   - Directory structure — modules, test files, docs
   - `SPECS.md` — current declared state

2. **Identify drift** — compare declared SPECS.md against actual project state:
   - New modules not listed in Module Boundaries?
   - New dependencies not in Tech Stack?
   - Public API symbols not documented?
   - Architecture changes not in Decision Log?

3. **Update sections** — modify SPECS.md with verified facts:
   - **Identity**: Update version, description if changed in pyproject.toml
   - **Tech Stack**: Add/remove based on actual dependencies
   - **Module Boundaries**: List all modules with their actual responsibilities
   - **API Surface**: Document public exports from `__init__.py` and key modules
   - **Testing Strategy**: Update coverage targets based on test count/structure
   - **Deployment**: Reflect actual deployment configuration
   - **Decision Log**: Add entry for any significant changes detected

4. **Preserve manual content** — do NOT overwrite:
   - Decision Log entries (append only)
   - Constraints (unless explicitly asked)
   - Custom notes or annotations added by developers

5. **Verify** — read the updated SPECS.md and confirm:
   - All modules listed match actual directory structure
   - Dependency list matches pyproject.toml
   - No stale references to removed code

Report what changed: sections updated, new entries added, stale entries flagged.
