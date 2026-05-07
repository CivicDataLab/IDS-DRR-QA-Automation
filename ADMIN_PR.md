# Admin PR Draft: Purge sensitive data and prepare repo for public release

This draft documents the non-destructive preparatory changes for publishing the repository.

Included in this branch:
- `CODE_OF_CONDUCT.md` (Contributor Covenant placeholder)
- `SECURITY.md` (placeholder contact — replace before public release)
- `.env.example` (example environment file; do NOT commit `.env`)

Next admin actions (not in this branch):
- Run the history purge (see `purge.sh` in admin notes) to remove `.env`, `venv/`, `reports/`, and `screenshots/` from history.
- Rotate any exposed credentials.
- Inform contributors to reclone after history rewrite.

See admin notes and `purge.sh` for detailed commands and backup procedure.
