"""
Combat System
Turn-based combat engine with attack rolls, damage, and special abilities
"""

import random
from enum import Enum
from typing import Dict, List

from generators.character import Player
from generators.monster import Monster
from tables import table_utilities
from tables.table_roller import roll_d20
from tables.table_utilities import update_status_effects


class CombatAction(Enum):
    """Available combat actions"""

    ATTACK = "attack"
    USE_ITEM = "use_item"
    FLEE = "flee"
    DEFEND = "defend"


class CombatResult(Enum):
    """Combat outcome states"""

    IN_PROGRESS = "in_progress"
    VICTORY = "victory"
    DEFEAT = "defeat"
    FLED = "fled"


class CombatEncounter:
    """Turn-based combat encounter manager with party support"""

    def __init__(self, player: Player = None, monsters: List[Monster] = None, party: List[Player] = None):
        """
        Initialize a combat encounter.

        Args:
            player: Player character (deprecated, use party instead)
            monsters: List of Monster instances
            party: List of party members (new party system)
        """
        # Support both old single-player and new party system
        if party:
            self.party = party
            self.player = party[0] if party else None  # Active character for backwards compatibility
        elif player:
            # Legacy single player mode
            self.party = [player]
            self.player = player
        else:
            self.party = []
            self.player = None

        self.monsters = monsters if monsters else []
        self.turn_number = 0
        self.combat_result = CombatResult.IN_PROGRESS
        self.combat_log: List[Dict] = []
        self.is_player_turn = True

        # Track loot
        self.loot: List[str] = []

        # Add initial log entry
        if self.player and self.monsters:
            monster_names = ", ".join(m.name for m in monsters)
            if len(self.party) > 1:
                party_names = ", ".join(p.name for p in self.party)
                self._log_message(f"Combat started! Party ({party_names}) vs {monster_names}")
            else:
                self._log_message(f"Combat started! {self.player.name} vs {monster_names}")

    def _log_message(self, message: str, message_type: str = "info"):
        """
        Add a message to the combat log.

        Args:
            message: Log message
            message_type: Type (info, attack, damage, heal, special, result)
        """
        self.combat_log.append(
            {
                "turn": self.turn_number,
                "message": message,
                "type": message_type,
            }
        )

    def get_alive_monsters(self) -> List[Monster]:
        """Get list of monsters still alive"""
        return [m for m in self.monsters if m.is_alive]

    def is_combat_over(self) -> bool:
        """Check if combat has ended"""
        return self.combat_result != CombatResult.IN_PROGRESS

    def check_combat_end(self):
        """
        Check and update combat end conditions.
        PDF Rule: At 0 HP, make WIL save - success stays at 1 HP, failure means dying
        """
        if self.player.hp_current <= 0:
            # Make death save (PDF rule)
            roll, success, message = self.player.make_death_save()
            self._log_message(message, "special")

            if success:
                # Player survives with 1 HP, check if combat can end
                self._log_message(f"{self.player.name} survives and can continue fighting!", "result")
                # Continue to check if all monsters are defeated
            else:
                # Player is dying - combat ends in defeat
                self.combat_result = CombatResult.DEFEAT
                self._log_message(f"{self.player.name} has been defeated and is dying!", "result")
                return

        alive_monsters = self.get_alive_monsters()
        if not alive_monsters:
            self.combat_result = CombatResult.VICTORY
            self._log_message(
                f"{self.player.name} is victorious! All enemies defeated!", "result"
            )
            # Award XP from defeated monsters
            self._award_xp()
            # Roll for loot from each defeated monster
            self._roll_all_loot()
            return

    def _award_xp(self):
        """
        Award XP to all party members for defeating all monsters.
        PDF Rule: 1 XP per enemy defeated (awarded to each party member)
        """
        total_xp = 0

        for monster in self.monsters:
            if not monster.is_alive:
                # PDF: Award 1 XP per enemy (not CR-based)
                total_xp += 1

        if total_xp > 0:
            # Debug: Log party size
            print(f"[XP AWARD DEBUG] Party size: {len(self.party)}, Total XP: {total_xp}")

            # Award XP to all party members
            for party_member in self.party:
                print(f"[XP AWARD DEBUG] Awarding {total_xp} XP to {party_member.name}")
                levels_gained = party_member.gain_xp(total_xp)

                if levels_gained:
                    # Party member leveled up!
                    for level in levels_gained:
                        self._log_message(
                            f"{party_member.name} gained {total_xp} XP and reached LEVEL {level}!",
                            "result"
                        )
                else:
                    # No level up, just XP gain
                    xp_to_next = party_member.get_xp_for_next_level() - party_member.xp_current
                    self._log_message(
                        f"{party_member.name} gained {total_xp} XP! ({xp_to_next} XP to next level)",
                        "result"
                    )

    def _roll_all_loot(self):
        """Roll loot for all defeated monsters"""
        from generators.item import Item

        for monster in self.monsters:
            if not monster.is_alive:
                loot_items = self._roll_loot(monster)
                self.loot.extend(loot_items)

        if self.loot:
            # Build loot summary handling both Item objects and strings
            loot_names = []
            for item in self.loot:
                if isinstance(item, Item):
                    loot_names.append(item.name)
                else:
                    loot_names.append(str(item))

            loot_summary = ", ".join(loot_names)
            self._log_message(
                f"Loot found: {loot_summary}",
                "result"
            )
        else:
            self._log_message("No loot found on the corpses.", "info")

    def _roll_loot(self, monster: Monster) -> List:
        """
        Roll for loot from a defeated monster.
        Generates Item objects based on monster tier.

        Args:
            monster: The defeated monster

        Returns:
            List of Item objects and gold amounts
        """
        from generators.item import ItemGenerator
        import random

        loot_items = []

        # Determine tier based on monster (assume tier 1 for now, can be enhanced)
        monster_tier = getattr(monster, 'tier', 1)

        # 60% chance for item loot
        if random.random() < 0.6:
            item = ItemGenerator.generate_random_loot(tier=monster_tier)
            loot_items.append(item)

        # Always drop some currency (silver/gold based on amount)
        # PDF Rule: 10 silver pieces = 1 gold piece
        currency_amount = random.randint(5, 20) * monster_tier

        if currency_amount >= 10:
            # Large rewards: give gold pieces
            gold_amount = currency_amount // 10
            silver_remainder = currency_amount % 10
            if silver_remainder > 0:
                loot_items.append(f"{gold_amount} gold, {silver_remainder} silver")
            else:
                loot_items.append(f"{gold_amount} gold")
        else:
            # Small rewards: give silver pieces
            loot_items.append(f"{currency_amount} silver")

        return loot_items

    def player_attack(self, target_index: int = 0) -> Dict:
        """
        Player attacks a monster.

        Args:
            target_index: Index of monster to attack

        Returns:
            Dictionary with attack results
        """
        if not self.is_player_turn:
            return {"success": False, "message": "Not player's turn"}

        if self.is_combat_over():
            return {"success": False, "message": "Combat is over"}

        alive_monsters = self.get_alive_monsters()
        if target_index >= len(alive_monsters):
            return {"success": False, "message": "Invalid target"}

        target = alive_monsters[target_index]

        # Determine attack type (melee or ranged) based on equipped weapon
        attack_type = "melee"
        weapon = self.player.equipment.get("weapon")
        if weapon and hasattr(weapon, 'modifiers') and 'ranged' in weapon.modifiers:
            attack_type = "ranged"

        # Make attack roll (use calculated attack bonus from equipment)
        attack_roll = roll_d20()
        attack_bonus = self.player.calculate_attack_bonus()
        attack_total = attack_roll + attack_bonus
        is_hit = attack_total >= target.ac
        is_critical = attack_roll == 20
        is_fumble = attack_roll == 1

        result = {
            "success": True,
            "attacker": self.player.name,
            "target": target.name,
            "attack_roll": attack_roll,
            "attack_total": attack_total,
            "target_ac": target.ac,
            "is_hit": is_hit,
            "is_critical": is_critical,
            "is_fumble": is_fumble,
            "damage": 0,
            "target_killed": False,
        }

        # Fumble - automatic miss
        if is_fumble:
            self._log_message(
                f"{self.player.name} fumbles the {attack_type} attack! (rolled 1)", "attack"
            )
            self.is_player_turn = False
            return result

        # Critical hit - automatic hit with double damage
        if is_critical:
            damage_die = self.player.calculate_damage()
            damage_bonus = self.player.calculate_damage_bonus()
            # D&D 5e: Critical hits double the dice, not the modifier
            damage = (self._roll_damage(damage_die) * 2) + damage_bonus
            actual_damage, killed = target.take_damage(damage)
            result["damage"] = actual_damage
            result["target_killed"] = killed

            self._log_message(
                f"{self.player.name} scores a CRITICAL HIT with {attack_type} attack on {target.name}! "
                f"Rolls {attack_roll}, deals {actual_damage} damage!",
                "attack",
            )

            if killed:
                self._log_message(f"{target.name} has been slain!", "result")

        # Normal hit
        elif is_hit:
            damage_die = self.player.calculate_damage()
            damage_bonus = self.player.calculate_damage_bonus()
            damage = self._roll_damage(damage_die) + damage_bonus
            actual_damage, killed = target.take_damage(damage)
            result["damage"] = actual_damage
            result["target_killed"] = killed

            bonus_type = "SB" if attack_type == "ranged" else "AB"
            self._log_message(
                f"{self.player.name} hits {target.name} with {attack_type} attack! "
                f"Rolls {attack_roll}+{attack_bonus} {bonus_type}={attack_total} vs AC {target.ac}, "
                f"deals {actual_damage} damage! ({target.hp_current}/{target.hp_max} HP remaining)",
                "attack",
            )

            if killed:
                self._log_message(f"{target.name} has been slain!", "result")

        # Miss
        else:
            bonus_type = "SB" if attack_type == "ranged" else "AB"
            self._log_message(
                f"{self.player.name} attacks {target.name} with {attack_type} attack but misses! "
                f"Rolls {attack_roll}+{attack_bonus} {bonus_type}={attack_total} vs AC {target.ac}",
                "attack",
            )

        # Check if combat ended
        self.check_combat_end()

        # End player turn
        self.is_player_turn = False

        return result

    def monster_turn(self):
        """Execute all monster turns"""
        if self.is_combat_over():
            return

        alive_monsters = self.get_alive_monsters()

        for monster in alive_monsters:
            # Update status effects
            table_utilities.update_status_effects(monster)

            # Check for paralysis/stun
            if monster.has_status_effect("paralyzed") or monster.has_status_effect(
                "stunned"
            ):
                self._log_message(
                    f"{monster.name} is paralyzed and cannot act!", "special"
                )
                continue

            # Apply regeneration
            if monster.has_special_ability("regeneration"):
                healed = monster.apply_regeneration()
                if healed > 0:
                    self._log_message(
                        f"{monster.name} regenerates {healed} HP! "
                        f"({monster.hp_current}/{monster.hp_max})",
                        "heal",
                    )

            # Make attack
            self._monster_attack(monster)

            # BUG FIX: If player dropped to 0 HP, check_combat_end will trigger death save
            # Break loop immediately after death save (successful or not) to give player a turn
            player_made_death_save = self.player.hp_current <= 0

            # Check if combat ended (player defeated)
            self.check_combat_end()
            if self.is_combat_over():
                break

            # Break loop if death save occurred (even if successful)
            # This gives player a turn to flee/heal before taking more hits
            if player_made_death_save:
                self._log_message(
                    f"{self.player.name} narrowly survives! Monster attacks end for this turn.",
                    "special"
                )
                break

        # End turn
        self.turn_number += 1
        self.is_player_turn = True

        # Update player status effects
        update_status_effects(self)
        # self.player.update_status_effects()

    def _monster_attack(self, monster: Monster):
        """
        Monster attacks the player.

        Args:
            monster: Monster making the attack
        """
        # Make attack roll with parsed attack bonus from monster description
        attack_bonus = monster.get_attack_bonus()
        attack_roll = roll_d20()
        attack_total = attack_roll + attack_bonus
        is_hit = attack_total >= self.player.ac
        is_critical = attack_roll == 20

        # Critical hit
        if is_critical:
            damage = monster.roll_damage() * 2
            # PDF: No damage reduction - armor only affects AC
            actual_damage, killed = self.player.take_damage(damage)

            self._log_message(
                f"{monster.name} scores a CRITICAL HIT on {self.player.name}! "
                f"Deals {actual_damage} damage!",
                "attack",
            )

            # Apply special ability effects on hit
            self._apply_monster_special_effects(monster, self.player)

            if killed:
                self._log_message(f"{self.player.name} has been defeated!", "result")

        # Normal hit
        elif is_hit:
            damage = monster.roll_damage()
            # PDF: No damage reduction - armor only affects AC
            actual_damage, killed = self.player.take_damage(damage)

            self._log_message(
                f"{monster.name} hits {self.player.name}! "
                f"Rolls {attack_roll}+{attack_bonus}={attack_total} vs AC {self.player.ac}, "
                f"deals {actual_damage} damage! ({self.player.hp_current}/{self.player.hp_max} HP remaining)",
                "attack",
            )

            # Apply special ability effects on hit
            self._apply_monster_special_effects(monster, self.player)

            if killed:
                self._log_message(f"{self.player.name} has been defeated!", "result")

        # Miss
        else:
            self._log_message(
                f"{monster.name} attacks {self.player.name} but misses! "
                f"Rolls {attack_roll}+{attack_bonus}={attack_total} vs AC {self.player.ac}",
                "attack",
            )

    def _apply_monster_special_effects(self, monster: Monster, target: Player):
        """
        Apply monster special ability effects on successful hit.

        Args:
            monster: Monster with special abilities
            target: Target (player)
        """
        # Poison - TOU saving throw (roll under TOU)
        if monster.has_special_ability("poison"):
            save_roll, success = target.make_saving_throw('tou')
            if not success:
                target.add_status_effect("poisoned", duration=6, damage_per_turn=1)
                self._log_message(
                    f"{target.name} is POISONED! (Rolled {save_roll}, needed {target.toughness} or less)", "special"
                )
            else:
                self._log_message(
                    f"{target.name} resists the poison! (Rolled {save_roll}, needed {target.toughness} or"
                    f" less)", "special"
                )

        # Paralyze - TOU saving throw (roll under TOU)
        if monster.has_special_ability("paralyze"):
            save_roll, success = target.make_saving_throw('tou')
            if not success:
                target.add_status_effect("paralyzed", duration=3)
                self._log_message(
                    f"{target.name} is PARALYZED! (Rolled {save_roll}, needed {target.toughness} or less)", "special"
                )
            else:
                self._log_message(
                    f"{target.name} resists the paralysis! (Rolled {save_roll}, needed {target.toughness} or"
                    f" less)", "special"
                )

        # Disease - TOU saving throw (roll under TOU)
        if monster.has_special_ability("disease"):
            save_roll, success = target.make_saving_throw('tou')
            if not success:
                target.add_status_effect("diseased", duration=-1)
                self._log_message(
                    f"{target.name} contracts a DISEASE! (Rolled {save_roll}, needed {target.toughness} or"
                    f" less)", "special"
                )
            else:
                self._log_message(
                    f"{target.name} resists the disease! (Rolled {save_roll}, needed {target.toughness} or"
                    f" less)", "special"
                )

        # Level drain (reduce max HP temporarily)
        if monster.has_special_ability("level_drain"):
            drain_amount = 2
            target.hp_max = max(1, target.hp_max - drain_amount)
            target.hp_current = min(target.hp_current, target.hp_max)
            self._log_message(
                f"{target.name} feels their life essence draining away! "
                f"(-{drain_amount} max HP)",
                "special",
            )

    def _roll_damage(self, damage_die: str) -> int:
        """
        Roll damage from dice notation.

        Args:
            damage_die: Dice notation (e.g., "1d6", "2d6")

        Returns:
            Damage amount
        """
        import re

        match = re.match(r"(\d+)d(\d+)", damage_die)
        if match:
            num_dice = int(match.group(1))
            die_size = int(match.group(2))
            return sum(random.randint(1, die_size) for _ in range(num_dice))

        # Default to 1d6
        return random.randint(1, 6)

    def player_use_item(self, item_name: str) -> Dict:
        """
        Player uses an item from inventory.

        Args:
            item_name: Name of item to use

        Returns:
            Dictionary with use results
        """
        if not self.is_player_turn:
            return {"success": False, "message": "Not player's turn"}

        if self.is_combat_over():
            return {"success": False, "message": "Combat is over"}

        # Check if player has the item
        if item_name not in self.player.inventory:
            return {"success": False, "message": f"You don't have {item_name}"}

        result = {"success": True, "item": item_name, "effect": None}

        # Handle common items
        if "healing" in item_name.lower() or "herb" in item_name.lower():
            # Heal player
            heal_amount = 3 if "minor" in item_name.lower() else 6
            actual_heal = self.player.heal(heal_amount)

            self._log_message(
                f"{self.player.name} uses {item_name} and heals {actual_heal} HP! "
                f"({self.player.hp_current}/{self.player.hp_max})",
                "heal",
            )

            result["effect"] = f"Healed {actual_heal} HP"
            self.player.remove_from_inventory(item_name)

        elif "antidote" in item_name.lower():
            # Cure poison
            if self.player.remove_status_effect("poisoned"):
                self._log_message(
                    f"{self.player.name} uses {item_name} and cures poison!", "heal"
                )
                result["effect"] = "Poison cured"
            else:
                self._log_message(
                    f"{self.player.name} uses {item_name} but is not poisoned.", "info"
                )
                result["effect"] = "No poison to cure"

            self.player.remove_from_inventory(item_name)

        else:
            return {"success": False, "message": f"{item_name} cannot be used in combat"}

        # End player turn
        self.is_player_turn = False

        return result

    def player_flee(self) -> Dict:
        """
        Player attempts to flee from combat.

        Returns:
            Dictionary with flee attempt results
        """
        if not self.is_player_turn:
            return {"success": False, "message": "Not player's turn"}

        if self.is_combat_over():
            return {"success": False, "message": "Combat has already ended", "combat_ended": True}

        # Flee chance: 50% base, +10% if player HP < 50%
        flee_chance = 50
        if self.player.hp_current < self.player.hp_max // 2:
            flee_chance += 10

        roll = random.randint(1, 100)
        fled = roll <= flee_chance

        result = {
            "success": True,
            "fled": fled,
            "roll": roll,
            "flee_chance": flee_chance,
        }

        if fled:
            self.combat_result = CombatResult.FLED
            self._log_message(
                f"{self.player.name} successfully flees from combat! (Rolled {roll} vs {flee_chance}%)",
                "result",
            )
        else:
            self._log_message(
                f"{self.player.name} tries to flee but fails! (Rolled {roll} vs {flee_chance}%)",
                "info",
            )
            # End player turn, monsters attack
            self.is_player_turn = False

        return result

    def get_combat_status(self) -> Dict:
        """
        Get current combat status.

        Returns:
            Dictionary with complete combat state
        """
        alive_monsters = self.get_alive_monsters()

        # Build party status
        party_status = []
        for party_member in self.party:
            party_status.append({
                "name": party_member.name,
                "hp_current": party_member.hp_current,
                "hp_max": party_member.hp_max,
                "ac": party_member.ac,
                "status_effects": party_member.status_effects,
            })

        return {
            "turn_number": self.turn_number,
            "is_player_turn": self.is_player_turn,
            "combat_result": self.combat_result.value,
            "is_over": self.is_combat_over(),
            "player": {  # Active character (backwards compatibility)
                "name": self.player.name,
                "hp_current": self.player.hp_current,
                "hp_max": self.player.hp_max,
                "ac": self.player.ac,
                "status_effects": self.player.status_effects,
            } if self.player else None,
            "party": party_status,  # All party members
            "monsters": [
                {
                    "name": m.name,
                    "hp_current": m.hp_current,
                    "hp_max": m.hp_max,
                    "ac": m.ac,
                    "is_alive": m.is_alive,
                    "status_effects": m.status_effects,
                }
                for m in alive_monsters
            ],
            "combat_log": self.combat_log[-10:],  # Last 10 messages
            "loot": self.loot,
        }

    def to_dict(self) -> Dict:
        """Serialize combat encounter to dictionary"""
        from generators.item import Item

        # Serialize loot (handle both Item objects and strings)
        serialized_loot = []
        for item in self.loot:
            if isinstance(item, Item):
                serialized_loot.append(item.to_dict())
            else:
                serialized_loot.append(item)  # String items or gold

        return {
            "turn_number": self.turn_number,
            "is_player_turn": self.is_player_turn,
            "combat_result": self.combat_result.value,
            "player": self.player.to_dict() if self.player else None,  # Backwards compatibility
            "party": [p.to_dict() for p in self.party] if self.party else [],  # New party system
            "monsters": [m.to_dict() for m in self.monsters],
            "combat_log": self.combat_log,
            "loot": serialized_loot,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CombatEncounter":
        """Deserialize combat encounter from dictionary"""
        from generators.character import Player
        from generators.monster import Monster
        from generators.item import Item

        # Load party if present (new system), otherwise load single player (legacy)
        party = None
        player = None

        if data.get("party"):
            party = [Player.from_dict(p) for p in data["party"]]
        elif data.get("player"):
            player = Player.from_dict(data["player"])

        monsters = [Monster.from_dict(m) for m in data["monsters"]]

        encounter = cls(player=player, monsters=monsters, party=party)
        encounter.turn_number = data["turn_number"]
        encounter.is_player_turn = data["is_player_turn"]
        encounter.combat_result = CombatResult(data["combat_result"])
        encounter.combat_log = data["combat_log"]

        # Deserialize loot (handle both Item dicts and strings)
        raw_loot = data.get("loot", [])
        encounter.loot = []
        for item in raw_loot:
            if isinstance(item, dict) and "item_type" in item:
                # This is a serialized Item object
                encounter.loot.append(Item.from_dict(item))
            else:
                # This is a string item or gold
                encounter.loot.append(item)

        return encounter
