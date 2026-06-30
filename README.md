# wsi-py-ai

[![Release](https://img.shields.io/github/v/release/jdiez/wsi-py-ai)](https://img.shields.io/github/v/release/jdiez/wsi-py-ai)
[![Build status](https://img.shields.io/github/actions/workflow/status/jdiez/wsi-py-ai/main.yml?branch=main)](https://github.com/jdiez/wsi-py-ai/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jdiez/wsi-py-ai/branch/main/graph/badge.svg)](https://codecov.io/gh/jdiez/wsi-py-ai)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jdiez/wsi-py-ai)](https://img.shields.io/github/commit-activity/m/jdiez/wsi-py-ai)
[![License](https://img.shields.io/github/license/jdiez/wsi-py-ai)](https://img.shields.io/github/license/jdiez/wsi-py-ai)

WSI Processing Pipeline — ingestion, de-identification, registry, DataLoader optimization, and automated QA for whole slide images. Dual-mode: local on-premise and GCP cloud.

- **Github repository**: <https://github.com/jdiez/wsi-py-ai/>
- **Documentation**: <https://jdiez.github.io/wsi-py-ai/>

## Getting started

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:YOUR_HANDLE/YOUR_PROJECT.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Install the environment and the pre-commit hooks with:

```bash
make install
```

This will also generate your `uv.lock` file.

### 3. Run the pre-commit hooks

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

### 5. Set up branch protection (recommended)

Go to **Settings > Branches > Add rule** for `main`:

- Require pull request reviews before merging
- Require status checks to pass (select `quality` and `tests-and-type-check`)
- Require branches to be up to date before merging

---

Repository initiated with [cookie-claude](https://github.com/jdiez/cookie-claude).
