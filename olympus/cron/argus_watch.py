"""
Argus Watch — Cron Job (every 30 minutes)

Wakes ARGUS to check the Watch List and fire Telegram alerts on triggered conditions.

Registration:
    hermes cron add --schedule "*/30 * * * *" --skill olympus-argus-monitor \
        --goal "$(python -c 'from olympus.agents.argus_monitor import build_delegate_goal; print(build_delegate_goal())')"

Or run via setup_crons.py which handles registration automatically.
"""

from olympus.agents.argus_monitor import build_delegate_goal

# The goal string passed to hermes-agent when this cron fires
CRON_GOAL = build_delegate_goal(mode="run_checks")

CRON_SCHEDULE = "*/30 * * * *"   # every 30 minutes
CRON_SKILL    = "olympus-argus-monitor"
CRON_NAME     = "argus-watch"
CRON_DESC     = "ARGUS: 30-minute watch cycle — check conditions, fire Telegram alerts"

CRON_DEFINITION = {
    "name":     CRON_NAME,
    "schedule": CRON_SCHEDULE,
    "skill":    CRON_SKILL,
    "goal":     CRON_GOAL,
    "description": CRON_DESC,
}
