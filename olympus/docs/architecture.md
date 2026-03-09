# OLYMPUS — Architecture

## System Overview

OLYMPUS is a directed multi-agent graph where every edge represents a delegation:

```
                    ┌─────────────────────────────────────┐
                    │            USER INPUT                │
                    └─────────────┬───────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────┐
                    │          HERMES ⚡                   │
                    │  Orchestrator — routes & synthesizes │
                    │  Skill: olympus-hermes-orchestrator  │
                    └──┬──────┬──────┬──────┬─────────────┘
                       │      │      │      │
              delegate │      │      │      │ schedule
              ─────────┘      │      │      └──────────
              │               │      │                 │
    ┌─────────▼───┐  ┌────────▼──┐  ┌▼─────────────┐  │
    │  PERSEUS ⚔️ │  │MNEMOSYNE 🌊│  │ASCLEPIUS 🌿  │  │
    │  Capture    │  │  3-Layer   │  │  Patterns &  │  │
    │  & Tag      │  │  Search    │  │  Diagnostics │  │
    └─────┬───────┘  └─────┬──────┘  └──────────────┘  │
          │                │                             │
          ▼                ▼                           cron
       memory           sessions                    ┌──┴────────────┐
       tool +           session_search              │               │
       USER.md          + read_file             ARGUS 👁️        HERACLES 💪
                                                Every 30min    Sunday 19:00
                                                Watchlist      Weekly digest
                                                → Telegram     → Telegram
```

## Data Flows

### Capture Flow (Perseus)
```
User message → HERMES detects new info → delegate_task(PERSEUS)
  → Perseus reads existing memory (dedup check)
  → stores via memory(target=memory) or memory(target=user)
  → runs session_search to check pattern frequency
  → if 3+ occurrences: writes ~/.hermes/olympus/patterns/[topic].md
  → returns ⚔️ PERSEUS capture report to HERMES
```

### Search Flow (Mnemosyne)
```
User asks a question → HERMES detects retrieval intent → delegate_task(MNEMOSYNE)
  → Layer 1: scan MEMORY.md / USER.md already in context
  → Layer 2: session_search(2–3 parallel queries with synonyms)
  → Layer 3: list_directory + read_file from ~/.hermes/olympus/
  → aggregate and enrich: direct answer + related discoveries + pattern note
  → returns 🌊 MNEMOSYNE report to HERMES
```

### Monitor Flow (Argus)
```
[Cron trigger every 30 min]
  → read_file(~/.hermes/olympus/argus_watchlist.json)
  → for each pending/active watch: check condition against current time
  → if triggered:
      → search memory context with context_query
      → compose alert (time_before / deadline / recurring / custom template)
      → send_message(target=telegram)
      → update watch status (fired / active), save watchlist
```

### Pattern Flow (Asclepius)
```
[Daily cron 09:00] OR [HERMES routes on-demand]
  → session_search (energy, procrastination, people, ideas — 3–4 parallel queries)
  → read_file(~/.hermes/olympus/patterns/)
  → score each finding: frequency × recency × actionability
  → select top 2–3
  → format as Telegram morning diagnostics OR on-demand report
  → if daily: send_message(target=telegram)
```

### Digest Flow (Heracles)
```
[Weekly cron Sunday 19:00]
  → session_search (4 parallel: events, done, struggles, wins)
  → read_file(~/.hermes/olympus/patterns/weekly_insights.md)
  → if < 3 sessions → send quiet-week message, exit
  → organize into 6 sections (Victories, Events, Progress, Open, Wisdom, Numbers)
  → write digest (≤ 4000 chars)
  → send_message(target=telegram)
```

## Storage Locations

| Store | Path | What lives there |
|-------|------|-----------------|
| Agent memory | `MEMORY.md` (managed by hermes-agent) | Events, tasks, ideas, decisions |
| User profile | `USER.md` (managed by hermes-agent) | People, preferences |
| Pattern files | `~/.hermes/olympus/patterns/[topic].md` | Multi-occurrence topic summaries |
| Note files | `~/.hermes/olympus/notes/[topic].md` | Overflow notes beyond memory |
| Watch list | `~/.hermes/olympus/argus_watchlist.json` | Active ARGUS monitoring conditions |
| Session DB | hermes-agent SQLite (`~/.hermes/sessions.db`) | Full session history (session_search) |

## Skill ↔ Agent Mapping

| Skill | Agent Python file | Used by |
|-------|------------------|---------|
| `olympus-hermes-orchestrator` | `agents/hermes_orchestrator.py` | Main entry (run_olympus.py) |
| `olympus-perseus-capture` | `agents/perseus_capture.py` | HERMES delegate_task |
| `olympus-mnemosyne-search` | `agents/mnemosyne_search.py` | HERMES delegate_task |
| `olympus-asclepius-insights` | `agents/asclepius_insights.py` | HERMES delegate_task + cron |
| `olympus-argus-monitor` | `agents/argus_monitor.py` | Cron (every 30 min) |
| `olympus-heracles-digest` | `agents/heracles_digest.py` | Cron (Sunday 19:00) |

## Cron Schedule Summary

| Job | Schedule | Cron expression |
|-----|---------|----------------|
| ARGUS watch cycle | Every 30 minutes | `*/30 * * * *` |
| ASCLEPIUS morning | Daily 09:00 | `0 9 * * *` |
| HERACLES digest | Sunday 19:00 | `0 19 * * 0` |
