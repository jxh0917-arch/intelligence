# GitHub Publishing Guide

The local repository is ready to publish. It contains two commits:

1. `6adad9d Organize chameleon tongue coursework workflow`
2. `09326ae Add model selection analysis`

## Recommended Repository Settings

- Repository name: `chameleon-tongue-workflow`
- Visibility: private unless redistribution of the coursework CSV files is explicitly permitted.
- Default branch: `main`
- Do not initialise the GitHub repository with a README, `.gitignore`, or license if pushing this local repository directly.

## Publish Through Codex

Codex can complete the upload when one of these is available:

- a GitHub repository URL, for example `https://github.com/jxh0917-arch/chameleon-tongue-workflow.git`;
- GitHub App access installed for the target repository;
- explicit approval to use the logged-in browser session as a fallback for creating or configuring the repository.

## Manual Push Commands

From this directory:

```powershell
git remote add origin https://github.com/jxh0917-arch/chameleon-tongue-workflow.git
git push -u origin main
```

If `git` is not on `PATH`, use the bundled Git executable already used for this repository:

```powershell
& 'C:\Users\10444\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' remote add origin https://github.com/jxh0917-arch/chameleon-tongue-workflow.git
& 'C:\Users\10444\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe' push -u origin main
```

After publishing, GitHub Actions should run the workflow in `.github/workflows/python.yml` and execute `pytest -q`.
