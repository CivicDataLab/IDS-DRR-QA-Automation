# Upstream Dispatch Setup

This QA repo (`CivicDataLab/IDS-DRR-QA-Automation`) accepts `repository_dispatch` events from two upstream repos:

- `CivicDataLab/IDS-DRR-Frontend`
- `CivicDataLab/IDS-DRR-Backend`

When either upstream repo deploys, it should fire a dispatch so the QA suite runs automatically against the just-deployed environment.

## Trigger map

| Upstream event | Dispatch payload | QA tests that run |
|---|---|---|
| Push/merge to `dev` → deploys to dev env | `environment: dev` | `pytest -m multistate` (4 shards) — multistate is the dev-only feature |
| Push/merge to `main` → deploys to prod env | `environment: prod` | `pytest -m "smoke or (analytics and not multistate) or component or dataset"` (3 shards) |

Routing in the QA repo is in [`.github/workflows/dispatch.yml`](../.github/workflows/dispatch.yml).

## Setup (do this once per upstream repo)

### 1. Create a fine-grained PAT

GitHub → Settings → Developer settings → **Fine-grained tokens** → Generate new token

- **Token name**: `dispatch-to-IDS-DRR-QA-Automation`
- **Resource owner**: `CivicDataLab`
- **Repository access**: Only select repositories → `IDS-DRR-QA-Automation`
- **Permissions** (Repository):
  - `Contents`: Read-only
  - `Actions`: Read and write
- **Expiration**: 90 days (rotate per org policy)

Copy the token value once — you'll paste it in step 2.

### 2. Add the PAT as a secret in the upstream repo

In `CivicDataLab/IDS-DRR-Frontend` (and again in `IDS-DRR-Backend`):

Settings → Secrets and variables → Actions → **New repository secret**

- **Name**: `QA_REPO_PAT`
- **Secret**: paste the PAT value from step 1

### 3. Add the dispatch step to the upstream repo's deploy workflow

In each upstream repo's deployment workflow file (typically `.github/workflows/deploy.yml` or similar), append this step **after** the deploy step succeeds:

```yaml
- name: Trigger QA tests
  if: success()
  uses: peter-evans/repository-dispatch@v3
  with:
    token: ${{ secrets.QA_REPO_PAT }}
    repository: CivicDataLab/IDS-DRR-QA-Automation
    event-type: ${{ github.repository == 'CivicDataLab/IDS-DRR-Frontend' && 'frontend-deployed' || 'backend-deployed' }}
    client-payload: |
      {
        "environment": "${{ github.ref_name == 'main' && 'prod' || 'dev' }}",
        "commit": "${{ github.sha }}",
        "actor": "${{ github.actor }}",
        "source_repo": "${{ github.repository }}"
      }
```

**Notes:**
- `event-type` is `frontend-deployed` or `backend-deployed` — both are accepted by the QA repo. Distinct event types make logs easier to read; routing is by `environment`, not event type.
- `environment` is derived from the branch: `main` → `prod`, anything else (`dev`, feature branches) → `dev`. Adjust the conditional if your upstream repo uses different branch names.
- `if: success()` ensures the dispatch only fires after a successful deploy. If you want to fire on partial success, drop this guard.

## Verifying the wiring

After steps 1–3, push a no-op commit to the `dev` branch of the upstream repo. You should see:

1. The upstream repo's deploy workflow runs and shows a "Trigger QA tests" step.
2. In the QA repo's Actions tab, a new run of **Dispatch Tests** appears within ~30 seconds, triggered by `frontend-deployed` (or `backend-deployed`).
3. Inside that run, the `Log dispatch` job prints the source repo, environment, and commit.
4. The `on-dev-deploy` job runs and executes multistate tests.

Repeat against `main` to verify the `on-main-deploy` path.

## Troubleshooting

- **No QA run appears**: check the upstream repo's Actions log for the dispatch step. A 401/403 means the PAT is missing, expired, or scoped wrong.
- **PAT lacks permissions**: re-create with `Contents: Read` and `Actions: Read and write` for the QA repo.
- **Wrong environment routing**: inspect the `Log dispatch` job output in the QA run. The `client_payload.environment` value drives routing; if it's wrong, fix the conditional in the upstream workflow.
- **Multistate runs on a main deploy** (or vice versa): check the marker selection in `dispatch.yml`. Multistate must NOT fire on `prod`/`staging`/`main` payloads.

## Rotation

PATs expire. When `QA_REPO_PAT` expires:
1. Create a new fine-grained PAT (step 1 above).
2. Update the `QA_REPO_PAT` secret in both upstream repos (step 2).
3. No workflow file changes are needed.

Set a calendar reminder ~7 days before expiration so dispatches don't silently break.
