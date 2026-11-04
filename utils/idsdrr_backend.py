"""
Plain-HTTP helpers for the IDS-DRR Data Management backend (not DataSpace).

The same env var / default is used by the other in-flight backend probes
(IDS_DRR_BACKEND_GRAPHQL_URL), so a single override points every test at the
same deployment. Read-only: GraphQL queries and GET requests only.
"""

import os

import pytest
import requests

from config.config import Config

GRAPHQL_URL = os.getenv(
    "IDS_DRR_BACKEND_GRAPHQL_URL", "https://hp.drr.backend.open-contracting.in/graphql"
)
# REST routes (raster/...) live on the same host as /graphql.
BACKEND_URL = GRAPHQL_URL.rsplit("/graphql", 1)[0]

_HEADERS = {"User-Agent": "IDS-DRR-QA-Automation/read-only-probe"}


def get(path, **params):
    """GET a backend route; fail the test readably if the host is unreachable."""
    url = f"{BACKEND_URL}{path}"
    try:
        return requests.get(url, params=params, timeout=Config.HTTP_TIMEOUT, headers=_HEADERS)
    except requests.RequestException as exc:
        pytest.fail(f"IDS-DRR backend unreachable: {url} - {type(exc).__name__}: {exc}")


def states_modules():
    """{state slug: [module slugs]} from the backend's getStates (authoritative for the frontend)."""
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": "{ getStates { slug modules } }"},
            timeout=Config.HTTP_TIMEOUT,
            headers=_HEADERS,
        )
        states = response.json()["data"]["getStates"]
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        pytest.fail(f"getStates failed against {GRAPHQL_URL}: {type(exc).__name__}: {exc}")
    return {s["slug"]: list(s.get("modules") or []) for s in states}
