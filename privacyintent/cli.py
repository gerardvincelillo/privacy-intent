
"""CLI entrypoint for PrivacyIntent."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from privacyintent.scanner import scan_site

app = typer.Typer(help="PrivacyIntent CLI for website privacy auditing.")


@app.callback()
def main() -> None:
    """Root command group for PrivacyIntent."""


@app.command("scan")
def scan(
    url: str,
    json: Optional[Path] = typer.Option(
        None,
        "--json",
        help="Write a JSON report to the given path.",
    ),
    md: Optional[Path] = typer.Option(
        None,
        "--md",
        help="Write a Markdown report to the given path.",
    ),
    timeout: int = typer.Option(30, "--timeout", min=1, help="Request timeout in seconds."),
    max_requests: int = typer.Option(
        200,
        "--max-requests",
        min=1,
        help="Maximum number of requests to collect.",
    ),
    headless: bool = typer.Option(True, "--headless/--no-headless", help="Run browser headless."),
    user_agent: Optional[str] = typer.Option(None, "--user-agent", help="Override browser user agent."),
    depth: int = typer.Option(0, "--depth", min=0, help="Basic crawl depth."),
) -> None:
    """Scan a URL for privacy risks."""
    scan_site(
        url=url,
        json_path=json,
        md_path=md,
        timeout=timeout,
        max_requests=max_requests,
        headless=headless,
        user_agent=user_agent,
        depth=depth,
    )


if __name__ == "__main__":
    app()
