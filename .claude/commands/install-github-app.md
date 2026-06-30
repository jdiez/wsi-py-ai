Install the Claude Code GitHub Action on this repository. Argument: $ARGUMENTS (optional: Anthropic API key)

This sets up `anthropics/claude-code-action` so Claude responds to @claude mentions in PR comments and reviews.

Follow this workflow strictly:

1. **Check prerequisites**:
   ```bash
   gh auth status
   gh repo view --json name,owner --jq '.owner.login + "/" + .name'
   ```
   If `gh` is not authenticated, stop and ask the user to run `gh auth login`.

2. **Verify workflow file exists** — confirm `.github/workflows/claude-code.yml` is present:
   ```bash
   cat .github/workflows/claude-code.yml
   ```
   If missing, create it with the standard configuration (triggers on `@claude` in PR comments and reviews).

3. **Set the API key secret**:
   - If `$ARGUMENTS` contains an API key, use it directly
   - Otherwise, check if `ANTHROPIC_API_KEY` already exists: `gh secret list | grep ANTHROPIC_API_KEY`
   - If not set, ask the user for their key, then:
   ```bash
   gh secret set ANTHROPIC_API_KEY --body "<key>"
   ```

4. **Verify repository permissions** — the workflow needs these enabled:
   ```bash
   gh api /repos/{owner}/{repo}/actions/permissions --jq '.enabled'
   ```
   If Actions are disabled, report and ask user to enable.

5. **Test the setup** — create a test comment to verify (optional, ask first):
   ```bash
   # Find an open PR to test on
   gh pr list --state open --limit 1
   ```

6. **Report**:
   - Workflow file: present/created
   - ANTHROPIC_API_KEY secret: set
   - Actions permissions: enabled
   - Trigger: `@claude` in PR comments and reviews
   - Any manual steps remaining
