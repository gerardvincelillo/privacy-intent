"""Automation helpers for PrivacyIntent CLI workflows."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

SCAN_PROFILES: dict[str, dict[str, int]] = {
    "quick": {"timeout": 20, "max_requests": 120, "depth": 0},
    "standard": {"timeout": 30, "max_requests": 200, "depth": 0},
    "deep": {"timeout": 45, "max_requests": 450, "depth": 2},
}


def normalize_target_url(url: str) -> str:
    """Normalize target URL by ensuring a scheme exists."""
    candidate = url.strip()
    if not candidate:
        raise ValueError("Target URL cannot be empty.")
    parsed = urlparse(candidate)
    if parsed.scheme:
        if not parsed.netloc:
            raise ValueError("Target URL must include a host.")
        return candidate
    normalized = f"https://{candidate}"
    normalized_parsed = urlparse(normalized)
    if not normalized_parsed.netloc:
        raise ValueError("Target URL must include a host.")
    return normalized


def resolve_scan_options(
    profile: str,
    timeout: int | None,
    max_requests: int | None,
    depth: int | None,
) -> tuple[int, int, int]:
    """Resolve effective scan options using profile defaults and explicit overrides."""
    normalized_profile = profile.strip().lower()
    if normalized_profile not in SCAN_PROFILES:
        supported = ", ".join(sorted(SCAN_PROFILES))
        raise ValueError(f"Unknown profile '{profile}'. Supported values: {supported}.")
    selected = SCAN_PROFILES[normalized_profile]
    final_timeout = int(timeout) if timeout is not None else selected["timeout"]
    final_max_requests = int(max_requests) if max_requests is not None else selected["max_requests"]
    final_depth = int(depth) if depth is not None else selected["depth"]
    return final_timeout, final_max_requests, final_depth


def build_auto_report_paths(url: str, artifacts_dir: Path, include_md: bool = True) -> tuple[Path, Path | None]:
    """Generate timestamped report file paths for JSON and optional Markdown outputs."""
    parsed = urlparse(normalize_target_url(url))
    target = (parsed.netloc or "target").replace(":", "_")
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    base_name = f"{target}_{timestamp}"
    json_path = artifacts_dir / f"{base_name}.json"
    md_path = artifacts_dir / f"{base_name}.md" if include_md else None
    return json_path, md_path
