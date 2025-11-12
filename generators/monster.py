"""
Monster System
Handles monster creation, stats, and special abilities
"""

import re
import random
from typing import Dict, List, Optional, Tuple

from tables.table_roller import roll_d6, roll_d20


class Monster:
    """Monster with stats, attacks, and special abilities"""

    def __init__(
        self,
        name: str,
        hd: str,
        ac: int,
        attack: str,
        special: Optional[str] = None,
    ):
        """
        Initialize a monster.

        Args:
            name: Monster name
            hd: Hit dice string (e.g., "2+2", "1-1", "1d2HP")
            ac: Armor class
            attack: Attack description
            special: Special abilities description
        """
        self.name = name
        self.hd_string = hd
        self.ac = ac
        self.attack_description = attack
        self.special_description = special

        # Parse HD and roll HP
        self.hp_max = self._parse_and_roll_hd(hd)
        self.hp_current = self.hp_max

        # Calculate XP value based on HD (roughly maps HD to CR)
        self.xp_value = self._calculate_xp_from_hd(hd)

        # Parse special abilities
        self.special_abilities = self._parse_special_abilities(attack, special)

        # Status
        self.is_alive = True
        self.status_effects: List[Dict] = []

    def _parse_and_roll_hd(self, hd_string: str) -> int:
        """
        Parse HD string and roll for HP.

        Examples:
            "1" -> 1d8
            "2+2" -> 2d8+2
            "1-1" -> 1d8-1 (minimum 1)
            "1d2HP" -> 1d2
            "1/2" -> 1d4
            "6+4" -> 6d8+4

        Args:
            hd_string: Hit dice notation

        Returns:
            Rolled HP value
        """
        hd_string = str(hd_string).strip()

        # Special case: "1d2HP" format
        if "HP" in hd_string.upper():
            match = re.match(r"(\d+)d(\d+)", hd_string, re.IGNORECASE)
            if match:
                num_dice = int(match.group(1))
                die_size = int(match.group(2))
                return max(1, sum(random.randint(1, die_size) for _ in range(num_dice)))

        # Special case: fractional HD like "1/2"
        if "/" in hd_string:
            # 1/2 HD = 1d4 HP
            return max(1, random.randint(1, 4))

        # Parse standard HD format: "2+2", "1-1", "1", "6+4", etc.
        match = re.match(r"(\d+)([+-]\d+)?", hd_string)
        if match:
            num_dice = int(match.group(1))
            modifier = int(match.group(2)) if match.group(2) else 0

            # Roll HP: number of d8s + modifier
            hp = sum(random.randint(1, 8) for _ in range(num_dice)) + modifier
            return max(1, hp)

        # Fallback: treat as single d8
        return random.randint(1, 8)

    def _calculate_xp_from_hd(self, hd_string: str) -> int:
        """
        Calculate D&D 5e XP value based on Hit Dice (roughly mapping HD to CR).

        HD to CR mapping (approximate):
        - 1/2 HD = CR 0 (10 XP)
        - 1 HD = CR 1/4 (50 XP)
        - 2 HD = CR 1/2 (100 XP)
        - 3 HD = CR 1 (200 XP)
        - 4 HD = CR 2 (450 XP)
        - 5 HD = CR 3 (700 XP)
        - 6 HD = CR 4 (1100 XP)
        - 7+ HD = CR 5+ (1800+ XP)

        Args:
            hd_string: Hit dice notation

        Returns:
            XP value for defeating this monster
        """
        hd_string = str(hd_string).strip()

        # Parse the base HD number
        hd_value = 1.0

        # Fractional HD
        if "/" in hd_string:
            hd_value = 0.5
        # Special HP notation
        elif "HP" in hd_string.upper():
            match = re.match(r"(\d+)d(\d+)", hd_string, re.IGNORECASE)
            if match:
                num_dice = int(match.group(1))
                hd_value = max(0.5, num_dice / 2)  # Rough estimate
        # Standard format with modifiers
        else:
            match = re.match(r"(\d+)", hd_string)
            if match:
                hd_value = int(match.group(1))

        # Map HD to XP (D&D 5e XP by CR)
        if hd_value <= 0.5:
            return 10  # CR 0
        elif hd_value <= 1:
            return 50  # CR 1/4
        elif hd_value <= 2:
            return 100  # CR 1/2
        elif hd_value <= 3:
            return 200  # CR 1
        elif hd_value <= 4:
            return 450  # CR 2
        elif hd_value <= 5:
            return 700  # CR 3
        elif hd_value <= 6:
            return 1100  # CR 4
        elif hd_value <= 7:
            return 1800  # CR 5
        elif hd_value <= 8:
            return 2300  # CR 6
        elif hd_value <= 9:
            return 2900  # CR 7
        elif hd_value <= 10:
            return 3900  # CR 8
        else:
            # Higher HD monsters get more XP (scaling up)
            return 3900 + ((hd_value - 10) * 1000)

    def _parse_special_abilities(self, attack: str, special: Optional[str]) -> Dict[str, bool]:
        """
        Parse attack and special text for special abilities.

        Args:
            attack: Attack description
            special: Special abilities description

        Returns:
            Dictionary of ability flags
        """
        abilities = {
            "poison": False,
            "paralyze": False,
            "disease": False,
            "level_drain": False,
            "regeneration": False,
            "immune_wpn": False,
            "immune_magic": False,
            "immune_cold": False,
            "immune_fire": False,
            "immune_poison": False,
            "berserking": False,
            "spell": False,
            "fly": False,
            "teleport": False,
            "gaze": False,
            "breath_weapon": False,
            "web": False,
            "charm": False,
        }

        # Combine attack and special for parsing
        text = (attack or "").lower() + " " + (special or "").lower()

        # Check for each ability
        if "poison" in text:
            abilities["poison"] = True
        if "paralyze" in text or "paralysis" in text:
            abilities["paralyze"] = True
        if "disease" in text:
            abilities["disease"] = True
        if "level drain" in text or "lvl drain" in text or "drain" in text:
            abilities["level_drain"] = True
        if "regeneration" in text or "regen" in text:
            abilities["regeneration"] = True
        if "immune wpn" in text or "imn. wpn" in text or "immune weapon" in text:
            abilities["immune_wpn"] = True
        if "immune magic" in text or "imn. magic" in text:
            abilities["immune_magic"] = True
        if "berserking" in text:
            abilities["berserking"] = True
        if "spell" in text:
            abilities["spell"] = True
        if "fly" in text:
            abilities["fly"] = True
        if "teleport" in text:
            abilities["teleport"] = True
        if "gaze" in text:
            abilities["gaze"] = True
        if "breath" in text or "fire breath" in text:
            abilities["breath_weapon"] = True
        if "web" in text:
            abilities["web"] = True
        if "charm" in text:
            abilities["charm"] = True

        return abilities

    def take_damage(self, amount: int) -> Tuple[int, bool]:
        """
        Apply damage to the monster.

        Args:
            amount: Damage amount

        Returns:
            Tuple of (actual damage taken, is_dead)
        """
        actual_damage = max(0, amount)
        self.hp_current = max(0, self.hp_current - actual_damage)

        if self.hp_current <= 0:
            self.is_alive = False

        return actual_damage, not self.is_alive

    def heal(self, amount: int) -> int:
        """
        Heal the monster (e.g., regeneration).

        Args:
            amount: Healing amount

        Returns:
            Actual amount healed
        """
        if not self.is_alive:
            return 0

        old_hp = self.hp_current
        self.hp_current = min(self.hp_max, self.hp_current + amount)
        return self.hp_current - old_hp

    def apply_regeneration(self) -> int:
        """
        Apply regeneration effect (if monster has it).

        Returns:
            Amount healed
        """
        if self.special_abilities.get("regeneration") and self.is_alive and self.hp_current > 0:
            # Regenerate 1 HP per turn
            return self.heal(1)
        return 0

    def make_attack_roll(self, target_ac: int, attack_bonus: int = 0) -> Tuple[bool, int, bool]:
        """
        Make an attack roll against a target.

        Args:
            target_ac: Target's armor class
            attack_bonus: Monster's attack bonus

        Returns:
            Tuple of (hit, roll_result, is_critical)
        """
        roll = roll_d20()
        total = roll + attack_bonus

        is_critical = roll == 20
        is_hit = total >= target_ac or is_critical

        return is_hit, roll, is_critical

    def roll_damage(self) -> int:
        """
        Roll damage for the monster.

        Parses attack description for damage notation.
        Defaults to 1d6 if no damage found.

        Returns:
            Damage amount
        """
        attack = self.attack_description.lower()

        # Check for explicit damage dice
        # Pattern: d6, d8, 2d6, 1d4, etc.
        match = re.search(r"(\d*)d(\d+)", attack)
        if match:
            num_dice = int(match.group(1)) if match.group(1) else 1
            die_size = int(match.group(2))
            return sum(random.randint(1, die_size) for _ in range(num_dice))

        # Check for weapon notation: "Wpn", "Wpn[+1]", "Wpn(2d6)", etc.
        if "wpn" in attack:
            # Check for damage in parentheses
            wpn_match = re.search(r"wpn\(([^)]+)\)", attack)
            if wpn_match:
                damage_str = wpn_match.group(1)
                dice_match = re.search(r"(\d*)d(\d+)", damage_str)
                if dice_match:
                    num_dice = int(dice_match.group(1)) if dice_match.group(1) else 1
                    die_size = int(dice_match.group(2))
                    return sum(random.randint(1, die_size) for _ in range(num_dice))

            # Default weapon damage
            return random.randint(1, 6)

        # Default to 1d6
        return random.randint(1, 6)

    def get_attack_bonus(self) -> int:
        """
        Parse attack bonus from attack description.

        Looks for patterns like "Wpn(+1)", "Claw(+2)", "+3", etc.

        Returns:
            Attack bonus (default 0)
        """
        attack = self.attack_description.lower()

        # Look for explicit bonus notation: (+1), (+2), etc.
        bonus_match = re.search(r'\(\+(\d+)\)', attack)
        if bonus_match:
            return int(bonus_match.group(1))

        # Look for bonus without parentheses: +1, +2, etc.
        bonus_match = re.search(r'\+(\d+)', attack)
        if bonus_match:
            return int(bonus_match.group(1))

        # Default: no bonus
        return 0

    def has_special_ability(self, ability: str) -> bool:
        """Check if monster has a specific special ability"""
        return self.special_abilities.get(ability, False)

    def add_status_effect(self, effect_name: str, duration: int = -1, **kwargs):
        """
        Add a status effect to the monster.

        Args:
            effect_name: Name of the effect
            duration: Duration in turns (-1 for permanent)
            **kwargs: Additional effect parameters
        """
        effect = {
            "name": effect_name,
            "duration": duration,
            **kwargs,
        }
        self.status_effects.append(effect)

    def remove_status_effect(self, effect_name: str) -> bool:
        """Remove a status effect by name"""
        for effect in self.status_effects:
            if effect["name"] == effect_name:
                self.status_effects.remove(effect)
                return True
        return False

    def update_status_effects(self):
        """Update status effects, decrementing durations"""
        effects_to_remove = []
        for effect in self.status_effects:
            if effect["duration"] > 0:
                effect["duration"] -= 1
                if effect["duration"] == 0:
                    effects_to_remove.append(effect)

        for effect in effects_to_remove:
            self.status_effects.remove(effect)

    def has_status_effect(self, effect_name: str) -> bool:
        """Check if monster has a specific status effect"""
        return any(effect["name"] == effect_name for effect in self.status_effects)

    def to_dict(self) -> Dict:
        """Serialize monster to dictionary"""
        return {
            "name": self.name,
            "hd": self.hd_string,
            "ac": self.ac,
            "attack": self.attack_description,
            "special": self.special_description,
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "is_alive": self.is_alive,
            "special_abilities": self.special_abilities,
            "status_effects": self.status_effects,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Monster":
        """
        Deserialize monster from dictionary.

        Args:
            data: Dictionary with monster data

        Returns:
            Monster instance
        """
        monster = cls(
            name=data["name"],
            hd=data["hd"],
            ac=data["ac"],
            attack=data["attack"],
            special=data.get("special"),
        )

        # Restore state (override the rolled HP with saved state)
        monster.hp_max = data.get("hp_max", monster.hp_max)
        monster.hp_current = data.get("hp_current", monster.hp_current)
        monster.is_alive = data.get("is_alive", True)
        monster.special_abilities = data.get("special_abilities", monster.special_abilities)
        monster.status_effects = data.get("status_effects", [])

        return monster

    @classmethod
    def from_table_entry(cls, entry: Dict) -> "Monster":
        """
        Create a monster from a table entry.

        Args:
            entry: Dictionary from dungeon_tables (DENIZEN or ENCOUNTER tables)

        Returns:
            Monster instance
        """
        return cls(
            name=entry["name"],
            hd=entry["hd"],
            ac=entry["ac"],
            attack=entry.get("attack", "Strike"),
            special=entry.get("special"),
        )


def roll_number_appearing(tier: int = 1, solo_pc: bool = False) -> int:
    """
    Roll for number of monsters appearing.

    Args:
        tier: Monster tier (1 or 2)
        solo_pc: Whether this is a solo PC game

    Returns:
        Number of monsters
    """
    if solo_pc:
        if tier == 1:
            # d2 (reduced from d3 for better balance)
            return random.randint(1, 2)
        else:  # tier 2
            # Always 1 (reduced from d2 for better balance)
            return 1
    else:
        # Party game - use standard numbers
        # Human: d4, Animal: d6, Humanoid: d4, Monster(S): d2, Monster(L): 1
        # For now, return a reasonable default
        return random.randint(1, 4)


def create_monster_encounter(monster_data: Dict, count: Optional[int] = None) -> List[Monster]:
    """
    Create an encounter with multiple monsters.

    Args:
        monster_data: Dictionary from tables with monster stats
        count: Number of monsters (auto-rolled if not provided)

    Returns:
        List of Monster instances
    """
    if count is None:
        count = roll_number_appearing()

    monsters = []
    for i in range(count):
        monster = Monster.from_table_entry(monster_data)
        # Add number suffix if multiple monsters
        if count > 1:
            monster.name = f"{monster.name} #{i + 1}"
        monsters.append(monster)

    return monsters
