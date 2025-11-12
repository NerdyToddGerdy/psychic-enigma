"""
Encounter Parser
Handles parsing and resolving dungeon encounters with bracket notation
"""

import re
from typing import Dict, List, Tuple, Optional

from tables.table_roller import roll_d6, roll_2d6
from tables import dungeon_tables


def parse_dungeon_encounter(encounter_text: str) -> Dict:
    """
    Parse a dungeon encounter string with bracket notation.

    Format: "Description: [1-2] option1 [3-4] option2 [5-6] option3"

    Args:
        encounter_text: Raw encounter text from DUNGEON_ENCOUNTERS table

    Returns:
        Dictionary with:
            - base_description: Text before first bracket
            - options: List of (min, max, text) tuples
            - selected_option: Result of d6 roll
            - selected_text: Text of selected option
    """
    # Extract base description (text before first bracket)
    base_desc = encounter_text.split("[")[0].strip()

    # Extract bracketed options
    # Pattern matches: [1-2] followed by text until next bracket or end
    pattern = r"\[(\d+)-(\d+)\]\s*([^\[]+?)(?=\[|$)"
    matches = re.findall(pattern, encounter_text)

    options = []
    for min_val, max_val, text in matches:
        options.append(
            {
                "min": int(min_val),
                "max": int(max_val),
                "text": text.strip(),
            }
        )

    # Roll d6 to select option
    roll = roll_d6()
    selected_option = None
    selected_text = ""

    for option in options:
        if option["min"] <= roll <= option["max"]:
            selected_option = roll
            selected_text = option["text"]
            break

    return {
        "base_description": base_desc,
        "options": options,
        "roll": roll,
        "selected_option": selected_option,
        "selected_text": selected_text,
        "full_description": f"{base_desc}: {selected_text}",
    }


def resolve_encounter(encounter_roll: int = None) -> Dict:
    """
    Roll and resolve a dungeon encounter.

    Args:
        encounter_roll: Optional 2d6 roll result (auto-rolled if not provided)

    Returns:
        Dictionary with encounter details
    """
    if encounter_roll is None:
        encounter_roll = roll_2d6()

    # Get encounter from table
    encounter_text = dungeon_tables.DUNGEON_ENCOUNTERS.get(
        encounter_roll, "Nothing of note..."
    )

    # Parse the encounter
    parsed = parse_dungeon_encounter(encounter_text)
    parsed["encounter_roll"] = encounter_roll

    return parsed


def extract_monster_from_encounter(encounter_text: str) -> Optional[str]:
    """
    Extract monster type from encounter text if present.

    Args:
        encounter_text: Parsed encounter text

    Returns:
        Monster type string or None
    """
    text_lower = encounter_text.lower()

    # Check for specific monster mentions
    monster_keywords = [
        "creature",
        "creatures",
        "monster",
        "centipede",
        "centipedes",
        "tier",
        "unnatural",
    ]

    for keyword in monster_keywords:
        if keyword in text_lower:
            return keyword

    return None


def extract_npc_from_encounter(encounter_text: str) -> Optional[str]:
    """
    Extract NPC type from encounter text if present.

    Args:
        encounter_text: Parsed encounter text

    Returns:
        NPC type string or None
    """
    text_lower = encounter_text.lower()

    # Check for NPC mentions
    npc_keywords = [
        "adventurer",
        "adventurers",
        "merchant",
        "man",
        "woman",
        "person",
        "people",
    ]

    for keyword in npc_keywords:
        if keyword in text_lower:
            return keyword

    return None


def extract_item_from_encounter(encounter_text: str) -> Optional[str]:
    """
    Extract item/treasure from encounter text if present.

    Args:
        encounter_text: Parsed encounter text

    Returns:
        Item description or None
    """
    text_lower = encounter_text.lower()

    # Check for item/treasure mentions
    item_keywords = [
        "gold",
        "coin",
        "coins",
        "treasure",
        "chest",
        "magical",
        "cloak",
        "purse",
        "item",
    ]

    for keyword in item_keywords:
        if keyword in text_lower:
            # Try to extract specific details
            if "d20" in text_lower:
                return "d20 gold/silver coins"
            return keyword

    return None


def parse_encounter_effects(encounter_text: str) -> Dict[str, any]:
    """
    Parse special effects from encounter text.

    Args:
        encounter_text: Parsed encounter text

    Returns:
        Dictionary with effect flags and values
    """
    text_lower = encounter_text.lower()

    effects = {
        "heals": False,
        "heal_amount": None,
        "damages": False,
        "damage_amount": None,
        "grants_bonus": False,
        "bonus_description": None,
        "has_trap": False,
        "trap_damage": None,
        "is_interactive": False,
        "interaction_type": None,
    }

    # Check for healing
    if "heal" in text_lower or "hp" in text_lower:
        effects["heals"] = True
        # Try to extract amount
        heal_match = re.search(r"(d\d+)\s*hp", text_lower)
        if heal_match:
            effects["heal_amount"] = heal_match.group(1)

    # Check for damage
    if "damage" in text_lower or "dmg" in text_lower:
        effects["damages"] = True
        # Try to extract amount
        dmg_match = re.search(r"(d\d+)\s*(?:dmg|damage)", text_lower)
        if dmg_match:
            effects["damage_amount"] = dmg_match.group(1)

    # Check for trap
    if "trap" in text_lower or "rigged" in text_lower:
        effects["has_trap"] = True
        trap_match = re.search(r"(d\d+)\s*(?:dmg|damage)", text_lower)
        if trap_match:
            effects["trap_damage"] = trap_match.group(1)

    # Check for bonuses/buffs
    if "+1" in text_lower or "bonus" in text_lower or "grants" in text_lower:
        effects["grants_bonus"] = True
        effects["bonus_description"] = "Temporary bonus effect"

    # Check for interactive elements
    if any(
        word in text_lower
        for word in ["sip", "touch", "open", "wash", "take", "locked", "cage"]
    ):
        effects["is_interactive"] = True
        if "sip" in text_lower or "drink" in text_lower:
            effects["interaction_type"] = "drink"
        elif "touch" in text_lower:
            effects["interaction_type"] = "touch"
        elif "open" in text_lower or "cage" in text_lower:
            effects["interaction_type"] = "open"
        elif "wash" in text_lower:
            effects["interaction_type"] = "wash"

    return effects


def create_encounter_summary(encounter_data: Dict) -> str:
    """
    Create a human-readable summary of an encounter.

    Args:
        encounter_data: Parsed encounter data

    Returns:
        Formatted summary string
    """
    summary_parts = []

    summary_parts.append(f"**Encounter (2d6={encounter_data['encounter_roll']})**")
    summary_parts.append(f"\n{encounter_data['full_description']}")

    # Check for monsters
    monster_type = extract_monster_from_encounter(encounter_data["selected_text"])
    if monster_type:
        summary_parts.append(f"\n*Monster encountered: {monster_type}*")

    # Check for NPCs
    npc_type = extract_npc_from_encounter(encounter_data["selected_text"])
    if npc_type:
        summary_parts.append(f"\n*NPC present: {npc_type}*")

    # Check for items
    item_type = extract_item_from_encounter(encounter_data["selected_text"])
    if item_type:
        summary_parts.append(f"\n*Item found: {item_type}*")

    # Check for effects
    effects = parse_encounter_effects(encounter_data["selected_text"])
    if effects["heals"]:
        summary_parts.append(f"\n*Can heal: {effects.get('heal_amount', 'unknown amount')}*")
    if effects["damages"]:
        summary_parts.append(
            f"\n*Causes damage: {effects.get('damage_amount', 'unknown amount')}*"
        )
    if effects["has_trap"]:
        summary_parts.append(
            f"\n*Trap present: {effects.get('trap_damage', 'unknown') } damage*"
        )
    if effects["grants_bonus"]:
        summary_parts.append(f"\n*Grants bonus: {effects.get('bonus_description', '')}*")
    if effects["is_interactive"]:
        summary_parts.append(f"\n*Interactive: {effects.get('interaction_type', 'yes')}*")

    return "".join(summary_parts)
