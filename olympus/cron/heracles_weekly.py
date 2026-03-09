"""
Heracles Weekly — Cron Job (every Sunday at 19:00)

Wakes HERACLES every Sunday evening to synthesize the entire week —
events, victories, open threads, patterns — and deliver a beautiful digest to Telegram.

Registration:
    hermes cron add --schedule "0 19 * * 0" --skill olympus-heracles-digest \
        --goal "$(python -c 'from olympus.agents.heracles_digest import build_delegate_goal; print(build_delegate_goal())')"

Or run via setup_crons.py which handles registration automatically.
"""

from olympus.agents.heracles_digest import build_delegate_goal

# The goal string passed to hermes-agent when this cron fires
CRON_GOAL = build_delegate_goal()

CRON_SCHEDULE = "0 19 * * 0"   # 19:00 every Sunday (0 = Sunday in cron)
CRON_SKILL    = "olympus-heracles-digest"
CRON_NAME     = "heracles-weekly"
CRON_DESC     = "HERACLES: Sunday 19:00 — weekly digest synthesis → Telegram"

CRON_DEFINITION = {
    "name":     CRON_NAME,
    "schedule": CRON_SCHEDULE,
    "skill":    CRON_SKILL,
    "goal":     CRON_GOAL,
    "description": CRON_DESC,
}
