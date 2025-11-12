"""
Player Character System
Handles player character creation, stats, inventory, and equipment
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from tables import overland_tables
from tables.table_roller import roll_on_table, roll_d6, roll_d20


class Player:
    """Player character with stats, inventory, and equipment"""

    def __init__(
        self,
        name: str,
        race: str = "Human",
        character_type: str = "Adventurer",
        hp_max: int = 10,
        ac: int = 10,
        attack_bonus: int = 0,
        damage_die: str = "1d6",
    ):
        """
        Initialize a player character.

        Args:
            name: Character name
            race: Character race (Human, Elf, Dwarf, Halfling)
            character_type: Character type/class
            hp_max: Maximum hit points
            ac: Armor class
            attack_bonus: Attack roll bonus
            damage_die: Damage die notation (e.g., "1d6", "2d6")
        """
        # Basic info
        self.name = name
        self.race = race
        self.character_type = character_type

        # Single Sheet Game System Attributes (3-18 range, 10 is average)
        # PDF uses: STR, DEX, WIL, TOU
        self.strength = 10  # STR - melee combat
        self.dexterity = 10  # DEX - ranged combat
        self.willpower = 10  # WIL - mental fortitude, spellcasting
        self.toughness = 10  # TOU - durability, armor class

        # Level and XP tracking
        self.level = 1
        self.xp_current = 0

        # Combat stats (now calculated from ability scores, but keep for backwards compatibility)
        self.hp_max = hp_max
        self.hp_current = hp_max
        self.ac = ac  # Legacy - now calculated from DEX + armor
        self.attack_bonus = attack_bonus  # Legacy - now calculated from STR/DEX + proficiency
        self.damage_die = damage_die

        # Inventory (10-slot system from PDF)
        self.inventory: List[str] = []
        self.inventory_max_slots = 10

        # Special Skill (choose one from PDF: Forestry, Thieving, Brutalism, Alchemy, Arcanism, Mentalism)
        self.special_skill: Optional[str] = None

        # Fatigue (from spellcasting - causes disadvantage on all rolls)
        self.is_fatigued: bool = False

        # Death save tracking (PDF: at 0 HP, make WIL save or die in 1 hour)
        self.is_dying: bool = False
        self.death_timer: Optional[int] = None  # Turns until death (None if not dying)

        # Equipment slots
        self.equipment = {
            "weapon": None,
            "armor": None,
            "shield": None,
            "helmet": None,
        }

        # Status effects
        self.status_effects: List[Dict] = []

        # Character traits and background
        self.traits: List[str] = []
        self.financial_status: Optional[str] = None
        self.starting_silver: int = 0
        self.silver: int = 0  # Current silver pieces (10 sp = 1 gp)
        self.gold: int = 0  # Current gold pieces

        # Experience tracking (for future leveling system)
        self.encounters_defeated: int = 0

        # Metadata
        self.created_at = datetime.now().isoformat()
        self.last_modified = self.created_at

    def take_damage(self, amount: int) -> Tuple[int, bool]:
        """
        Apply damage to the player.

        Args:
            amount: Damage amount

        Returns:
            Tuple of (actual damage taken, is_dead)
        """
        actual_damage = max(0, amount)
        self.hp_current = max(0, self.hp_current - actual_damage)
        self.last_modified = datetime.now().isoformat()
        return actual_damage, self.hp_current <= 0

    def heal(self, amount: int) -> int:
        """
        Heal the player.

        Args:
            amount: Healing amount

        Returns:
            Actual amount healed
        """
        old_hp = self.hp_current
        self.hp_current = min(self.hp_max, self.hp_current + amount)
        actual_healing = self.hp_current - old_hp
        self.last_modified = datetime.now().isoformat()
        return actual_healing

    def add_status_effect(self, effect_name: str, duration: int = -1, **kwargs):
        """
        Add a status effect to the player.

        Args:
            effect_name: Name of the effect (e.g., "poisoned", "paralyzed")
            duration: Duration in turns (-1 for permanent until cured)
            **kwargs: Additional effect parameters
        """
        effect = {
            "name": effect_name,
            "duration": duration,
            "applied_at": datetime.now().isoformat(),
            **kwargs,
        }
        self.status_effects.append(effect)
        self.last_modified = datetime.now().isoformat()

    def remove_status_effect(self, effect_name: str) -> bool:
        """
        Remove a status effect by name.

        Args:
            effect_name: Name of the effect to remove

        Returns:
            True if effect was found and removed
        """
        for effect in self.status_effects:
            if effect["name"] == effect_name:
                self.status_effects.remove(effect)
                self.last_modified = datetime.now().isoformat()
                return True
        return False

    def update_status_effects(self):
        """Update status effects, decrementing durations and removing expired ones"""
        effects_to_remove = []
        for effect in self.status_effects:
            if effect["duration"] > 0:
                effect["duration"] -= 1
                if effect["duration"] == 0:
                    effects_to_remove.append(effect)

        for effect in effects_to_remove:
            self.status_effects.remove(effect)

        if effects_to_remove:
            self.last_modified = datetime.now().isoformat()

    def has_status_effect(self, effect_name: str) -> bool:
        """Check if player has a specific status effect"""
        return any(effect["name"] == effect_name for effect in self.status_effects)

    def set_special_skill(self, skill: str) -> bool:
        """
        Set the character's special skill.
        PDF Rule: Choose one of 6 skills at character creation

        Args:
            skill: One of: Forestry, Thieving, Brutalism, Alchemy, Arcanism, Mentalism

        Returns:
            True if skill was set successfully
        """
        valid_skills = ["Forestry", "Thieving", "Brutalism", "Alchemy", "Arcanism", "Mentalism"]

        if skill in valid_skills:
            self.special_skill = skill
            self.last_modified = datetime.now().isoformat()
            return True
        return False

    def has_skill_advantage(self, context: str) -> bool:
        """
        Check if the character has advantage in a given context based on their special skill.

        PDF Skill Advantages:
        - Forestry: tracking, foraging, herb understanding
        - Thieving: locks, triggers
        - Brutalism: combat vs goblins, ogres, trolls, giants
        - Alchemy: potion creation
        - Arcanism: scrolls, artifacts
        - Mentalism: intimidation, persuasion

        Args:
            context: The context to check (e.g., "tracking", "locks", "vs_goblin")

        Returns:
            True if character has advantage in this context
        """
        if not self.special_skill:
            return False

        context_lower = context.lower()

        skill_advantages = {
            "Forestry": ["tracking", "foraging", "herb", "nature", "wilderness"],
            "Thieving": ["locks", "lock", "trap", "trigger", "pickpocket", "stealth"],
            "Brutalism": ["goblin", "ogre", "troll", "giant", "vs_goblin", "vs_ogre", "vs_troll", "vs_giant"],
            "Alchemy": ["potion", "elixir", "brew", "mixture", "concoction"],
            "Arcanism": ["scroll", "artifact", "magic_item", "enchantment", "spell"],
            "Mentalism": ["intimidation", "persuasion", "charm", "social", "negotiate"]
        }

        advantages = skill_advantages.get(self.special_skill, [])
        return any(adv in context_lower for adv in advantages)

    def cast_spell_from_scroll(self, spell_name: str) -> Tuple[bool, int, str]:
        """
        Attempt to cast a spell from a scroll.
        PDF Rules:
        - Anyone can cast spells via WIL Check (roll d20 under WIL)
        - Scrolls burn after attempt (success or fail)
        - Successful cast causes Fatigue (disadvantage on all rolls until overnight rest)
        - Failed cast causes d6 damage

        Args:
            spell_name: Name of the spell/scroll

        Returns:
            Tuple of (success, damage_taken, message)
        """
        # Make WIL check to cast
        roll, success = self.make_saving_throw('wil')

        if success:
            # Spell cast successfully - apply Fatigue
            self.is_fatigued = True
            message = f"{self.name} successfully casts {spell_name}! (Rolled {roll}, needed {self.willpower} or less) BUT is now Fatigued!"
            damage_taken = 0
        else:
            # Spell fails - take d6 damage
            damage_taken = roll_d6()
            self.take_damage(damage_taken)
            message = f"{self.name} fails to cast {spell_name}! (Rolled {roll}, needed {self.willpower} or less) Takes {damage_taken} damage from the backlash!"

        self.last_modified = datetime.now().isoformat()
        return success, damage_taken, message

    def sacrifice_equipment(self, slot: str) -> Tuple[bool, str]:
        """
        Sacrifice shield or helmet to negate one full attack.
        PDF Rule: Can destroy shield or helmet to avoid one full incoming attack

        Args:
            slot: Equipment slot to sacrifice ("shield" or "helmet")

        Returns:
            Tuple of (success, item_destroyed_name)
        """
        if slot not in ["shield", "helmet"]:
            return False, ""

        equipped_item = self.equipment.get(slot)

        if not equipped_item:
            return False, ""

        # Get item name
        from generators.item import Item
        if isinstance(equipped_item, Item):
            item_name = equipped_item.name
        else:
            item_name = str(equipped_item)

        # Destroy the item (remove from equipment)
        self.equipment[slot] = None
        self.last_modified = datetime.now().isoformat()

        return True, item_name

    def rest_overnight(self):
        """
        Rest overnight to recover from fatigue and restore some HP.
        PDF Rule: Regain d6 HP after day of rest, clear Fatigue
        """
        # Regain d6 HP
        heal_amount = roll_d6()
        actual_healing = self.heal(heal_amount)

        # Clear fatigue
        self.is_fatigued = False

        self.last_modified = datetime.now().isoformat()
        return actual_healing

    def make_death_save(self) -> Tuple[int, bool, str]:
        """
        Make a death save when reduced to 0 HP.
        PDF Rule: At 0 HP, make WIL Save (roll d20 under WIL)
        - Success: Stay at 1 HP and remain conscious
        - Failure: Die in 1 hour (60 turns) if not treated

        Returns:
            Tuple of (roll value, success, message)
        """
        roll, success = self.make_saving_throw('wil')

        if success:
            # Success: Stay at 1 HP
            self.hp_current = 1
            self.is_dying = False
            self.death_timer = None
            message = f"Death save SUCCESS! {self.name} clings to life with 1 HP! (Rolled {roll}, needed {self.willpower} or less)"
        else:
            # Failure: Dying, will die in 1 hour
            self.hp_current = 0
            self.is_dying = True
            self.death_timer = 60  # 60 turns = 1 hour
            message = f"Death save FAILED! {self.name} is dying and will perish in 1 hour if not treated! (Rolled {roll}, needed {self.willpower} or less)"

        self.last_modified = datetime.now().isoformat()
        return roll, success, message

    # ===== SINGLE SHEET GAME SYSTEM ATTRIBUTE BONUSES =====

    def get_melee_attack_bonus(self) -> int:
        """
        Get melee attack bonus from STR.
        PDF Rule: STR 14+ gives +1 AB (Attack Bonus)

        Returns:
            Attack bonus for melee weapons (+1 if STR >= 14, else +0)
        """
        return 1 if self.strength >= 14 else 0

    def get_ranged_attack_bonus(self) -> int:
        """
        Get ranged attack bonus from DEX.
        PDF Rule: DEX 14+ gives +1 SB (Shooting Bonus)

        Returns:
            Attack bonus for ranged weapons (+1 if DEX >= 14, else +0)
        """
        return 1 if self.dexterity >= 14 else 0

    def get_hp_bonus(self) -> int:
        """
        Get HP bonus from WIL.
        PDF Rule: WIL 14+ gives +1 max HP

        Returns:
            Bonus to max HP (+1 if WIL >= 14, else +0)
        """
        return 1 if self.willpower >= 14 else 0

    def get_ac_bonus(self) -> int:
        """
        Get AC bonus from TOU.
        PDF Rule: TOU 14+ gives +1 AC

        Returns:
            Bonus to AC (+1 if TOU >= 14, else +0)
        """
        return 1 if self.toughness >= 14 else 0

    # ===== CURRENCY MANAGEMENT =====

    def add_currency(self, silver: int = 0, gold: int = 0):
        """
        Add currency to the player and auto-convert silver to gold.
        PDF Rule: 10 silver pieces = 1 gold piece

        Args:
            silver: Silver pieces to add
            gold: Gold pieces to add
        """
        self.silver += silver
        self.gold += gold
        self._convert_silver_to_gold()

    def remove_currency(self, silver: int = 0, gold: int = 0) -> bool:
        """
        Remove currency from the player. Returns False if insufficient funds.

        Args:
            silver: Silver pieces to remove
            gold: Gold pieces to remove

        Returns:
            True if successful, False if insufficient funds
        """
        total_needed_in_silver = silver + (gold * 10)
        total_available_in_silver = self.silver + (self.gold * 10)

        if total_available_in_silver < total_needed_in_silver:
            return False

        # Convert all to silver, subtract, then convert back
        self.silver = total_available_in_silver - total_needed_in_silver
        self.gold = 0
        self._convert_silver_to_gold()
        return True

    def _convert_silver_to_gold(self):
        """
        Auto-convert silver to gold when silver >= 10.
        PDF Rule: 10 silver pieces = 1 gold piece
        """
        if self.silver >= 10:
            gold_to_add = self.silver // 10
            self.gold += gold_to_add
            self.silver = self.silver % 10

    def get_total_currency_in_silver(self) -> int:
        """Get total currency value in silver pieces."""
        return self.silver + (self.gold * 10)

    # ===== SINGLE SHEET GAME SYSTEM XP AND LEVELING =====

    # PDF Rule: Flat 20 XP per level
    XP_PER_LEVEL = 20

    def get_xp_for_next_level(self) -> int:
        """
        Get XP required for next level.
        PDF Rule: Flat 20 XP per level

        Returns:
            XP needed for next level
        """
        return self.level * self.XP_PER_LEVEL

    def gain_xp(self, amount: int) -> List[int]:
        """
        Gain XP and check for level-ups.
        PDF Rule: 20 XP per level

        Args:
            amount: XP to gain

        Returns:
            List of levels gained (empty if no level-up)
        """
        self.xp_current += amount
        levels_gained = []

        # Check for level-ups (can gain multiple levels at once)
        while self.xp_current >= self.get_xp_for_next_level():
            self.level_up()
            levels_gained.append(self.level)

        self.last_modified = datetime.now().isoformat()
        return levels_gained

    def level_up(self):
        """
        Level up the character.
        PDF Rules:
        - Add 1d6 to max HP
        - Roll 3d6 for each attribute; if roll exceeds current value, increase attribute by +1
        """
        self.level += 1

        # Increase HP: roll 1d6 (no modifier)
        hp_increase = roll_d6()
        self.hp_max += hp_increase
        self.hp_current += hp_increase  # Heal to new max

        # Attribute improvements: Roll 3d6 for each attribute
        # If the roll exceeds the current attribute value, increase by +1
        attributes = ['strength', 'dexterity', 'willpower', 'toughness']
        for attr in attributes:
            roll = roll_d6() + roll_d6() + roll_d6()  # 3d6
            current_value = getattr(self, attr)
            if roll > current_value:
                setattr(self, attr, current_value + 1)

        self.last_modified = datetime.now().isoformat()

    # ===== SINGLE SHEET GAME SYSTEM SAVING THROWS =====

    def make_saving_throw(self, attribute: str, advantage: bool = False, disadvantage: bool = False) -> Tuple[int, bool]:
        """
        Make a saving throw using PDF rules: roll d20 equal to or under attribute value.

        PDF Rules:
        - Roll 1d20
        - Success if roll <= attribute value
        - Advantage: roll 2d20, take better (higher) result
        - Disadvantage: roll 2d20, take worse (lower) result

        Args:
            attribute: Attribute to use ('str', 'dex', 'wil', 'tou')
            advantage: Roll with advantage (2d20 take better)
            disadvantage: Roll with disadvantage (2d20 take worse)

        Returns:
            Tuple of (roll value, success)
        """
        # Get attribute value
        attribute_map = {
            'str': self.strength,
            'dex': self.dexterity,
            'wil': self.willpower,
            'tou': self.toughness
        }
        target = attribute_map.get(attribute.lower(), 10)

        # Apply fatigue (disadvantage on all rolls)
        if self.is_fatigued:
            disadvantage = True

        # Roll d20 (with advantage/disadvantage)
        if advantage and not disadvantage:
            roll = max(roll_d20(), roll_d20())  # Take better (higher) roll
        elif disadvantage:
            roll = min(roll_d20(), roll_d20())  # Take worse (lower) roll
        else:
            roll = roll_d20()

        # Success if roll is equal to or under attribute value
        success = roll <= target

        return roll, success

    def equip_item(self, slot: str, item: str):
        """
        Equip an item to a specific slot.

        Args:
            slot: Equipment slot (weapon, armor, shield, helmet)
            item: Item description/name
        """
        if slot in self.equipment:
            # Unequip current item if any
            if self.equipment[slot]:
                self.inventory.append(self.equipment[slot])

            # Equip new item
            self.equipment[slot] = item

            # Remove from inventory if present
            if item in self.inventory:
                self.inventory.remove(item)

            self.last_modified = datetime.now().isoformat()

    def unequip_item(self, slot: str):
        """
        Unequip an item from a specific slot.

        Args:
            slot: Equipment slot to unequip
        """
        if slot in self.equipment and self.equipment[slot]:
            item = self.equipment[slot]
            self.equipment[slot] = None
            self.inventory.append(item)
            self.last_modified = datetime.now().isoformat()

    def get_inventory_slots_used(self) -> int:
        """
        Calculate total inventory slots used.
        PDF Rule: 10 slots max, bulky items take 2 slots

        Returns:
            Number of slots currently used
        """
        from generators.item import Item

        slots_used = 0
        for item in self.inventory:
            if isinstance(item, Item):
                # Check if item is bulky
                slots_used += item.get_slot_size()
            elif isinstance(item, str):
                # String items - check for bulky keywords
                if any(bulky in item.lower() for bulky in ['plate', 'chain', 'great sword', 'warhammer', 'battle axe', 'crossbow']):
                    slots_used += 2
                else:
                    slots_used += 1
            else:
                slots_used += 1

        return slots_used

    def get_available_inventory_slots(self) -> int:
        """
        Get number of available inventory slots.

        Returns:
            Number of available slots
        """
        return self.inventory_max_slots - self.get_inventory_slots_used()

    def can_add_to_inventory(self, item) -> Tuple[bool, str]:
        """
        Check if an item can be added to inventory.

        Args:
            item: Item to check (Item object or string)

        Returns:
            Tuple of (can_add: bool, reason: str)
        """
        from generators.item import Item

        # Determine item slot size
        slot_size = 1
        if isinstance(item, Item):
            slot_size = item.get_slot_size()
        elif isinstance(item, str):
            if any(bulky in item.lower() for bulky in ['plate', 'chain', 'great sword', 'warhammer', 'battle axe', 'crossbow']):
                slot_size = 2

        available = self.get_available_inventory_slots()

        if slot_size <= available:
            return True, "OK"
        else:
            return False, f"Not enough inventory space (need {slot_size} slots, have {available})"

    def add_to_inventory(self, item: str):
        """
        Add an item to inventory with slot checking.
        PDF Rule: 10 slots max

        Args:
            item: Item to add
        """
        can_add, reason = self.can_add_to_inventory(item)
        if can_add:
            self.inventory.append(item)
            self.last_modified = datetime.now().isoformat()
        else:
            # For backward compatibility, still add but warn
            # In a real implementation, this might raise an exception
            self.inventory.append(item)
            self.last_modified = datetime.now().isoformat()

    def remove_from_inventory(self, item: str) -> bool:
        """
        Remove an item from inventory.

        Args:
            item: Item to remove

        Returns:
            True if item was found and removed
        """
        if item in self.inventory:
            self.inventory.remove(item)
            self.last_modified = datetime.now().isoformat()
            return True
        return False

    # ===== ITEM SYSTEM METHODS =====

    def calculate_total_ac(self) -> int:
        """
        Calculate total AC using PDF rules: 10 + TOU bonus + armor/shield/helmet bonuses.
        PDF Rule: TOU 14+ gives +1 AC
        Works with both string-based and Item-based equipment.

        Returns:
            Total armor class
        """
        from generators.item import Item

        # PDF base AC: 10 + TOU bonus
        total_ac = 10 + self.get_ac_bonus()

        # Check for equipped armor
        armor = self.equipment.get("armor")
        if armor:
            if isinstance(armor, Item):
                # Item-based armor provides AC bonus
                total_ac += armor.ac_bonus
            elif isinstance(armor, str) and "AC" in armor:
                # String-based armor with AC notation
                import re
                match = re.search(r'AC\s+(\d+)', armor)
                if match:
                    # This is absolute AC (like "Chain Mail (AC 16)")
                    # PDF: Leather +2, Chain +3, Plate +4
                    total_ac = int(match.group(1))

        # Add bonuses from shield, helmet, and other items
        # PDF: Shield +1, Helmet +1
        for slot in ["shield", "helmet"]:
            equipped = self.equipment.get(slot)
            if equipped and isinstance(equipped, Item):
                total_ac += equipped.ac_bonus

        return total_ac

    def calculate_attack_bonus(self) -> int:
        """
        Calculate total attack bonus using PDF rules:
        STR 14+ gives +1 AB for melee, DEX 14+ gives +1 SB for ranged

        Returns:
            Total attack bonus
        """
        from generators.item import Item

        # PDF formula: +1 if STR/DEX >= 14 (depending on weapon type)
        # Default to melee (STR bonus)
        ability_bonus = self.get_melee_attack_bonus()

        # Check weapon type to determine if DEX should be used
        weapon = self.equipment.get("weapon")
        if weapon and isinstance(weapon, Item):
            # Check if weapon has 'finesse' or 'ranged' in modifiers
            if weapon.modifiers and ('finesse' in weapon.modifiers or 'ranged' in weapon.modifiers):
                # Use ranged attack bonus (DEX)
                ability_bonus = self.get_ranged_attack_bonus()

        total_bonus = ability_bonus

        # Add weapon attack bonus
        if weapon and isinstance(weapon, Item):
            total_bonus += weapon.attack_bonus

        return total_bonus

    def calculate_damage(self) -> str:
        """
        Calculate damage die including weapon damage.

        Returns:
            Damage die string (e.g., "1d8", "2d6")
        """
        from generators.item import Item

        # Check for equipped weapon
        weapon = self.equipment.get("weapon")
        if weapon and isinstance(weapon, Item) and weapon.damage_die:
            return weapon.damage_die

        # Check for string-based weapon with damage notation
        if weapon and isinstance(weapon, str):
            import re
            match = re.search(r'(\d+d\d+)', weapon)
            if match:
                return match.group(1)

        # Fall back to base damage die
        return self.damage_die

    def calculate_damage_bonus(self) -> int:
        """
        Calculate damage bonus.
        PDF Rule: No attribute bonuses to damage (only weapon dice matter)

        Returns:
            Damage bonus to add to damage roll (usually 0)
        """
        from generators.item import Item

        # PDF: No attribute modifiers to damage
        # Only weapon bonuses count
        damage_bonus = 0

        weapon = self.equipment.get("weapon")
        if weapon and isinstance(weapon, Item) and hasattr(weapon, 'damage_bonus'):
            damage_bonus += weapon.damage_bonus

        return damage_bonus

    def calculate_damage_reduction(self) -> int:
        """
        Calculate damage reduction.
        PDF Rule: No damage reduction system - armor only affects AC

        Returns:
            Damage reduction value (always 0)
        """
        # PDF: No damage reduction - armor only affects whether you get hit
        return 0

    def get_total_stats(self) -> Dict:
        """
        Get all calculated stats including equipment bonuses.

        Returns:
            Dictionary with all stats
        """
        return {
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "ac": self.calculate_total_ac(),
            "attack_bonus": self.calculate_attack_bonus(),
            "damage": self.calculate_damage(),
            "gold": self.gold,
        }

    def equip_item_object(self, item):
        """
        Equip an Item object to its appropriate slot.
        Supports the new Item system.

        Args:
            item: Item object to equip

        Returns:
            Tuple of (success: bool, message: str)
        """
        from generators.item import Item, ItemSlot

        if not isinstance(item, Item):
            return False, "Not a valid Item object"

        if item.slot == ItemSlot.NONE:
            return False, "This item cannot be equipped"

        slot_name = item.slot.value

        # Unequip current item if any
        if self.equipment.get(slot_name):
            old_item = self.equipment[slot_name]
            self.inventory.append(old_item)

        # Equip new item
        self.equipment[slot_name] = item

        # Remove from inventory if present
        if item in self.inventory:
            self.inventory.remove(item)

        self.last_modified = datetime.now().isoformat()
        return True, f"Equipped {item.name}"

    def add_item_to_inventory(self, item):
        """
        Add an Item object to inventory.
        Supports both string and Item objects for backward compatibility.

        Args:
            item: Item object or string
        """
        self.inventory.append(item)
        self.last_modified = datetime.now().isoformat()

    def remove_item_from_inventory(self, item) -> bool:
        """
        Remove an Item object from inventory.

        Args:
            item: Item object to remove

        Returns:
            True if item was found and removed
        """
        if item in self.inventory:
            self.inventory.remove(item)
            self.last_modified = datetime.now().isoformat()
            return True
        return False

    def find_item_by_name(self, item_name: str):
        """
        Find an item in inventory by name.
        Works with both string and Item objects.

        Args:
            item_name: Name of the item to find

        Returns:
            The item if found, None otherwise
        """
        from generators.item import Item

        for item in self.inventory:
            if isinstance(item, Item) and item.name == item_name:
                return item
            elif isinstance(item, str) and item == item_name:
                return item
        return None

    # ===== END ITEM SYSTEM METHODS =====

    def to_dict(self) -> Dict:
        """Serialize player to dictionary"""
        from generators.item import Item

        # Serialize inventory (handle both strings and Item objects)
        serialized_inventory = []
        for item in self.inventory:
            if isinstance(item, Item):
                serialized_inventory.append(item.to_dict())
            else:
                serialized_inventory.append(item)  # String items

        # Serialize equipment (handle both strings and Item objects)
        serialized_equipment = {}
        for slot, item in self.equipment.items():
            if item:
                if isinstance(item, Item):
                    serialized_equipment[slot] = item.to_dict()
                else:
                    serialized_equipment[slot] = item  # String items
            else:
                serialized_equipment[slot] = None

        return {
            "name": self.name,
            "race": self.race,
            "character_type": self.character_type,
            # Single Sheet Game System attributes
            "strength": self.strength,
            "dexterity": self.dexterity,
            "willpower": self.willpower,
            "toughness": self.toughness,
            # Level and XP
            "level": self.level,
            "xp_current": self.xp_current,
            # Combat stats
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "ac": self.ac,  # Legacy
            "attack_bonus": self.attack_bonus,  # Legacy
            "damage_die": self.damage_die,
            # Inventory and equipment
            "inventory": serialized_inventory,
            "inventory_max_slots": self.inventory_max_slots,
            "equipment": serialized_equipment,
            "status_effects": self.status_effects,
            # Special abilities
            "special_skill": self.special_skill,
            "is_fatigued": self.is_fatigued,
            "is_dying": self.is_dying,
            "death_timer": self.death_timer,
            # Background
            "traits": self.traits,
            "financial_status": self.financial_status,
            "starting_silver": self.starting_silver,
            "silver": self.silver,
            "gold": self.gold,
            "encounters_defeated": self.encounters_defeated,  # Legacy
            # Metadata
            "created_at": self.created_at,
            "last_modified": self.last_modified,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Player":
        """
        Deserialize player from dictionary.

        Args:
            data: Dictionary with player data

        Returns:
            Player instance
        """
        player = cls(
            name=data["name"],
            race=data.get("race", "Human"),
            character_type=data.get("character_type", "Adventurer"),
            hp_max=data.get("hp_max", 10),
            ac=data.get("ac", 10),
            attack_bonus=data.get("attack_bonus", 0),
            damage_die=data.get("damage_die", "1d6"),
        )

        from generators.item import Item

        player.hp_current = data.get("hp_current", player.hp_max)

        # Deserialize inventory (handle both strings and Item dicts)
        raw_inventory = data.get("inventory", [])
        player.inventory = []
        for item in raw_inventory:
            if isinstance(item, dict) and "item_type" in item:
                # This is a serialized Item object
                player.inventory.append(Item.from_dict(item))
            else:
                # This is a string item (backward compatibility)
                player.inventory.append(item)

        # Deserialize equipment (handle both strings and Item dicts)
        raw_equipment = data.get("equipment", {})
        player.equipment = {
            "weapon": None,
            "armor": None,
            "shield": None,
            "helmet": None,
        }
        for slot, item in raw_equipment.items():
            if item:
                if isinstance(item, dict) and "item_type" in item:
                    # This is a serialized Item object
                    player.equipment[slot] = Item.from_dict(item)
                else:
                    # This is a string item (backward compatibility)
                    player.equipment[slot] = item

        # Single Sheet Game System attributes (with defaults for backwards compatibility)
        player.strength = data.get("strength", 10)
        player.dexterity = data.get("dexterity", 10)
        player.willpower = data.get("willpower", data.get("wisdom", 10))  # Fallback to wisdom for old saves
        player.toughness = data.get("toughness", data.get("constitution", 10))  # Fallback to constitution for old saves

        # Level and XP (with defaults for backwards compatibility)
        player.level = data.get("level", 1)
        player.xp_current = data.get("xp_current", 0)

        # Special abilities
        player.special_skill = data.get("special_skill")
        player.is_fatigued = data.get("is_fatigued", False)
        player.is_dying = data.get("is_dying", False)
        player.death_timer = data.get("death_timer")
        player.inventory_max_slots = data.get("inventory_max_slots", 10)

        player.status_effects = data.get("status_effects", [])
        player.traits = data.get("traits", [])
        player.financial_status = data.get("financial_status")
        player.starting_silver = data.get("starting_silver", 0)

        # Currency (with backward compatibility for old saves)
        player.silver = data.get("silver", 0)
        player.gold = data.get("gold", 0)

        # Backward compatibility: if silver not in save but gold exists, assume all currency is gold
        if "silver" not in data and "gold" in data:
            # Old save format had everything as gold, keep it that way
            pass

        player.encounters_defeated = data.get("encounters_defeated", 0)
        player.created_at = data.get("created_at", player.created_at)
        player.last_modified = data.get("last_modified", player.last_modified)

        return player


def create_character(
    name: str,
    race: str = "Human",
    character_type: str = "Adventurer",
    hp: int = 10,
    ac: int = 10,
    attack_bonus: int = 0,
    weapon: Optional[str] = None,
    armor: Optional[str] = None,
) -> Player:
    """
    Create a custom player character.

    Args:
        name: Character name
        race: Character race
        character_type: Character type/class
        hp: Hit points
        ac: Armor class
        attack_bonus: Attack bonus
        weapon: Starting weapon
        armor: Starting armor

    Returns:
        Player instance
    """
    player = Player(
        name=name,
        race=race,
        character_type=character_type,
        hp_max=hp,
        ac=ac,
        attack_bonus=attack_bonus,
        damage_die="1d6",  # Default damage die
    )

    # Equip starting gear
    if weapon:
        player.equip_item("weapon", weapon)
    if armor:
        player.equip_item("armor", armor)

    # Add basic starting items
    player.add_to_inventory("Ration")
    player.add_to_inventory("Waterskin")
    player.add_to_inventory("Torch")

    return player


def roll_ability_score() -> int:
    """
    Roll D&D 5e ability score using 4d6 drop lowest method.

    Returns:
        Ability score (typically 3-18, average ~12)
    """
    rolls = [roll_d6() for _ in range(4)]
    rolls.remove(min(rolls))  # Drop the lowest roll
    return sum(rolls)


def roll_all_ability_scores() -> Dict[str, int]:
    """
    Roll all four Single Sheet Game System attributes using 4d6 drop lowest.

    Returns:
        Dictionary with attribute scores (STR, DEX, WIL, TOU)
    """
    return {
        'strength': roll_ability_score(),
        'dexterity': roll_ability_score(),
        'willpower': roll_ability_score(),
        'toughness': roll_ability_score()
    }


def generate_random_character(name: Optional[str] = None) -> Player:
    """
    Generate a random character using the game tables.

    Args:
        name: Optional character name (random if not provided)

    Returns:
        Player instance with randomly generated attributes
    """
    # Generate race
    race = roll_on_table(overland_tables.RACE)

    # Generate character type
    char_type = roll_on_table(overland_tables.CHARACTER_TYPE)

    # Generate financial status (for flavor/traits, not starting silver)
    financial = roll_on_table(overland_tables.FINANCIAL)

    # PDF Rule: Roll 3d6 for starting silver
    starting_silver = roll_d6() + roll_d6() + roll_d6()

    # Generate traits
    trait1 = roll_on_table(overland_tables.TRAITS_1)
    trait2 = roll_on_table(overland_tables.TRAITS_2)

    # Generate name if not provided
    if not name:
        # For simplicity, use a generic name
        name = f"{race} {char_type}"

    # Roll Single Sheet Game System attributes
    ability_scores = roll_all_ability_scores()

    # Calculate starting HP using PDF rules: 1d6+1
    # WIL 14+ adds +1 to max HP
    base_hp = roll_d6() + 1
    wil_bonus = 1 if ability_scores['willpower'] >= 14 else 0
    starting_hp = base_hp + wil_bonus

    # Create player with Single Sheet Game System stats
    player = Player(
        name=name,
        race=race,
        character_type=char_type,
        hp_max=starting_hp,
        ac=10,  # Base AC (will be calculated from TOU + armor)
        attack_bonus=0,  # Legacy (will be calculated from STR/DEX)
        damage_die="1d6",
    )

    # Set attribute scores
    player.strength = ability_scores['strength']
    player.dexterity = ability_scores['dexterity']
    player.willpower = ability_scores['willpower']
    player.toughness = ability_scores['toughness']

    # Set additional attributes
    player.financial_status = financial
    player.starting_silver = starting_silver
    player.silver = starting_silver  # Initialize silver to starting silver (3d6 sp)
    player.gold = 0  # Start with no gold pieces
    player.traits = [trait1, trait2]

    # Select random special skill (PDF rule: choose one of 6)
    import random
    special_skills = ["Forestry", "Thieving", "Brutalism", "Alchemy", "Arcanism", "Mentalism"]
    player.special_skill = random.choice(special_skills)

    # PDF Rule: Starting equipment is Cloak + 3 Rations
    # Players buy their other equipment with their 3d6 silver
    player.add_to_inventory("Cloak")
    player.add_to_inventory("Ration")
    player.add_to_inventory("Ration")
    player.add_to_inventory("Ration")

    return player


def save_character(player: Player, filename: Optional[str] = None) -> str:
    """
    Save character to a file.

    Args:
        player: Player to save
        filename: Optional filename (auto-generated if not provided)

    Returns:
        Path to saved file
    """
    # Create characters directory if it doesn't exist
    char_dir = os.path.join(os.getcwd(), "saved_characters")
    os.makedirs(char_dir, exist_ok=True)

    # Generate filename if not provided
    if not filename:
        safe_name = "".join(c for c in player.name if c.isalnum() or c in (" ", "_"))
        safe_name = safe_name.replace(" ", "_")
        filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = os.path.join(char_dir, filename)

    # Save to file
    with open(filepath, "w") as f:
        json.dump(player.to_dict(), f, indent=2)

    return filepath


def load_character(filename: str) -> Player:
    """
    Load character from a file.

    Args:
        filename: Filename or full path to character file

    Returns:
        Player instance

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Check if it's a full path or just a filename
    if os.path.exists(filename):
        filepath = filename
    else:
        char_dir = os.path.join(os.getcwd(), "saved_characters")
        filepath = os.path.join(char_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Character file not found: {filepath}")

    # Load from file
    with open(filepath, "r") as f:
        data = json.load(f)

    return Player.from_dict(data)


def list_saved_characters() -> List[Dict]:
    """
    List all saved characters.

    Returns:
        List of dicts with character info (name, race, type, file)
    """
    char_dir = os.path.join(os.getcwd(), "saved_characters")

    if not os.path.exists(char_dir):
        return []

    characters = []
    for filename in os.listdir(char_dir):
        if filename.endswith(".json"):
            try:
                filepath = os.path.join(char_dir, filename)
                with open(filepath, "r") as f:
                    data = json.load(f)

                characters.append(
                    {
                        "filename": filename,
                        "name": data.get("name", "Unknown"),
                        "race": data.get("race", "Unknown"),
                        "character_type": data.get("character_type", "Unknown"),
                        "level": f"HP: {data.get('hp_current', 0)}/{data.get('hp_max', 0)}",
                        "created_at": data.get("created_at", "Unknown"),
                    }
                )
            except Exception:
                # Skip invalid files
                continue

    # Sort by creation date (newest first)
    characters.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return characters
