# GitHub Actions Workflows

## test-automation.yml

Automated test execution with maximum parallel performance.

### Triggers

- **Push**: `main`, `develop`, `master` branches
- **Pull Request**: All PRs
- **Deployment**: All deployment events
- **Manual**: Actions tab → Run workflow

### Parallel Execution

**Two-level parallelization:**

1. **Matrix Strategy**: 3 shards (separate runners)
2. **pytest-xdist**: 3 workers per shard

**Total**: 3 shards × 3 workers = **9 parallel executions**

### Performance

| Tests | Serial | Parallel | Speedup |
|-------|--------|----------|---------|
| 30    | 15 min | ~3-4 min | 4-5x    |
| 60    | 30 min | ~6-8 min | 4-5x    |

### Jobs

**test** - Main test suite with sharding
- Runs 3 parallel shards
- 3 workers per shard
- Auto-retries failures (2x)
- Generates HTML/XML reports

**test-summary** - Combines results
- Aggregates shard results
- Publishes unified test results
- Comments on PRs

**smoke-test** - Quick validation
- Runs smoke tests only
- 4 parallel workers
- Fast feedback on push/PR

### Manual Run Options

Actions tab → QA Test Automation → Run workflow:

- **workers**: 1-4 (default: 3)
- **test_marker**: smoke, analytics, dataset, etc.

### Artifacts

- **Test reports**: HTML + XML (30 days)
- **Screenshots**: On failure (14 days)
- **Self-healing logs**: (30 days)

### Configuration

To adjust parallelization:

**More tests (100+)**: Increase shards
```yaml
matrix:
  shard: [1, 2, 3, 4, 5]
```

**Heavy tests**: Reduce workers
```yaml
env:
  PARALLEL_WORKERS: 2
```

**Fewer tests (<20)**: Reduce shards
```yaml
matrix:
  shard: [1, 2]
```

### GitHub Runner Specs

Standard `ubuntu-latest`:
- CPU: 2 cores
- RAM: 7 GB
- Recommended: 2-4 workers max
