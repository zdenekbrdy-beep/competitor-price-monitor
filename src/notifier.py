"""Slack alert sender.

Uses a single Incoming Webhook URL. Configured via the SLACK_WEBHOOK_URL
environment variable so it is safe to commit the rest of the repo without
leaking secrets. In GitHub Actions, set it as a repository secret.
"""

from __future__ import annotations

import os

import httpx
from rich.console import Console

console = Console()


def send_alerts(alerts: list[dict]) -> bool:
    """Post a single combined message to Slack. Returns True on success."""
    if not alerts:
        return True
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        console.log("[yellow]SLACK_WEBHOOK_URL not set, skipping Slack alert.[/yellow]")
        return False

    lines = [":rotating_light: *Competitor price drops*"]
    for alert in alerts:
        lines.append(
            f"• <{alert['url']}|{alert['name']}>  "
            f"·  {alert['old_price']:,.2f} -> *{alert['new_price']:,.2f}*  "
            f"·  -{alert['drop_pct']}%  "
            f"·  _{alert['target']}_"
        )
    payload = {"text": "\n".join(lines)}
    try:
        response = httpx.post(webhook, json=payload, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPError as e:
        console.log(f"[red]Slack post failed: {e}[/red]")
        return False
    console.log(f"[green]Posted {len(alerts)} alert(s) to Slack.[/green]")
    return True
