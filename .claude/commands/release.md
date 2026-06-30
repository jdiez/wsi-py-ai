Release the project: update docs, changelog, commit, tag, and push. Argument: $ARGUMENTS (patch|minor|major)

Follow this workflow strictly:

1. **Validate** — confirm argument is one of `patch`, `minor`, or `major`. If missing or invalid, stop and ask.

2. **Determine version** — read current version from `pyproject.toml`, compute the new version:
   - `patch`: 0.4.1 → 0.4.2
   - `minor`: 0.4.1 → 0.5.0
   - `major`: 0.4.1 → 1.0.0

3. **Gather changes** — run `git log --oneline <last-tag>..HEAD` to see all commits since the last release.

4. **Update CHANGELOG.md** — add a new section at the top following the existing format:
   ```
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added
   - ...

   ### Changed
   - ...

   ### Fixed
   - ...
   ```
   Only include sections (Added/Changed/Fixed/Removed) that have entries. Summarize commits into user-facing descriptions.

5. **Update version** — bump the version in `pyproject.toml` (`[project] version = "X.Y.Z"`).

6. **Update SPECS.md** — if it exists, update the Identity table version.

7. **Update README.md** — only if version is referenced there.

8. **Verify** — run `make check && make test` to confirm nothing is broken.

9. **Commit** — stage all modified files and commit:
   ```
   Release vX.Y.Z
   ```

10. **Tag** — create an annotated tag:
    ```bash
    git tag -a vX.Y.Z -m "vX.Y.Z: <one-line summary of release>"
    ```

11. **Push** — push commit and tag to origin:
    ```bash
    git push origin main --tags
    ```

Report the new version, changelog entries added, and the pushed tag.
