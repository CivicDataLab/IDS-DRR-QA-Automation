#!/usr/bin/env bash
#
# File / update / close the DataSpace availability incident sub-issue.
#
# One sub-issue per incident, never one per failed run: while an incident is open
# the script comments on the existing child (at most hourly) instead of filing a
# new one. Children hang off the umbrella card so the board shows one row, not a
# growing pile.
#
# Usage: availability_alert.sh <pass|fail>
set -euo pipefail

RESULT="${1:?usage: availability_alert.sh <pass|fail>}"
REPO="${GITHUB_REPOSITORY:?}"
PARENT="${PARENT_ISSUE:?}"
LOG="${PROBE_LOG:-probe.log}"
RUN_URL="${GITHUB_SERVER_URL}/${REPO}/actions/runs/${GITHUB_RUN_ID}"
COMMENT_COOLDOWN_MIN="${COMMENT_COOLDOWN_MIN:-60}"

# The umbrella card carries the same label, so exclude it explicitly.
child=$(gh issue list --repo "$REPO" --label availability-incident --state open \
  --json number --jq "[.[] | select(.number != ${PARENT}) | .number] | first // empty")

log_excerpt() {
  if [[ -f "$LOG" ]]; then
    # Failures only — the full pytest run is mostly passing noise.
    grep -E "^(FAILED|E |AssertionError|assert )" "$LOG" | head -25 \
      || tail -25 "$LOG"
  else
    echo "(probe log missing)"
  fi
}

link_as_sub_issue() {
  local number="$1" child_id parent_id
  child_id=$(gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){id}}}' \
    -f o="${REPO%/*}" -f r="${REPO#*/}" -F n="$number" --jq '.data.repository.issue.id')
  parent_id=$(gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){id}}}' \
    -f o="${REPO%/*}" -f r="${REPO#*/}" -F n="$PARENT" --jq '.data.repository.issue.id')
  # An issue has exactly one parent; a repeat call fails, which is harmless here.
  gh api graphql -H "GraphQL-Features: sub_issues" \
    -f query='mutation($p:ID!,$c:ID!){addSubIssue(input:{issueId:$p,subIssueId:$c}){issue{number}}}' \
    -f p="$parent_id" -f c="$child_id" >/dev/null \
    && echo "linked #${number} under #${PARENT}" \
    || echo "WARNING: could not link #${number} under #${PARENT}" >&2
}

if [[ "$RESULT" == "fail" ]]; then
  if [[ -n "$child" ]]; then
    last=$(gh issue view "$child" --repo "$REPO" --json comments --jq '.comments[-1].createdAt // ""')
    age_min=99999
    if [[ -n "$last" ]]; then
      age_min=$(( ( $(date -u +%s) - $(date -u -d "$last" +%s) ) / 60 ))
    fi
    if (( age_min >= COMMENT_COOLDOWN_MIN )); then
      gh issue comment "$child" --repo "$REPO" --body "$(cat <<EOF
Still failing as of $(date -u '+%Y-%m-%d %H:%M UTC').

\`\`\`
$(log_excerpt)
\`\`\`

[Run]($RUN_URL)
EOF
)"
      echo "commented on open incident #${child} (last comment ${age_min}m ago)"
    else
      echo "incident #${child} already open, last comment ${age_min}m ago — staying quiet"
    fi
  else
    body=$(cat <<EOF
A scheduled availability probe failed. Filed automatically by \`.github/workflows/availability.yml\`.

**Detected:** $(date -u '+%Y-%m-%d %H:%M UTC')
**Run:** $RUN_URL

\`\`\`
$(log_excerpt)
\`\`\`

## What this means

One or more of the DataSpace hosts IDS-DRR reads from is not answering. IDS-DRR itself will keep rendering — the frontend does not fail loudly when its data source is gone — so this will not be visible in the UI suite.

Browser CORS errors are a common downstream symptom: an nginx 502 page carries no \`Access-Control-Allow-Origin\`, so a failed call surfaces in the console as a CORS rejection rather than as the outage it is. Check the host before chasing CORS config.

## First things to check

Both past outages were on \`prod-drr-cds\` (13.201.23.28), which serves the prod web UI and API from two separate processes:

\`\`\`bash
ssh prod-drr-cds
docker ps -a | grep DataSpace                       # API container
export NVM_DIR=\$HOME/.nvm && . "\$NVM_DIR/nvm.sh"
pm2 list                                            # frontend process
\`\`\`

Prior write-up, including the reboot-survival fixes: CivicDataLab/DataSpaceBackend#148

---
This issue closes itself when the probes pass again. Parent: #${PARENT}
EOF
)
    number=$(gh issue create --repo "$REPO" \
      --title "DataSpace unavailable — $(date -u '+%Y-%m-%d %H:%M UTC')" \
      --label availability-incident --body "$body" | grep -oE '[0-9]+$')
    echo "filed incident #${number}"
    link_as_sub_issue "$number"
  fi
else
  if [[ -n "$child" ]]; then
    gh issue comment "$child" --repo "$REPO" --body "Recovered — all DataSpace probes passing as of $(date -u '+%Y-%m-%d %H:%M UTC'). Closing.

[Run]($RUN_URL)"
    gh issue close "$child" --repo "$REPO" --reason completed
    echo "closed incident #${child}"
  else
    echo "all probes passing, no open incident"
  fi
fi
