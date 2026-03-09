"""
run_olympus.py — Main entry point for OLYMPUS

Wraps hermes-agent's HermesCLI with the HERMES persona and OLYMPUS display theme.

Usage:
    python olympus/run_olympus.py
    python olympus/run_olympus.py --quiet
    python olympus/run_olympus.py --message "I met Anton today, VC fund"
"""

import argparse
import sys
import os

# ── Ensure project root is on path ────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from olympus.display import OlympusDisplay
from olympus.agents.hermes_orchestrator import HERMES_SYSTEM_PROMPT, route_to_gods


def build_cli_args(message: str = None, quiet: bool = False) -> list:
    """
    Build the argument list for hermes-agent CLI.

    hermes-agent is launched as a subprocess (or imported if available)
    with the HERMES system prompt set as the ephemeral prompt.
    """
    args = [
        "--skill", "olympus-hermes-orchestrator",
        "--ephemeral-system-prompt", HERMES_SYSTEM_PROMPT,
    ]
    if message:
        args += ["--message", message]
    if quiet:
        args += ["--quiet"]
    return args


def run_interactive(display: OlympusDisplay) -> None:
    """Run OLYMPUS in interactive REPL mode using hermes-agent."""
    display.banner()
    display.god_speaking("HERMES", "Olympus is online. Speak, mortal.")
    display.divider()

    try:
        # Import and run hermes interactively
        from cli import main as hermes_main
        sys.argv = ["hermes"] + build_cli_args()
        hermes_main()
    except ImportError:
        display.error(
            "Could not import hermes CLI. "
            "Make sure you are running from the hermes-agent project root "
            "and the environment is activated.\n"
            "  cd /path/to/hermes-agent && python olympus/run_olympus.py"
        )
        sys.exit(1)


def run_one_shot(message: str, display: OlympusDisplay) -> None:
    """Send a single message to OLYMPUS and print the response."""
    plan = route_to_gods(message)
    display.routing(plan)

    try:
        from cli import main as hermes_main
        sys.argv = ["hermes"] + build_cli_args(message=message, quiet=True)
        hermes_main()
    except ImportError:
        display.error(
            "Could not import hermes CLI. "
            "Run from the hermes-agent project root."
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="olympus",
        description="OLYMPUS — Second Brain as a Multi-Agent System on hermes-agent.",
    )
    parser.add_argument(
        "--message", "-m", type=str, default=None,
        help="Send a single message and exit (non-interactive mode).",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress OLYMPUS banners and status lines.",
    )
    parser.add_argument(
        "--setup-crons", action="store_true",
        help="Register all cron jobs and exit (same as running setup_crons.py).",
    )
    args = parser.parse_args()

    display = OlympusDisplay(quiet=args.quiet)

    if args.setup_crons:
        from olympus.setup_crons import main as setup_main
        setup_main()
        return

    if args.message:
        run_one_shot(args.message, display)
    else:
        run_interactive(display)


if __name__ == "__main__":
    main()
