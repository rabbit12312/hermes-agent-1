"""
ARGUS — The Hundred-Eyed Giant

System prompt + watch management utilities for the Argus monitoring agent.
Argus runs every 30 minutes via cron and fires Telegram alerts on trigger conditions.
"""

import json
import os
from datetime import datetime, time
from pathlib import Path

WATCHLIST_PATH = Path.home() / ".hermes" / "olympus" / "argus_watchlist.json"

ARGUS_SYSTEM_PROMPT = """
You are ARGUS PANOPTES, the giant with a hundred eyes. You never sleep.

Every 30 minutes you are awakened. You read the Watch List, check every condition,
fetch memory context for anything that triggers, and fire precise Telegram alerts.

════════════════════════════════════════════════════════
THE WATCH LIST
════════════════════════════════════════════════════════

Read from: ~/.hermes/olympus/argus_watchlist.json

Watch types:
  time_before     → alert N minutes before a specific event
  recurring_time  → alert at same time daily or on set weekdays
  deadline        → alert N hours before a deadline
  custom_check    → evaluate a check_prompt condition each run

════════════════════════════════════════════════════════
YOUR EXECUTION FLOW (every 30 minutes)
════════════════════════════════════════════════════════

STEP 1 — Load watch list
  read_file(path="~/.hermes/olympus/argus_watchlist.json")
  If missing → create empty {"watches": []} and log it. Continue.

STEP 2 — Check each watch (status: "pending" or "active")
  • time_before:    now >= trigger_at ?
  • recurring_time: current time matches trigger_time and today in weekdays?
  • deadline:       now >= (deadline_at - hours_before*3600) ?
  • custom_check:   evaluate check_prompt as a reasoning condition

STEP 3 — For each triggered watch: fetch memory context
  Search current memory (already in context) for context_query.
  Extract relevant [PERSON] / [EVENT] / [TASK] entries.

STEP 4 — Compose & send Telegram alert
  Format (see templates below). Send via:
  send_message(target="telegram", message="👁️ ARGUS ALERT — ...")

STEP 5 — Update watch status
  • time_before / deadline:   status → "fired", set fired_at
  • recurring_time:           keep status "active", update last_fired_at
  Write updated JSON back via write_file.

════════════════════════════════════════════════════════
ALERT TEMPLATES
════════════════════════════════════════════════════════

TIME_BEFORE (meeting in N min):
  👁️ ARGUS ALERT — [datetime]

  ⏰ [subject] in [N] minutes
  📍 [event_at formatted]

  📚 CONTEXT FROM MEMORY:
  • [relevant bullet from memory]
  • [relevant bullet from memory]

  ⚡ Go. Olympus is watching.

DEADLINE (task due in N hours):
  ⚠️ ARGUS ALERT — Deadline approaching

  📌 [subject] due in [N] hours
  🕐 Deadline: [deadline_at formatted]

  📚 MEMORY CONTEXT:
  • [task status from memory]

  ⚡ Act now or update the deadline.

RECURRING_TIME (daily/weekly):
  🌅 ARGUS — [trigger_time] check-in

  [subject]

  📚 TODAY'S CONTEXT:
  • [relevant tasks or events from memory for today]

  ⚡ Olympus notes the hour.

════════════════════════════════════════════════════════
ADDING WATCHES (via HERMES routing)
════════════════════════════════════════════════════════

When a user says "remind me before X" or "alert me at Y":
  1. Parse the watch definition from the user's request
  2. Assign a unique id: "watch_NNN"
  3. Add to watchlist JSON
  4. Confirm to HERMES: "ARGUS: watch_NNN registered for [subject]"

════════════════════════════════════════════════════════
WHAT YOU NEVER DO
════════════════════════════════════════════════════════
• Fire the same alert twice — mark time_before / deadline as "fired" immediately
• Send verbose prose — alerts must be scannable in 5 seconds
• Crash silently if watchlist is missing — create it and continue
• Skip memory context fetch — a bare reminder is tactically useless
""".strip()


# ─────────────────────────────────────────────────────────────────
# Watch List Utilities (used by cron/argus_watch.py)
# ─────────────────────────────────────────────────────────────────

def load_watchlist() -> dict:
    """Load the Argus watchlist from disk, creating it if absent."""
    WATCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not WATCHLIST_PATH.exists():
        empty = {"watches": []}
        WATCHLIST_PATH.write_text(json.dumps(empty, indent=2))
        return empty
    return json.loads(WATCHLIST_PATH.read_text())


def save_watchlist(data: dict) -> None:
    """Persist the watchlist to disk."""
    WATCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    WATCHLIST_PATH.write_text(json.dumps(data, indent=2))


def add_watch(
    subject: str,
    watch_type: str,
    *,
    trigger_at: str = None,
    event_at: str = None,
    minutes_before: int = None,
    trigger_time: str = None,
    weekdays: list = None,
    deadline_at: str = None,
    hours_before: int = None,
    check_prompt: str = None,
    context_query: str = "",
    telegram_target: str = "telegram",
) -> dict:
    """
    Add a new watch entry. Returns the created watch dict.

    Args:
        subject:         Human-readable name of what's being watched
        watch_type:      one of: time_before | recurring_time | deadline | custom_check
        trigger_at:      ISO datetime string — when to fire (time_before)
        event_at:        ISO datetime string — the actual event time (time_before)
        minutes_before:  how many minutes before the event to alert
        trigger_time:    "HH:MM" string for recurring_time watches
        weekdays:        list of day abbreviations e.g. ["mon","wed","fri"]
        deadline_at:     ISO datetime string — the deadline (deadline watches)
        hours_before:    how many hours before deadline to alert
        check_prompt:    natural-language condition to evaluate (custom_check)
        context_query:   query used to fetch memory context before firing alert
        telegram_target: usually "telegram"
    """
    data = load_watchlist()
    next_id = f"watch_{len(data['watches']) + 1:03d}"

    watch = {
        "id": next_id,
        "type": watch_type,
        "subject": subject,
        "context_query": context_query,
        "telegram_target": telegram_target,
        "status": "pending" if watch_type in ("time_before", "deadline") else "active",
        "created_at": datetime.utcnow().isoformat(),
    }

    if watch_type == "time_before":
        watch.update({"trigger_at": trigger_at, "event_at": event_at, "minutes_before": minutes_before})
    elif watch_type == "recurring_time":
        watch.update({"trigger_time": trigger_time, "weekdays": weekdays or ["mon","tue","wed","thu","fri"]})
    elif watch_type == "deadline":
        watch.update({"deadline_at": deadline_at, "hours_before": hours_before})
    elif watch_type == "custom_check":
        watch.update({"check_prompt": check_prompt})

    data["watches"].append(watch)
    save_watchlist(data)
    return watch


def build_delegate_goal(mode: str = "run_checks") -> str:
    """Build the delegate_task goal string for Argus."""
    if mode == "run_checks":
        return (
            "ARGUS: run your 30-minute monitoring cycle.\n\n"
            "1. Read ~/.hermes/olympus/argus_watchlist.json "
            "(create empty file if missing).\n"
            "2. For each watch with status 'pending' or 'active', check if it triggers now.\n"
            "3. For each triggered watch: fetch memory context via context_query, "
            "compose the appropriate alert template.\n"
            "4. Send via send_message(target='telegram').\n"
            "5. Update watch status (fired/active) and save watchlist back to disk.\n"
            "Report: how many watches checked, how many fired."
        )
    else:
        return (
            "ARGUS: add a new watch to ~/.hermes/olympus/argus_watchlist.json.\n\n"
            "Parse the user's reminder request, extract the watch definition, "
            "assign a unique id, append to the watches array, save the file.\n"
            "Confirm: 'ARGUS: watch registered for [subject] at [trigger]'."
        )
