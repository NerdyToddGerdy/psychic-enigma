"""
Item System for RPG Game
Handles procedural item generation with rarity tiers, random stats, and modifiers
Inspired by Clickpocalypse-style loot systems
"""

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ItemRarity(Enum):
    """Item rarity tiers with color codes"""
    COMMON = ("common", "#FFFFFF", 0)  # White
    UNCOMMON = ("uncommon", "#1EFF00", 1)  # Green
    RARE = ("rare", "#0070DD", 2)  # Blue
    EPIC = ("epic", "#A335EE", 3)  # Purple
    LEGENDARY = ("legendary", "#FF8000", 4)  # Orange

    def __init__(self, name: str, color: str, tier: int):
        self._name = name
        self.color = color
        self.tier = tier

    @property
    def display_name(self):
        return self._name.capitalize()

    @property
    def name(self):
        return self._name


class ItemType(Enum):
    """Types of items"""
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    SHIELD = "shield"
    CONSUMABLE = "consumable"
    QUEST_ITEM = "quest_item"
    JUNK = "junk"


class ItemSlot(Enum):
    """Equipment slots"""
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    SHIELD = "shield"
    NONE = None  # For consumables/quest items


@dataclass
class Item:
    """
    Represents an item with stats, rarity, and modifiers.
    """
    name: str
    item_type: ItemType
    slot: ItemSlot
    rarity: ItemRarity
    value: int  # Gold value

    # Stats that can be modified
    damage_die: Optional[str] = None  # e.g., "1d8", "2d6"
    attack_bonus: int = 0
    ac_bonus: int = 0
    damage_reduction: int = 0

    # Special modifiers
    modifiers: List[str] = field(default_factory=list)  # e.g., ["fire_damage", "lifesteal"]

    # PDF inventory system
    is_bulky: bool = False  # Bulky items take 2 slots (Plate, Chain, Great Sword, etc.)

    # Consumable properties
    healing_amount: int = 0
    effect_duration: int = 0
    effect_type: Optional[str] = None  # e.g., "heal", "buff_attack", "buff_defense"

    # Description
    description: str = ""

    def to_dict(self) -> Dict:
        """Serialize item to dictionary"""
        return {
            "name": self.name,
            "item_type": self.item_type.value,
            "slot": self.slot.value if self.slot != ItemSlot.NONE else None,
            "rarity": self.rarity.name,
            "value": self.value,
            "damage_die": self.damage_die,
            "attack_bonus": self.attack_bonus,
            "ac_bonus": self.ac_bonus,
            "damage_reduction": self.damage_reduction,
            "modifiers": self.modifiers,
            "is_bulky": self.is_bulky,
            "healing_amount": self.healing_amount,
            "effect_duration": self.effect_duration,
            "effect_type": self.effect_type,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Item":
        """Deserialize item from dictionary"""
        # Handle rarity - can be enum name (RARE) or lowercase string (rare)
        rarity_value = data["rarity"]
        if isinstance(rarity_value, str):
            # Try uppercase first (enum name)
            try:
                rarity = ItemRarity[rarity_value.upper()]
            except KeyError:
                # Fall back to searching by value
                rarity = next((r for r in ItemRarity if r.name == rarity_value), ItemRarity.COMMON)
        else:
            rarity = rarity_value

        return cls(
            name=data["name"],
            item_type=ItemType(data["item_type"]),
            slot=ItemSlot(data["slot"]) if data.get("slot") else ItemSlot.NONE,
            rarity=rarity,
            value=data["value"],
            damage_die=data.get("damage_die"),
            attack_bonus=data.get("attack_bonus", 0),
            ac_bonus=data.get("ac_bonus", 0),
            damage_reduction=data.get("damage_reduction", 0),
            modifiers=data.get("modifiers", []),
            is_bulky=data.get("is_bulky", False),
            healing_amount=data.get("healing_amount", 0),
            effect_duration=data.get("effect_duration", 0),
            effect_type=data.get("effect_type"),
            description=data.get("description", ""),
        )

    def get_total_bonus(self) -> int:
        """Calculate total bonus value for comparison"""
        bonus = self.attack_bonus + self.ac_bonus + self.damage_reduction
        if self.damage_die:
            # Parse damage die to get average damage
            if 'd' in self.damage_die:
                parts = self.damage_die.split('d')
                num_dice = int(parts[0])
                die_size = int(parts[1])
                bonus += (num_dice * (die_size + 1)) // 2  # Average damage
        return bonus

    def get_slot_size(self) -> int:
        """
        Get inventory slot size for this item.
        PDF Rule: Bulky items take 2 slots, normal items take 1 slot

        Returns:
            Number of inventory slots this item occupies
        """
        return 2 if self.is_bulky else 1


class ItemGenerator:
    """Generates procedural items with random stats and modifiers"""

    # Item name components
    WEAPON_PREFIXES = ["Rusty", "Crude", "Steel", "Sharp", "Gleaming", "Mighty", "Ancient", "Legendary"]
    ARMOR_PREFIXES = ["Tattered", "Worn", "Sturdy", "Reinforced", "Gleaming", "Enchanted", "Ancient", "Legendary"]

    WEAPON_TYPES = ["Dagger", "Short Sword", "Long Sword", "Great Sword", "Axe", "Battle Axe", "Mace", "Warhammer",
                    "Spear", "Bow", "Crossbow"]
    ARMOR_TYPES = ["Leather Armor", "Hide Armor", "Chain Mail", "Scale Mail", "Plate Mail"]
    HELMET_TYPES = ["Leather Cap", "Iron Helm", "Steel Helm", "Full Helm"]
    SHIELD_TYPES = ["Buckler", "Round Shield", "Kite Shield", "Tower Shield"]

    SUFFIXES = ["of Fire", "of Ice", "of Lightning", "of the Bear", "of the Wolf", "of Protection",
                "of Power", "of Swiftness", "of the Titan", "of the Phoenix"]

    # Modifier effects
    MODIFIERS = ["fire_damage", "ice_damage", "lightning_damage", "lifesteal", "critical_hit",
                 "armor_pierce", "durability", "luck"]

    # Consumables
    CONSUMABLE_TYPES = [
        ("Healing Potion", "heal", 20, 0),
        ("Greater Healing Potion", "heal", 40, 0),
        ("Antidote", "cure_poison", 0, 0),
        ("Strength Potion", "buff_attack", 0, 3),
        ("Defense Potion", "buff_defense", 0, 3),
    ]

    # Spell Scrolls (PDF system)
    SPELL_SCROLLS = [
        ("Fireball Scroll", "spell_damage", "Hurls a ball of fire dealing 2d6 damage to target"),
        ("Lightning Bolt Scroll", "spell_damage", "Strikes target with lightning for 2d6 damage"),
        ("Ice Shard Scroll", "spell_damage", "Launches ice shards dealing 1d8 damage"),
        ("Healing Light Scroll", "spell_heal", "Restores 2d6 HP to the caster"),
        ("Shield Scroll", "spell_buff", "Grants +2 AC for 3 turns"),
        ("Haste Scroll", "spell_buff", "Grants advantage on next 2 attacks"),
        ("Sleep Scroll", "spell_debuff", "Target must make WIL save or be paralyzed for 2 turns"),
        ("Web Scroll", "spell_debuff", "Target movement reduced, disadvantage on attacks for 2 turns"),
    ]

    @classmethod
    def generate_weapon(cls, tier: int = 1, rarity: Optional[ItemRarity] = None) -> Item:
        """
        Generate a weapon with stats scaled by tier and rarity.

        Args:
            tier: Dungeon/enemy tier (1-4), affects base stats
            rarity: Optional fixed rarity, otherwise random based on tier

        Returns:
            Generated weapon Item
        """
        if rarity is None:
            rarity = cls._roll_rarity(tier)

        # Base weapon type
        weapon_type = random.choice(cls.WEAPON_TYPES)

        # Determine damage die based on weapon type and tier
        # PDF: d6 for small, 2d6 take higher for medium, d8 for bulky
        damage_dice = {
            "Dagger": "1d6",
            "Short Sword": "1d6",
            "Long Sword": "1d8",  # 2d6 take higher in PDF
            "Great Sword": "2d6",  # d8 bulky in PDF
            "Axe": "1d6",
            "Battle Axe": "2d6",  # d8 bulky in PDF
            "Mace": "1d8",  # 2d6 take higher in PDF
            "Warhammer": "2d6",  # d8 bulky in PDF
            "Spear": "1d8",  # 2d6 take higher in PDF
            "Bow": "1d8",  # 2d6 take higher in PDF
            "Crossbow": "2d6",  # d8 bulky in PDF
        }
        base_damage = damage_dice.get(weapon_type, "1d6")

        # Scale damage by tier
        if tier >= 2:
            base_damage = cls._upgrade_damage_die(base_damage)
        if tier >= 4:
            base_damage = cls._upgrade_damage_die(base_damage)

        # Attack bonus scaled by rarity
        attack_bonus = cls._get_bonus_by_rarity(rarity)

        # Modifiers for higher rarities
        modifiers = []
        if rarity.tier >= ItemRarity.RARE.tier:
            modifiers.append(random.choice(cls.MODIFIERS))
        if rarity.tier >= ItemRarity.LEGENDARY.tier:
            modifiers.append(random.choice([m for m in cls.MODIFIERS if m not in modifiers]))

        # Build name
        name = cls._build_item_name(weapon_type, rarity, attack_bonus, modifiers)

        # Value scales with rarity and tier
        value = (10 + tier * 5) * (rarity.tier + 1)

        # PDF: Mark bulky weapons (Great Sword, Warhammer, Battle Axe, Crossbow)
        bulky_weapons = ["Great Sword", "Warhammer", "Battle Axe", "Crossbow"]
        is_bulky = weapon_type in bulky_weapons

        # PDF: Ranged weapons use DEX (Shooting Bonus) instead of STR (Attack Bonus)
        ranged_weapons = ["Bow", "Crossbow"]
        if weapon_type in ranged_weapons and 'ranged' not in modifiers:
            modifiers.append('ranged')

        return Item(
            name=name,
            item_type=ItemType.WEAPON,
            slot=ItemSlot.WEAPON,
            rarity=rarity,
            value=value,
            damage_die=base_damage,
            attack_bonus=attack_bonus,
            modifiers=modifiers,
            is_bulky=is_bulky,
            description=f"A {rarity.display_name} weapon. Damage: {base_damage}+{attack_bonus}"
        )

    @classmethod
    def generate_armor(cls, tier: int = 1, rarity: Optional[ItemRarity] = None,
                       armor_slot: ItemSlot = ItemSlot.ARMOR) -> Item:
        """
        Generate armor/helmet/shield with stats scaled by tier and rarity.

        Args:
            tier: Dungeon/enemy tier (1-4)
            rarity: Optional fixed rarity
            armor_slot: ARMOR, HELMET, or SHIELD

        Returns:
            Generated armor Item
        """
        if rarity is None:
            rarity = cls._roll_rarity(tier)

        # Choose armor type based on slot
        if armor_slot == ItemSlot.ARMOR:
            armor_type = random.choice(cls.ARMOR_TYPES)
            base_ac = 2
        elif armor_slot == ItemSlot.HELMET:
            armor_type = random.choice(cls.HELMET_TYPES)
            base_ac = 1
        elif armor_slot == ItemSlot.SHIELD:
            armor_type = random.choice(cls.SHIELD_TYPES)
            base_ac = 1
        else:
            armor_type = "Armor"
            base_ac = 1

        # Scale AC by tier and rarity
        ac_bonus = base_ac + (tier - 1) + cls._get_bonus_by_rarity(rarity)

        # Modifiers for higher rarities
        modifiers = []
        if rarity.tier >= ItemRarity.RARE.tier:
            modifiers.append(random.choice(["durability", "armor_pierce_resist", "luck"]))

        # Build name
        name = cls._build_item_name(armor_type, rarity, ac_bonus, modifiers)

        # Value
        value = (8 + tier * 4) * (rarity.tier + 1)

        # PDF: Mark bulky armor (Chain Mail, Plate Mail)
        bulky_armor = ["Chain Mail", "Scale Mail", "Plate Mail"]
        is_bulky = armor_type in bulky_armor

        return Item(
            name=name,
            item_type=ItemType.ARMOR if armor_slot == ItemSlot.ARMOR else
            (ItemType.HELMET if armor_slot == ItemSlot.HELMET else ItemType.SHIELD),
            slot=armor_slot,
            rarity=rarity,
            value=value,
            ac_bonus=ac_bonus,
            modifiers=modifiers,
            is_bulky=is_bulky,
            description=f"A {rarity.display_name} piece of protective gear. AC +{ac_bonus}"
        )

    @classmethod
    def generate_consumable(cls, tier: int = 1) -> Item:
        """Generate a consumable item (potion, etc.)"""
        consumable_name, effect_type, healing, duration = random.choice(cls.CONSUMABLE_TYPES)

        # Scale healing by tier
        if healing > 0:
            healing = healing + (tier - 1) * 10

        value = 10 + tier * 5

        return Item(
            name=consumable_name,
            item_type=ItemType.CONSUMABLE,
            slot=ItemSlot.NONE,
            rarity=ItemRarity.COMMON,
            value=value,
            healing_amount=healing,
            effect_duration=duration,
            effect_type=effect_type,
            description=f"A consumable item. {effect_type.replace('_', ' ').title()}"
        )

    @classmethod
    def generate_spell_scroll(cls, tier: int = 1) -> Item:
        """
        Generate a spell scroll (PDF system).
        PDF Rules:
        - Anyone can attempt to cast from scroll via WIL Check
        - Scroll burns after attempt (success or fail)
        - Success causes Fatigue, failure causes d6 damage
        """
        scroll_name, effect_type, description = random.choice(cls.SPELL_SCROLLS)

        # Value increases with tier
        value = 15 + tier * 10

        return Item(
            name=scroll_name,
            item_type=ItemType.CONSUMABLE,
            slot=ItemSlot.NONE,
            rarity=ItemRarity.UNCOMMON if tier <= 2 else ItemRarity.RARE,
            value=value,
            effect_type=effect_type,
            description=description
        )

    @classmethod
    def generate_random_loot(cls, tier: int = 1) -> Item:
        """Generate random loot appropriate for the tier"""
        roll = random.random()

        if roll < 0.35:  # 35% weapon
            return cls.generate_weapon(tier)
        elif roll < 0.60:  # 25% armor
            slot = random.choice([ItemSlot.ARMOR, ItemSlot.HELMET, ItemSlot.SHIELD])
            return cls.generate_armor(tier, armor_slot=slot)
        elif roll < 0.80:  # 20% consumable
            return cls.generate_consumable(tier)
        else:  # 20% spell scroll (PDF system)
            return cls.generate_spell_scroll(tier)

    @classmethod
    def _roll_rarity(cls, tier: int) -> ItemRarity:
        """Roll for item rarity based on tier"""
        roll = random.random()

        # Tier 1: Mostly common/uncommon
        if tier == 1:
            if roll < 0.6:
                return ItemRarity.COMMON
            elif roll < 0.9:
                return ItemRarity.UNCOMMON
            else:
                return ItemRarity.RARE

        # Tier 2: More uncommon/rare
        elif tier == 2:
            if roll < 0.3:
                return ItemRarity.COMMON
            elif roll < 0.6:
                return ItemRarity.UNCOMMON
            elif roll < 0.9:
                return ItemRarity.RARE
            else:
                return ItemRarity.EPIC

        # Tier 3: Rare/Epic focus
        elif tier == 3:
            if roll < 0.2:
                return ItemRarity.UNCOMMON
            elif roll < 0.5:
                return ItemRarity.RARE
            elif roll < 0.9:
                return ItemRarity.EPIC
            else:
                return ItemRarity.LEGENDARY

        # Tier 4: Epic/Legendary focus
        else:
            if roll < 0.3:
                return ItemRarity.RARE
            elif roll < 0.6:
                return ItemRarity.EPIC
            else:
                return ItemRarity.LEGENDARY

    @classmethod
    def _get_bonus_by_rarity(cls, rarity: ItemRarity) -> int:
        """Get stat bonus range by rarity"""
        if rarity == ItemRarity.COMMON:
            return random.randint(0, 1)
        elif rarity == ItemRarity.UNCOMMON:
            return random.randint(1, 2)
        elif rarity == ItemRarity.RARE:
            return random.randint(2, 4)
        elif rarity == ItemRarity.EPIC:
            return random.randint(4, 6)
        else:  # LEGENDARY
            return random.randint(6, 10)

    @classmethod
    def _upgrade_damage_die(cls, damage_die: str) -> str:
        """Upgrade damage die to next tier"""
        upgrades = {
            "1d4": "1d6",
            "1d6": "1d8",
            "1d8": "1d10",
            "1d10": "1d12",
            "1d12": "2d6",
            "2d6": "2d8",
            "2d8": "2d10",
        }
        return upgrades.get(damage_die, damage_die)

    @classmethod
    def _build_item_name(cls, base_name: str, rarity: ItemRarity,
                         bonus: int, modifiers: List[str]) -> str:
        """Build procedural item name with prefix/suffix"""
        name_parts = []

        # Prefix for higher rarities
        if rarity.tier >= ItemRarity.UNCOMMON.tier:
            if "weapon" in base_name.lower() or any(
                    w in base_name for w in ["Sword", "Axe", "Mace", "Dagger", "Spear", "Bow"]):
                prefix = random.choice(cls.WEAPON_PREFIXES)
            else:
                prefix = random.choice(cls.ARMOR_PREFIXES)
            name_parts.append(prefix)

        name_parts.append(base_name)

        # Add bonus if significant
        if bonus > 0:
            name_parts.append(f"+{bonus}")

        # Suffix for rare+
        if rarity.tier >= ItemRarity.RARE.tier and modifiers:
            suffix = random.choice(cls.SUFFIXES)
            name_parts.append(suffix)

        return " ".join(name_parts)
