"""
Combat System Module
Handles turn-based combat, encounters, and special effects
"""

from .combat_system import CombatEncounter, CombatAction, CombatResult
from .encounter_parser import parse_dungeon_encounter, resolve_encounter

__all__ = [
    "CombatEncounter",
    "CombatAction",
    "CombatResult",
    "parse_dungeon_encounter",
    "resolve_encounter",
]
