"""
Security Tests — `requests`-based checks, no browser needed.

Run:
    pytest tests/test_security.py -v
"""

import re

import pytest
import requests

from config.config import Config

REQUIRED_HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
)

XSS_PAYLOAD = "<script>alert('xss')</script>"
# Query params most likely to be reflected server-side if any are (search-style params).
CANDIDATE_REFLECTED_PARAMS = ("q", "search", "query", "search_query")

# Sensitive-file paths that must not be served with actual content. Note: this
# app's catch-all router 200s almost any unknown path (soft-404 — confirmed
# live 2026-09-09, /debug and /admin both redirect to /en/<path> and render
# 200, same as a nonsense path does), so status code alone can't tell a real
# exposure from routine soft-404 behavior. Checking response content instead.
SENSITIVE_PATHS = ("/.env", "/.git/config", "/wp-config.php", "/config.json")
SECRET_MARKERS = ("SECRET_KEY", "DATABASE_URL", "AWS_SECRET", "-----BEGIN", "password=")


@pytest.mark.security
class TestSecurityHeaders:
    """Standard defensive HTTP headers on the main page response."""

    @pytest.mark.xfail(
        reason="Live 2026-09-09: none of Strict-Transport-Security, Content-Security-Policy, "
        "X-Frame-Options, X-Content-Type-Options, or Referrer-Policy are present — tracked in issue"
    )
    def test_security_headers_present(self):
        """Main page response carries the standard defensive headers"""
        response = requests.get(Config.BASE_URL, timeout=15)
        missing = [h for h in REQUIRED_HEADERS if h not in response.headers]
        assert not missing, f"Missing security headers: {missing}"


@pytest.mark.security
class TestInjection:
    """Reflected-content probes."""

    def test_query_params_not_reflected_unescaped(self):
        """A script-tag payload in common search-style query params isn't echoed back raw"""
        base = f"{Config.BASE_URL.rstrip('/')}/datasets"
        reflected = []
        for param in CANDIDATE_REFLECTED_PARAMS:
            response = requests.get(base, params={param: XSS_PAYLOAD}, timeout=15)
            if XSS_PAYLOAD in response.text:
                reflected.append(param)
        assert not reflected, f"XSS payload reflected unescaped via param(s): {reflected}"


@pytest.mark.security
class TestExposedPaths:
    """Sensitive files must not be served with real content."""

    def test_sensitive_paths_do_not_leak_content(self):
        """.env / .git / config-style paths never return actual secret content"""
        base = Config.BASE_URL.rstrip("/")
        leaking = []
        for path in SENSITIVE_PATHS:
            response = requests.get(f"{base}{path}", timeout=15)
            if any(marker in response.text for marker in SECRET_MARKERS):
                leaking.append(path)
        assert not leaking, f"Sensitive content served at: {leaking}"


@pytest.mark.security
class TestGraphQLIntrospection:
    """Informational only — introspection being on is expected for dev."""

    def test_data_layer_introspection_status(self):
        """Log whether the data-layer GraphQL endpoint has introspection enabled

        Not asserted: introspection-on is normal for a dev environment. A
        prod-scoped equivalent of this check (where it should be off) is a
        separate, deliberately out-of-scope test — see the plan.
        """
        response = requests.post(
            "https://hp.drr.backend.open-contracting.in/graphql",
            json={"query": "{__schema{types{name}}}"},
            timeout=15,
        )
        enabled = response.status_code == 200 and "__schema" in response.text
        print(f"ℹ️  Data-layer GraphQL introspection enabled: {enabled} (expected on dev)")
