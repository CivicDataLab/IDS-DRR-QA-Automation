# GitHub Actions Workflows

This repo runs Selenium + pytest end-to-end tests against the IDS-DRR platform. CI is split into one **reusable workflow** and four **caller workflows**, plus a **composite action** for environment setup. Different triggers run different test selections — there is no single workflow that "does everything."

## Files

```
.github/
├── actions/
│   └── setup-test-env/
│       └── action.yml        # composite: checkout, Python, deps, driver cache, mkdir reports/
└── workflows/
    ├── _test.yml             # reusable workflow (workflow_call)
    ├── pr.yml                # PR → smoke
    ├── main.yml              # push to main → full suite
    ├── nightly.yml           # cron + manual → multistate
    └── dispatch.yml          # manual + cross-repo dispatch
```

## Trigger map

| Trigger | Workflow | Markers | Shards × workers | Target env |
|---|---|---|---|---|
| **Pull request** | `pr.yml` | `smoke` | 1 × 4 | dev |
| **Push to main** | `main.yml` | (all) | 3 × 2 | staging |
| **Schedule 02:00 UTC** + manual | `nightly.yml` | `multistate` (`tests/test_analytics.py`) | 4 × 2 | dev |
| **Upstream dev deploy** (`repository_dispatch` w/ `environment: dev`) | `dispatch.yml` → `on-dev-deploy` | `multistate` | 4 × 2 | dev |
| **Upstream main deploy** (`environment: prod`/`staging`/`main`) | `dispatch.yml` → `on-main-deploy` | `smoke or (analytics and not multistate) or component or dataset` | 3 × 2 | prod |
| **Manual** (`workflow_dispatch`) | `dispatch.yml` | user-chosen | per scope | user-chosen |

**Why these splits:** the multistate feature is currently dev-only (flagged off on main), so it runs on dev deploys + nightly heartbeat. Main deploys exercise smoke + single-state Assam analytics + components + datasets. The QA repo's own PR/main pushes validate the test framework itself.

## Reusable workflow inputs (`_test.yml`)

| Input | Type | Default | Notes |
|---|---|---|---|
| `markers` | string | `""` | Pytest `-m` expression. Empty = run everything. Compound expressions OK (e.g. `"smoke or component"`). |
| `shards` | number | `1` | Matrix size. `1` disables `pytest-split`. |
| `workers` | number | `2` | `pytest-xdist` workers per shard. |
| `target_env` | string | `dev` | Picks URL: `prod` → `URL`, `staging` → `STAGING_URL`/fallback, `dev` → `DEV_URL`/fallback. |
| `test_path` | string | `tests/` | Path passed to pytest (e.g. `tests/test_analytics.py`). |
| `bootstrap_states` | bool | `false` | If true, runs `scripts/discover_state_indicators.py` when `config/states/states_master.yaml` is missing. |

The `_test.yml` workflow runs two jobs:
1. **`test`** — matrix-sharded pytest. Each shard emits `reports/junit_shard_<N>.xml` and a per-shard HTML.
2. **`summary`** — downloads all shard artifacts, runs `scripts/merge_test_reports.py` (consolidates JUnit XMLs into a single `reports/report.html`), publishes JUnit results, posts a PR comment.

## Cross-repository integration

The QA repo accepts `repository_dispatch` events from the upstream `IDS-DRR-Frontend` and `IDS-DRR-Backend` repos. See [`docs/upstream-dispatch-setup.md`](../../docs/upstream-dispatch-setup.md) for the wiring (PAT, secret, deploy-workflow snippet).

`dispatch.yml` accepts these dispatch types:
- `frontend-deployed` — fired by IDS-DRR-Frontend after a successful deploy
- `backend-deployed` — fired by IDS-DRR-Backend after a successful deploy

Routing is by `client_payload.environment`, not by event type. Either source can trigger either branch.

Expected payload:
```json
{
  "environment": "dev",          // or "prod" / "staging" / "main"
  "commit": "<sha>",
  "actor": "<github-user>",
  "source_repo": "CivicDataLab/IDS-DRR-Frontend"
}
```

## Manual runs

GitHub → Actions tab → **Dispatch Tests** → Run workflow:

- **scope**: `smoke`, `multistate`, `main-deploy`, or `full`
- **target_env**: `dev`, `staging`, or `prod`

For multistate or full ad-hoc runs against dev, `dispatch.yml` is the right entry point. The reusable `_test.yml` is not directly triggerable.

## Artifacts

| Artifact | Retention | Source |
|---|---|---|
| `test-reports-shard-<N>` | 30 days | per-shard HTML, JUnit XML, log, self-healing dir |
| `screenshots-shard-<N>` | 14 days | failure screenshots |
| `consolidated-test-report` | 30 days | merged `reports/report.html` |

## GitHub runner sizing

`ubuntu-latest` is 2 vCPU / 7 GB. Recommended: `workers ≤ 2` per shard (oversubscription hurts Selenium tests). Scale via `shards`, not `workers`.

## Tuning

- **Add a new test marker**: register it in `pytest.ini`'s `markers` list, then reference it via `markers:` input in any caller.
- **Change the nightly time**: edit the cron in `nightly.yml`.
- **Add a new test selection**: add a new `manual-*` job in `dispatch.yml` keyed off a new `scope` choice.

## Local equivalents

- PR smoke ≈ `pytest tests/ -n 4 -m smoke`
- Main full ≈ `./run_parallel_tests.sh -n 2`
- Nightly multistate ≈ `pytest tests/test_analytics.py -n 2 -m multistate`
- Main-deploy selection ≈ `pytest tests/ -n 2 -m "smoke or (analytics and not multistate) or component or dataset"`
