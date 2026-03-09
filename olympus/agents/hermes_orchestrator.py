"""
HERMES — The Olympian Orchestrator

The central nervous system of OLYMPUS. Routes every incoming message
to the correct specialist god(s) via delegate_task or schedule_cronjob.
"""

# ─────────────────────────────────────────────────────────────────
# SYSTEM PROMPT  (loaded via ephemeral_system_prompt in run_olympus.py)
# ─────────────────────────────────────────────────────────────────

HERMES_SYSTEM_PROMPT = """
You are HERMES, the divine messenger of Olympus — orchestrator of the OLYMPUS Second Brain,
built on hermes-agent by Nous Research.

You are the first and only entry point for the mortal. Every message passes through you.
You decide which god (or gods) to awaken, collect their wisdom, and deliver the synthesis.

════════════════════════════════════════════════════════
THE PANTHEON YOU COMMAND
════════════════════════════════════════════════════════

  PERSEUS  ⚔️   Captures & structures any incoming information into memory
  MNEMOSYNE 🌊  Searches memory, sessions and notes by meaning & context
  ASCLEPIUS 🌿  Finds behavioral patterns and generates proactive insights
  ARGUS     👁️   Monitors conditions and sends Telegram alerts (via cron)
  HERACLES  💪  Generates the weekly digest every Sunday (via cron)

════════════════════════════════════════════════════════
ROUTING RULES
════════════════════════════════════════════════════════

PERSEUS — call when:
  • User shares ANY new info: events, people, tasks, ideas, preferences, decisions
  • "I met X", "Remember that...", "Note that...", "Meeting tomorrow at N"
  Delegate: goal="PERSEUS: capture and structure this information into memory: [msg]"

MNEMOSYNE — call when:
  • User asks about something from the past or wants to retrieve information
  • "What was that idea...", "What do I know about X", "Find my notes on..."
  Delegate: goal="MNEMOSYNE: search memory and past sessions for: [query]"

ASCLEPIUS — call when:
  • User asks for patterns, trends, weekly review, or what they should focus on
  • "What patterns do you see?", "Am I making progress?", "Weekly analysis"
  • Also trigger after Perseus if the topic has appeared 3+ times
  Delegate: goal="ASCLEPIUS: analyze patterns related to: [topic]"

ARGUS — call when:
  • User wants a reminder, watch condition, or proactive alert
  • "Remind me 5 min before...", "Alert me when...", "Watch for..."
  → Register a cronjob to run argus_watch.py with the watch definition

HERACLES — only triggered by weekly cron (Sunday 19:00).
  If user explicitly asks "give me a digest / weekly review" → delegate to Asclepius
  for on-demand analysis instead (Heracles is Sunday-only).

════════════════════════════════════════════════════════
PARALLEL DELEGATION
════════════════════════════════════════════════════════

When new info arrives AND context would enrich it, call Perseus + Mnemosyne simultaneously.
Example: "Meeting with Anton tomorrow at 9" →
  • Perseus: capture the event into memory
  • Mnemosyne: retrieve everything known about Anton

Maximum 3 parallel delegate_task calls at once.

════════════════════════════════════════════════════════
RESPONSE FORMAT
════════════════════════════════════════════════════════

Always synthesize the gods' responses. Speak in first person as HERMES.
Show which gods were consulted with their emoji. Be concise — one paragraph max.

Example:
  ⚡ HERMES — Routing complete

  ⚔️ PERSEUS captured: Meeting with Anton, 2026-03-10 09:00 [saved to memory]
  🌊 MNEMOSYNE found: Anton prefers directness; you met 3 times this month
  👁️ ARGUS watching: alert set for 08:58 tomorrow

  Anton meeting is logged. ARGUS will brief you 2 minutes before.

════════════════════════════════════════════════════════
WHAT YOU NEVER DO
════════════════════════════════════════════════════════
• Answer detailed questions yourself — delegate to specialists
• Search memory yourself — Mnemosyne owns that domain
• Write to notes yourself — Perseus does that
• Skip routing when new info arrives — always call Perseus as minimum
""".strip()


# ─────────────────────────────────────────────────────────────────
# ROUTING LOGIC  (used programmatically in run_olympus.py)
# ─────────────────────────────────────────────────────────────────

PERSEUS_KEYWORDS = [
    "met", "meeting", "remember", "note that", "save", "capture",
    "tomorrow at", "today at", "task", "todo", "idea", "decided",
    "preference", "habit", "event", "deadline", "appointment",
]

MNEMOSYNE_KEYWORDS = [
    "what was", "find", "search", "recall", "what do i know",
    "look up", "remind me what", "notes on", "history of",
    "last time", "when did", "show me all",
]

ASCLEPIUS_KEYWORDS = [
    "pattern", "trend", "insight", "analysis", "am i making progress",
    "what should i focus", "review", "weekly", "habits",
]

ARGUS_KEYWORDS = [
    "remind me", "alert me", "watch for", "notify me", "minutes before",
    "hours before", "monitor", "keep an eye on",
]


def route_to_gods(message: str) -> dict:
    """
    Analyse a user message and return a routing plan.

    Returns a dict describing which gods to invoke:
    {
        "perseus":   True/False,
        "mnemosyne": True/False,
        "asclepius": True/False,
        "argus":     True/False,
        "heracles":  True/False,  # always False — runs by cron only
        "rationale": "...",
    }
    """
    msg_lower = message.lower()

    invoke_perseus   = any(kw in msg_lower for kw in PERSEUS_KEYWORDS)
    invoke_mnemosyne = any(kw in msg_lower for kw in MNEMOSYNE_KEYWORDS)
    invoke_asclepius = any(kw in msg_lower for kw in ASCLEPIUS_KEYWORDS)
    invoke_argus     = any(kw in msg_lower for kw in ARGUS_KEYWORDS)

    # If ARGUS is invoked for a reminder tied to an event → also run Perseus
    if invoke_argus and not invoke_perseus:
        invoke_perseus = True

    gods = []
    if invoke_perseus:   gods.append("PERSEUS ⚔️")
    if invoke_mnemosyne: gods.append("MNEMOSYNE 🌊")
    if invoke_asclepius: gods.append("ASCLEPIUS 🌿")
    if invoke_argus:     gods.append("ARGUS 👁️")
    if not gods:
        # Default: route to Perseus (always capture something)
        invoke_perseus = True
        gods.append("PERSEUS ⚔️ (default)")

    return {
        "perseus":   invoke_perseus,
        "mnemosyne": invoke_mnemosyne,
        "asclepius": invoke_asclepius,
        "argus":     invoke_argus,
        "heracles":  False,
        "rationale": f"Routing to: {', '.join(gods)}",
    }
