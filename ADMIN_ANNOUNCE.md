# Admin Notice: Repository History Rewritten

The repository history was rewritten to remove sensitive and generated files (`.env`, `venv/`, `reports/`, `screenshots/`). Please follow these steps to sync your local clone and restore working state.

Immediate actions for contributors

1. Rotate any credentials you control that may have been committed to this repo previously.

2. Recloning (recommended):

```bash
rm -rf your-local-clone
git clone https://github.com/CivicDataLab/IDS-DRR-QA-Automation.git
```

3. If you cannot reclone, resync your current clone (risky; prefer reclone):

```bash
git fetch origin --prune
git checkout main
git reset --hard origin/main
```

4. CI & Secrets:
- GitHub Actions has been disabled for the rewrite window — verify workflows are re-enabled and required secrets are set in Settings → Secrets.
- Required secrets: `URL`, `DEV_URL`, `HOME_URL_4`, `HOME_URL_USERNAME`, `HOME_URL_PASSWORD`, `QA_REPO_PAT`.

5. Contact & support:
- Maintainers: @maintainer1, @maintainer2
- Security: replace `leave-the-email-for-now` in `SECURITY.md` with a monitored contact.

Admin notes:
- Backups and pre-rewrite scans are available to admins at `/Users/home/repo-backups` on the admin machine.
- If you had local branches with unpushed commits, coordinate before recloning.
