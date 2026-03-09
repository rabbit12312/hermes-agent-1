"""
OLYMPUS — Second Brain as a Multi-Agent System

Built on hermes-agent by Nous Research.

The gods of Olympus are specialists. Together they form a living organism —
not just a tool that responds, but a mind that thinks, notices, and acts.

    HERMES    — Orchestrator: the messenger who coordinates all gods
    PERSEUS   — Capture: the hero who hunts and structures raw information
    MNEMOSYNE — Search: the goddess who remembers everything by meaning
    ASCLEPIUS — Insights: the healer who diagnoses hidden patterns
    ARGUS     — Monitor: the giant with 100 eyes who never sleeps
    HERACLES  — Digest: the hero who synthesizes a week into one scroll

Usage:
    from olympus import orchestrate
    response = orchestrate("Meeting with Anton tomorrow at 9am")
"""

__version__ = "1.0.0"
__author__ = "OLYMPUS — built on hermes-agent"

from olympus.agents.hermes_orchestrator import HERMES_SYSTEM_PROMPT, route_to_gods
from olympus.display import OlympusDisplay

__all__ = [
    "HERMES_SYSTEM_PROMPT",
    "route_to_gods",
    "OlympusDisplay",
]
