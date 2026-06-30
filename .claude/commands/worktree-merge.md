Merge worktree branch(es) back to main and clean up. Argument: $ARGUMENTS (optional: branch name or worktree path)

Follow this workflow strictly:

1. **Identify targets** — resolve what to merge:
   - If `$ARGUMENTS` is empty: discover ALL worktrees under `.trees/` via `git worktree list`, process each one sequentially
   - If it's a path (e.g., `.trees/feature-x`), extract the branch name from `git worktree list`
   - If it's a branch name (e.g., `feature/x`), locate its worktree path
   - Run `git worktree list` to confirm it exists

2. **Verify worktree is clean** — check for uncommitted changes in the worktree:
   ```bash
   git -C <worktree-path> status --porcelain
   ```
   If dirty, stop and report what's uncommitted.

3. **Run checks in worktree** — ensure quality before merging:
   ```bash
   cd <worktree-path> && make check && make test
   ```
   If checks fail, stop and report.

4. **Switch to main repo** — ensure we're on main and up to date:
   ```bash
   cd <repo-root>
   git checkout main && git pull
   ```

5. **Merge** — fast-forward if possible, otherwise merge commit:
   ```bash
   git merge <branch-name> --no-ff -m "Merge <branch-name>"
   ```

6. **Remove worktree and branch** — clean up completely:
   ```bash
   git worktree remove <worktree-path>
   git branch -d <branch-name>
   ```

7. **Remove .trees/ if empty** — after all merges, delete the directory if nothing remains:
   ```bash
   rmdir .trees 2>/dev/null || true
   ```

8. **Verify** — run `git log --oneline -5` and `git worktree list` to confirm merges landed and worktrees are gone.

For each worktree processed, repeat steps 2–6. If any worktree fails checks, skip it and continue with the rest — report failures at the end. Run steps 7–8 once at the end.

Report: branches merged, branches deleted, worktrees removed, .trees/ status, any skipped (with reason), current HEAD.
