"""
OLYMPUS Display — Terminal UI Theme

Rich-powered god-themed spinners, headers, colors, and status styles.
Used by run_olympus.py to give the terminal the feel of Olympus.
"""

import sys
from typing import Optional

# ─────────────────────────────────────────────────────────────────
# Try to import rich; fall back to plain-text if not installed
# ─────────────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.style import Style
    from rich.spinner import Spinner
    from rich.live import Live
    from rich import box
    _RICH = True
except ImportError:
    _RICH = False


class OlympusDisplay:
    """
    Terminal display handler for OLYMPUS.

    Usage:
        display = OlympusDisplay()
        display.banner()
        display.god_speaking("HERMES", "Routing your message…")
        display.status("Waiting for Perseus…")
    """

    # ── God color palette ──────────────────────────────────────────
    GOD_COLORS = {
        "HERMES":    "bold gold1",
        "PERSEUS":   "bold cyan",
        "MNEMOSYNE": "bold blue",
        "ASCLEPIUS": "bold green",
        "ARGUS":     "bold red",
        "HERACLES":  "bold magenta",
        "OLYMPUS":   "bold white",
    }

    GOD_EMOJI = {
        "HERMES":    "⚡",
        "PERSEUS":   "⚔️",
        "MNEMOSYNE": "🌊",
        "ASCLEPIUS": "🌿",
        "ARGUS":     "👁️",
        "HERACLES":  "💪",
    }

    BANNER = r"""
  ___  _    _   _ __  __ ____  _   _ ____
 / _ \| |  | | | |  \/  |  _ \| | | / ___|
| | | | |  | |_| | |\/| | |_) | | | \___ \
| |_| | |__|  _  | |  | |  __/| |_| |___) |
 \___/|____|_| |_|_|  |_|_|    \___/|____/

        Second Brain — Multi-Agent System
        Built on hermes-agent  ·  v1.0.0
"""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        if _RICH:
            self.console = Console(stderr=False)
        else:
            self.console = None

    # ── Public API ─────────────────────────────────────────────────

    def banner(self) -> None:
        """Print the OLYMPUS ASCII banner on startup."""
        if self.quiet:
            return
        if _RICH:
            self.console.print(
                Panel(
                    Text(self.BANNER, style="bold gold1", justify="center"),
                    border_style="dim white",
                    box=box.DOUBLE,
                )
            )
        else:
            print(self.BANNER)

    def god_speaking(self, god: str, message: str) -> None:
        """Print a god's status line with emoji and color."""
        if self.quiet:
            return
        emoji = self.GOD_EMOJI.get(god.upper(), "•")
        color = self.GOD_COLORS.get(god.upper(), "white")
        line  = f"{emoji}  {god.upper()} — {message}"
        if _RICH:
            self.console.print(line, style=color)
        else:
            print(line)

    def status(self, message: str) -> None:
        """Print a neutral status line."""
        if self.quiet:
            return
        if _RICH:
            self.console.print(f"   {message}", style="dim white")
        else:
            print(f"   {message}")

    def routing(self, plan: dict) -> None:
        """Print the routing plan summary from route_to_gods()."""
        if self.quiet:
            return
        rationale = plan.get("rationale", "")
        if _RICH:
            self.console.print(f"\n⚡ {rationale}\n", style="bold gold1")
        else:
            print(f"\n⚡ {rationale}\n")

    def divider(self) -> None:
        """Print a thin divider line."""
        if self.quiet:
            return
        if _RICH:
            self.console.rule(style="dim white")
        else:
            print("─" * 60)

    def error(self, message: str) -> None:
        """Print an error message."""
        if _RICH:
            self.console.print(f"✗  {message}", style="bold red")
        else:
            print(f"ERROR: {message}", file=sys.stderr)

    def success(self, message: str) -> None:
        """Print a success message."""
        if self.quiet:
            return
        if _RICH:
            self.console.print(f"✓  {message}", style="bold green")
        else:
            print(f"OK: {message}")

    def cron_registered(self, name: str, schedule: str) -> None:
        """Confirm a cron job was registered."""
        if self.quiet:
            return
        msg = f"Cron registered: {name}  [{schedule}]"
        if _RICH:
            self.console.print(f"🕐  {msg}", style="bold cyan")
        else:
            print(f"CRON: {msg}")
