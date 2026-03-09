# OLYMPUS Skills Guide

OLYMPUS is built on the `hermes-agent` skill system. Each god's intelligence is defined in a `SKILL.md` file, which includes their identity, tools, and operation protocols.

## Using Skills

All OLYMPUS skills are located in `skills/olympus/`.

### ⚡ hermes-orchestrator
The primary skill used by the `run_olympus.py` entry point. It contains the logic for coordinating all other gods.

### ⚔️ perseus-capture
Used to hunt and structure information. It relies heavily on the `memory` tool to store data into `MEMORY.md` and `USER.md`.

### 🌊 mnemosyne-search
Used for retrieval. It utilizes `session_search` and `read_file` to provide a 3-layer recall experience.

### 🌿 asclepius-insights
Used for pattern detection. It analyzes session history and memory to generate reports.

### 👁️ argus-monitor
Used for chronjob-based alerts. It manages `~/.hermes/olympus/argus_watchlist.json`.

### 💪 heracles-digest
Used for the Sunday evening review. It synthesizes a week's worth of data into a Telegram digest.

---

## Extending OLYMPUS

To add a new god or a new capability:

1.  **Create a new skill folder** in `skills/olympus/new-god/`.
2.  **Define the `SKILL.md`**: Include the god's persona, specific tool usage rules, and desired output format.
3.  **Update HERMES**: Modify `olympus/agents/hermes_orchestrator.py` to include the new god in the routing logic and system prompt.
4.  **Add the Agent file**: Create `olympus/agents/new_god.py` to handle prompt building and specific logic.

## Tool Requirements

OLYMPUS gods are designed to work together through `delegate_task`. Ensure that:
- You have a **Telegram bot** configured in `.env` for ARGUS, ASCLEPIUS, and HERACLES.
- You have **semantic search** enabled in `hermes-agent` for MNEMOSYNE.
