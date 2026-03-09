"""
setup_crons.py — Register all OLYMPUS cron jobs with hermes-agent

Run once after installing OLYMPUS:
    python olympus/setup_crons.py

This script reads the three cron job definitions and registers them
using the hermes CLI (or prints the commands if --dry-run is passed).
"""

import argparse
import subprocess
import sys

from olympus.cron.argus_watch    import CRON_DEFINITION as ARGUS
from olympus.cron.asclepius_daily import CRON_DEFINITION as ASCLEPIUS
from olympus.cron.heracles_weekly import CRON_DEFINITION as HERACLES
from olympus.display import OlympusDisplay

CRONS = [ARGUS, ASCLEPIUS, HERACLES]


def register_cron(defn: dict, dry_run: bool, display: OlympusDisplay) -> bool:
    """
    Register a single cron job via the hermes CLI.
    Returns True on success, False on failure.
    """
    cmd = [
        "hermes", "cron", "add",
        "--name",     defn["name"],
        "--schedule", defn["schedule"],
        "--skill",    defn["skill"],
        "--goal",     defn["goal"],
    ]

    if dry_run:
        display.status(f"[DRY RUN] {' '.join(cmd)}")
        return True

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            display.cron_registered(defn["name"], defn["schedule"])
            return True
        else:
            display.error(
                f"Failed to register {defn['name']}: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
            return False
    except FileNotFoundError:
        display.error(
            "hermes CLI not found. "
            "Please ensure hermes-agent is installed and 'hermes' is in your PATH."
        )
        return False
    except subprocess.TimeoutExpired:
        display.error(f"Timeout registering cron: {defn['name']}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register all OLYMPUS cron jobs with hermes-agent."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print commands without executing them."
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress banner and verbosity."
    )
    args = parser.parse_args()

    display = OlympusDisplay(quiet=args.quiet)
    display.banner()
    display.god_speaking("OLYMPUS", "Setting up autonomous cron jobs…")
    display.divider()

    success_count = 0
    for defn in CRONS:
        ok = register_cron(defn, dry_run=args.dry_run, display=display)
        if ok:
            success_count += 1

    display.divider()
    if success_count == len(CRONS):
        display.success(
            f"All {len(CRONS)} cron jobs registered successfully.\n"
            "   ARGUS watches every 30 minutes.\n"
            "   ASCLEPIUS wakes at 09:00 daily.\n"
            "   HERACLES rises every Sunday at 19:00."
        )
    else:
        failed = len(CRONS) - success_count
        display.error(f"{failed} cron job(s) failed to register. Check output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
