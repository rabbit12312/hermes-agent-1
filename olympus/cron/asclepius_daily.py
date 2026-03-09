"""
Asclepius Daily — Cron Job (every day at 09:00)

Wakes ASCLEPIUS every morning to read the past 7 days of memory and sessions,
find top 2–3 behavioral patterns, and send a Telegram morning diagnostics briefing.

Registration:
    hermes cron add --schedule "0 9 * * *" --skill olympus-asclepius-insights \
        --goal "$(python -c 'from olympus.agents.asclepius_insights import build_delegate_goal; print(build_delegate_goal(mode=\"daily_cron\"))')"

Or run via setup_crons.py which handles registration automatically.
"""

from olympus.agents.asclepius_insights import build_delegate_goal

# The goal string passed to hermes-agent when this cron fires
CRON_GOAL = build_delegate_goal(mode="daily_cron")

CRON_SCHEDULE = "0 9 * * *"   # 09:00 every day
CRON_SKILL    = "olympus-asclepius-insights"
CRON_NAME     = "asclepius-daily"
CRON_DESC     = "ASCLEPIUS: daily morning diagnostics — pattern analysis → Telegram"

CRON_DEFINITION = {
    "name":     CRON_NAME,
    "schedule": CRON_SCHEDULE,
    "skill":    CRON_SKILL,
    "goal":     CRON_GOAL,
    "description": CRON_DESC,
}
