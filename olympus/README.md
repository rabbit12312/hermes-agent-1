# OLYMPUS — Second Brain as a Multi-Agent System

> *"The gods of Olympus are specialists. Together they form a living organism —  
> not just a tool that responds, but a mind that thinks, notices, and acts."*

Built on **[hermes-agent](https://github.com/NousResearch/hermes-agent)** by Nous Research.

---

## What is OLYMPUS?

OLYMPUS is a **multi-agent Second Brain** — a system of six specialized AI gods that work together to capture your world, remember it, find patterns in it, and proactively surface what matters.

You speak. HERMES routes. The gods act.

---

## The Pantheon

| God | Role | Trigger |
|-----|------|---------|
| **HERMES ⚡** | Orchestrator — routes every message to the correct specialists | Every message |
| **PERSEUS ⚔️** | Captures & structures raw information into tagged memory | New info detected |
| **MNEMOSYNE 🌊** | Searches memory, sessions, and notes by meaning | Retrieval request |
| **ASCLEPIUS 🌿** | Detects behavioral patterns and sends proactive insights | On-demand + daily 09:00 |
| **ARGUS 👁️** | Monitors conditions and fires Telegram alerts | Every 30 min (cron) |
| **HERACLES 💪** | Synthesizes the entire week into a digest | Every Sunday 19:00 (cron) |

---

## Architecture

```
User message
     │
     ▼
  HERMES ⚡  (olympus-hermes-orchestrator skill)
     │
     ├──► PERSEUS ⚔️   delegate_task → captures info → memory tool
     │
     ├──► MNEMOSYNE 🌊  delegate_task → session_search + read_file → 3-layer recall
     │
     └──► ASCLEPIUS 🌿  delegate_task → pattern analysis → insight report

Autonomous (cron):
  ARGUS 👁️    → every 30 min   → reads watchlist → Telegram alerts
  ASCLEPIUS 🌿 → daily 09:00   → morning diagnostics → Telegram
  HERACLES 💪  → Sunday 19:00  → weekly digest → Telegram
```

---

## Quick Start

### 1. Install dependencies

```bash
cd hermes-agent
pip install -e .
```

### 2. Configure

Copy `.env.example` to `.env` and set your API keys and Telegram credentials.

### 3. Register cron jobs

```bash
python olympus/setup_crons.py
# or dry-run to preview commands:
python olympus/setup_crons.py --dry-run
```

### 4. Run OLYMPUS

```bash
# Interactive mode
python olympus/run_olympus.py

# One-shot message
python olympus/run_olympus.py --message "Meeting with Sara tomorrow at 14:00"
```

### 5. Run demo scenarios

```bash
python olympus/demo.py --scenario 1   # Chain reaction
python olympus/demo.py --scenario 2   # Smart search
python olympus/demo.py --scenario 3   # Live insight
python olympus/demo.py --all          # All three
```

---

## How It Works

### Capturing Information

Say anything new — a meeting, an idea, a person's preference:

```
You: "I met Masha today. She runs a startup called UserBrain — AI analytics for hr teams."

HERMES routes to → PERSEUS

⚔️ PERSEUS — Captured
TYPE: [PERSON]
STORED: "Masha — founder of UserBrain, AI analytics for HR"
TARGET: user
PATTERN CHECK: Masha mentioned 1x — no pattern yet
```

### Searching Memory

Ask about anything from your past:

```
You: "What was that startup idea about jobs?"

HERMES routes to → MNEMOSYNE

🌊 MNEMOSYNE — Memory Retrieved
DIRECT ANSWER: Feb 12, 2026 — AI job aggregator with candidate scoring (6 sessions)
RELATED DISCOVERIES: linked to funding frustration theme, rising excitement
PATTERN NOTE: ASCLEPIUS flagged as high-recurrence signal
```

### Setting Reminders

```
You: "Remind me 5 minutes before my meeting with Masha tomorrow at 3pm"

HERMES routes to → ARGUS (watch registered) + PERSEUS (event captured)

👁️ ARGUS ALERT — 2026-03-10 14:55
⏰ Meeting with Masha in 5 minutes
📚 CONTEXT: UserBrain founder. Agenda: product demo.
⚡ Go. Olympus is watching.
```

### Daily Intelligence (automatic)

Every morning at 09:00 via Telegram:

```
🌿 ASCLEPIUS — Morning Diagnostics
March 10, 2026

PATTERN 1: Wednesday Fatigue Cycle
You mention low energy every Wednesday for 3 weeks. 
Heaviest meeting day correlates.
→ Consider blocking 14:00–16:00 as rest.

PATTERN 2: OLYMPUS README stalled
Appears in 3 sessions, zero [DONE] markers.
→ Schedule a 30-min focused block.
```

---

## Memory Format

Perseus tags all entries consistently:

| Tag | Meaning | Example |
|-----|---------|---------|
| `[PERSON]` | Contact profile | `[PERSON] Masha — founder UserBrain, prefers async` |
| `[EVENT\|date]` | Meeting or event | `[EVENT\|2026-03-10T14:00] Demo with Masha` |
| `[TASK\|priority]` | Task with deadline | `[TASK\|deadline:2026-03-15\|priority:high] Submit README` |
| `[IDEA\|date]` | Captured idea | `[IDEA\|2026-03-09] AI job aggregator — 6th mention` |
| `[PREF]` | User preference | `[PREF] Prefers voice notes for quick thoughts` |
| `[DECISION]` | Made decision | `[DECISION\|2026-03-09] Python over TypeScript for OLYMPUS` |

---

## Project Structure

```
olympus/
├── __init__.py              # Package header + exports
├── display.py               # Rich terminal UI (god-themed)
├── run_olympus.py           # Main entry point
├── setup_crons.py           # Cron job registration script
├── demo.py                  # Hackathon demo (3 scenarios)
├── agents/
│   ├── hermes_orchestrator.py   # HERMES: routing logic + system prompt
│   ├── perseus_capture.py       # PERSEUS: capture agent
│   ├── mnemosyne_search.py      # MNEMOSYNE: 3-layer search agent
│   ├── asclepius_insights.py    # ASCLEPIUS: pattern healer
│   ├── argus_monitor.py         # ARGUS: watchlist + cron monitor
│   └── heracles_digest.py       # HERACLES: weekly digest
├── cron/
│   ├── argus_watch.py           # Every 30 minutes
│   ├── asclepius_daily.py       # Daily 09:00 AM
│   └── heracles_weekly.py       # Sunday 19:00
└── docs/
    ├── architecture.md           # Detailed architecture
    ├── gods.md                   # Each god's role & API
    └── skills_guide.md           # How to use & extend skills

skills/olympus/
├── hermes-orchestrator/SKILL.md
├── perseus-capture/SKILL.md
├── mnemosyne-search/SKILL.md
├── asclepius-insights/SKILL.md
├── argus-monitor/SKILL.md
└── heracles-digest/SKILL.md
```

---

## Philosophy

OLYMPUS is built on one principle: **a Second Brain should be alive**.

Most note-taking tools are passive — they wait for you to query them. OLYMPUS is different:

- **ARGUS never sleeps** — it checks your watches every 30 minutes
- **ASCLEPIUS acts without being asked** — it reads your history daily and sends what it finds
- **HERACLES shows up every Sunday** — not because you asked, but because you need it

The gods don't just store — they *understand*. MNEMOSYNE searches by meaning, not keywords. PERSEUS doesn't just save — it tags, structures, detects duplicates, and flags patterns. ASCLEPIUS doesn't just summarize — it *diagnoses*.

This is a Second Brain that thinks back.

---

## License

MIT — Built on hermes-agent by Nous Research.
