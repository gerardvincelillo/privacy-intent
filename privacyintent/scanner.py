
"""Scanning orchestrator."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer


def scan_site(
    url: str,
    json_path: Optional[Path],
    md_path: Optional[Path],
    timeout: int,
    max_requests: int,
    headless: bool,
    user_agent: Optional[str],
    depth: int,
) -> None:
    """Temporary scan handler until full scanner is implemented."""
    _ = (json_path, md_path, timeout, max_requests, headless, user_agent, depth)
    typer.echo(f"PrivacyIntent scan interface is ready. Target: {url}")
