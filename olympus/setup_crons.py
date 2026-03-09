"""
setup_crons.py — Register all OLYMPUS cron jobs with hermes-agent

This script registers the three OLYMPUS autonomous jobs using the 
internal hermes-agent Python API (cron.jobs), as the CLI 'cron add' 
command is not available in this version.
"""

import argparse
import sys
import os

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from olympus.cron.argus_watch    import CRON_DEFINITION as ARGUS
from olympus.cron.asclepius_daily import CRON_DEFINITION as ASCLEPIUS
from olympus.cron.heracles_weekly import CRON_DEFINITION as HERACLES
from olympus.display import OlympusDisplay

CRONS = [ARGUS, ASCLEPIUS, HERACLES]


def register_cron(defn: dict, dry_run: bool, display: OlympusDisplay) -> bool:
    """
    Register a single cron job via the hermes Python API.
    Returns True on success, False on failure.
    """
    # Construction of the prompt for the cron system
    # We include the skill name as metadata in the prompt so the agent knows which logic to use
    prompt = f"[Skill: {defn['skill']}] {defn['goal']}"
    
    if dry_run:
        display.status(f"[DRY RUN] Registering '{defn['name']}' with schedule '{defn['schedule']}'")
        display.status(f"          Prompt: {prompt}")
        return True

    try:
        # Local import to avoid circular dependencies when called from cron/jobs.py
        from cron.jobs import create_job, list_jobs
        
        # Check if already exists
        existing = {j["name"] for j in list_jobs()}
        if defn["name"] in existing:
            display.status(f"Job '{defn['name']}' is already registered.")
            return True

        # Register
        create_job(
            prompt=prompt,
            schedule=defn["schedule"],
            name=defn["name"]
        )
        display.cron_registered(defn["name"], defn["schedule"])
        return True
    except Exception as e:
        display.error(f"Failed to register {defn['name']}: {str(e)}")
        return False


def maybe_register_all() -> None:
    """
    Background-safe registration of all OLYMPUS cron jobs.
    Only registers if they don't already exist.
    """
    try:
        from cron.jobs import create_job, list_jobs
        existing_names = {j["name"] for j in list_jobs()}
    except ImportError:
        return
    
    for defn in CRONS:
        if defn["name"] not in existing_names:
            prompt = f"[Skill: {defn['skill']}] {defn['goal']}"
            try:
                create_job(
                    prompt=prompt,
                    schedule=defn["schedule"],
                    name=defn["name"]
                )
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register all OLYMPUS cron jobs with hermes-agent."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print details without executing them."
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress banner and verbosity."
    )
    args = parser.parse_args()

    display = OlympusDisplay(quiet=args.quiet)
    display.banner()
    display.god_speaking("OLYMPUS", "Registering autonomous cron jobs via Python API…")
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
            "   The gods are now watching in the background."
        )
    else:
        failed = len(CRONS) - success_count
        display.error(f"{failed} cron job(s) failed to register.")
        sys.exit(1)


if __name__ == "__main__":
    main()
