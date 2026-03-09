"""
demo.py — OLYMPUS Hackathon Demo Script

Three showcase scenarios that demonstrate the full power of OLYMPUS.
Run each scenario to record a compelling demo video.

Usage:
    python olympus/demo.py --scenario 1   # Chain reaction: capture → search → alert
    python olympus/demo.py --scenario 2   # Smart search: 3-layer memory retrieval
    python olympus/demo.py --scenario 3   # Live insight: Asclepius pattern detection
    python olympus/demo.py --all          # Run all three in sequence
"""

import argparse
import time
import sys
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from olympus.display import OlympusDisplay
from olympus.agents.hermes_orchestrator import route_to_gods

display = OlympusDisplay()

# ─────────────────────────────────────────────────────────────────
# SCENARIO 1 — Chain Reaction
# Shows: Perseus (capture) + Mnemosyne (context) + Argus (reminder) in one message
# ─────────────────────────────────────────────────────────────────

SCENARIO_1_MESSAGE = (
    "I have a meeting with Anton Volkov tomorrow at 9am to demo OLYMPUS. "
    "He's a VC, prefers direct pitches, no fluff. "
    "Remind me 5 minutes before."
)

def scenario_1() -> None:
    display.banner()
    display.god_speaking("OLYMPUS", "SCENARIO 1 — Chain Reaction Demo")
    display.divider()
    display.status("User says:")
    print(f'\n   "{SCENARIO_1_MESSAGE}"\n')
    time.sleep(1)

    plan = route_to_gods(SCENARIO_1_MESSAGE)
    display.routing(plan)
    time.sleep(0.5)

    display.god_speaking("PERSEUS",   "Capturing: [EVENT] Meeting with Anton, 2026-03-10 09:00")
    time.sleep(0.4)
    display.god_speaking("PERSEUS",   "Capturing: [PERSON] Anton Volkov — VC, prefers direct pitches")
    time.sleep(0.4)
    display.god_speaking("MNEMOSYNE", "Searching memory for 'Anton'…")
    time.sleep(0.5)
    display.god_speaking("MNEMOSYNE", "Found: Anton mentioned 3x — last meeting Feb 28 (positive)")
    time.sleep(0.4)
    display.god_speaking("ARGUS",     "Watch registered — alert at 08:55 tomorrow")
    time.sleep(0.3)

    display.divider()
    print("""
⚡ HERMES — Routing complete

⚔️  PERSEUS captured: Meeting with Anton, 2026-03-10 09:00 [memory ✓]
               Anton Volkov profile stored [user ✓]
🌊  MNEMOSYNE found: Anton — 3 past sessions, last contact Feb 28
👁️  ARGUS watching: alert set for 08:55 tomorrow

Anton meeting is locked in. I'll wake you at 08:55 with full context.
    """)


# ─────────────────────────────────────────────────────────────────
# SCENARIO 2 — Smart Search
# Shows: Mnemosyne's 3-layer memory retrieval
# ─────────────────────────────────────────────────────────────────

SCENARIO_2_MESSAGE = "What was that startup idea I kept mentioning?"

def scenario_2() -> None:
    display.banner()
    display.god_speaking("OLYMPUS", "SCENARIO 2 — Smart Search Demo")
    display.divider()
    display.status("User asks:")
    print(f'\n   "{SCENARIO_2_MESSAGE}"\n')
    time.sleep(1)

    display.god_speaking("HERMES",    "Routing to MNEMOSYNE…")
    time.sleep(0.5)
    display.god_speaking("MNEMOSYNE", "Layer 1: Scanning memory context… [IDEA] AI job aggregator found")
    time.sleep(0.6)
    display.god_speaking("MNEMOSYNE", "Layer 2: session_search('startup OR idea OR business')… 6 sessions hit")
    time.sleep(0.7)
    display.god_speaking("MNEMOSYNE", "Layer 3: reading ~/.hermes/olympus/patterns/startup_idea.md…")
    time.sleep(0.6)
    display.god_speaking("ASCLEPIUS", "Pattern file confirms: this idea is high-recurrence signal")
    time.sleep(0.4)

    display.divider()
    print("""
🌊 MNEMOSYNE — Memory Retrieved

DIRECT ANSWER:
  Feb 12, 2026 — "AI job aggregator with candidate scoring."
  Scrape LinkedIn/HH.ru, score candidates with LLM, sell to HR teams as SaaS.

RELATED DISCOVERIES:
  • Mentioned 6× across 5 sessions (Feb–Mar)
  • Emotional arc: excited → anxious about execution → re-energized (Mar 9)
  • Linked to funding frustration theme (3 sessions)

PATTERN NOTE:
  ⚡ ASCLEPIUS flagged this as "persistent signal — worth dedicated exploration."

SOURCES:
  — Sessions Feb 12 | Feb 18 | Mar 03 | Mar 09
  — MEMORY.md [IDEA] | pattern: startup_idea.md
    """)


# ─────────────────────────────────────────────────────────────────
# SCENARIO 3 — Live Insight
# Shows: Asclepius detecting a behavioral pattern
# ─────────────────────────────────────────────────────────────────

SCENARIO_3_MESSAGE = "What patterns do you see in the last few weeks?"

def scenario_3() -> None:
    display.banner()
    display.god_speaking("OLYMPUS", "SCENARIO 3 — Live Insight Demo")
    display.divider()
    display.status("User asks:")
    print(f'\n   "{SCENARIO_3_MESSAGE}"\n')
    time.sleep(1)

    display.god_speaking("HERMES",    "Routing to ASCLEPIUS…")
    time.sleep(0.5)
    display.god_speaking("ASCLEPIUS", "Scanning energy patterns…")
    time.sleep(0.6)
    display.god_speaking("ASCLEPIUS", "Found: 'tired' / 'exhausted' — 4× on Wednesdays in 3 weeks")
    time.sleep(0.5)
    display.god_speaking("ASCLEPIUS", "Scanning procrastination signatures…")
    time.sleep(0.6)
    display.god_speaking("ASCLEPIUS", "Found: OLYMPUS README — in 3 sessions, 0 [DONE] tags")
    time.sleep(0.5)
    display.god_speaking("ASCLEPIUS", "Scanning idea momentum…")
    time.sleep(0.5)
    display.god_speaking("ASCLEPIUS", "AI job aggregator — 6 occurrences, rising sentiment")
    time.sleep(0.4)

    display.divider()
    print("""
🌿 ASCLEPIUS — Pattern Report

QUERY: patterns in last few weeks
SESSIONS ANALYZED: 14 (past 30 days)

PATTERN 1: Wednesday Fatigue Cycle
  I notice low-energy markers (tired/exhausted) on 3 consecutive Wednesdays.
  Wednesday is your highest-meeting day (avg 4 sessions).
  → Consider moving one Wednesday meeting to Tuesday, or blocking 14:00-16:00 as rest.

PATTERN 2: Stalled task — OLYMPUS README
  This task appears in 3 separate sessions with no [DONE] marker.
  It's not blocking a release — it has low urgency but high visibility.
  → Schedule a focused 30-min block. Perseus will help structure it.

PATTERN 3: Startup idea is not casual
  The AI job aggregator appears 6× over 3 weeks with rising excitement.
  This is a persistent signal, not a passing thought.
  → Dedicate one session to writing a concrete concept doc.

Stay sharp, mortal. Olympus watches. 🏛️
    """)


# ─────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────

SCENARIOS = {
    1: scenario_1,
    2: scenario_2,
    3: scenario_3,
}

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="olympus-demo",
        description="OLYMPUS hackathon demo — three showcase scenarios.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--scenario", "-s", type=int, choices=[1, 2, 3],
        help="Run a specific scenario (1, 2, or 3).",
    )
    group.add_argument(
        "--all", "-a", action="store_true",
        help="Run all three scenarios in sequence.",
    )
    args = parser.parse_args()

    if args.all:
        for i in [1, 2, 3]:
            SCENARIOS[i]()
            if i < 3:
                print("\n" + "═" * 60 + "\n")
                time.sleep(2)
    else:
        SCENARIOS[args.scenario]()


if __name__ == "__main__":
    main()
