"""
Dungeon Generator for RPG Game
Uses dungeon tables to generate procedural dungeons
"""

import random
import re

from tables import dungeon_tables
from tables.table_roller import roll_on_table, roll_d6
from generators.item import Item, ItemGenerator, ItemType, ItemSlot, ItemRarity


def select_denizen_table(tier: int) -> dict:
    """
    Select appropriate DENIZEN table based on tier and d6 roll.

    Args:
        tier: Monster tier (1 or 2)

    Returns:
        Selected DENIZEN table dictionary
    """
    range_roll = roll_d6()

    if tier == 1:
        if range_roll <= 2:
            return dungeon_tables.DENIZEN_TIER_1_RANGE_1_2
        elif range_roll <= 4:
            return dungeon_tables.DENIZEN_TIER_1_RANGE_3_4
        else:  # 5-6
            return dungeon_tables.DENIZEN_TIER_1_RANGE_5_6
    else:  # tier 2
        if range_roll <= 2:
            return dungeon_tables.DENIZEN_TIER_2_RANGE_1_2
        else:  # 3-6
            return dungeon_tables.DENIZEN_TIER_2_RANGE_3_5


# Handle dice expressions for coins/gems
# Pattern: "3d6 Gold", "d6 Gems"
def handle_dice_expressions(treasure_str: str):
    dice_match = re.match(r'(\d*)d(\d+)(?:x(\d+))?\s*(\w+)', treasure_str, re.IGNORECASE)
    if dice_match:
        num_dice = int(dice_match.group(1)) if dice_match.group(1) else 1
        die_size = int(dice_match.group(2))
        multiplier = int(dice_match.group(3)) if dice_match.group(3) else 1
        item_type = dice_match.group(4).lower()

        total = sum(random.randint(1, die_size) for _ in range(num_dice)) * multiplier
        return total, item_type


def get_gem_data(total=None):
    gem_value = total * random.randint(10, 50)
    gem_types = ["Ruby", "Sapphire", "Emerald", "Diamond", "Amethyst", "Topaz"]
    gem_name = random.choice(gem_types) if total == 1 else f"{total} Mixed Gems"
    return Item(
        name=gem_name,
        item_type=ItemType.JUNK,
        slot=ItemSlot.NONE,
        rarity=ItemRarity.UNCOMMON if total > 5 else ItemRarity.COMMON,
        value=gem_value,
        description=f"{total} precious gem(s) worth {gem_value} gold total"
    )


def parse_treasure_to_item(treasure_string: str, tier: int = 1) -> Item:
    """
    Parse a treasure string from TREASURE_B table and generate an actual Item object.

    Args:
        treasure_string: String from TREASURE_B table (e.g., "d100 Silver", "Artifact", "Ring")
        tier: Dungeon tier for scaling item quality

    Returns:
        Generated Item object
    """
    treasure_lower = treasure_string.lower().strip()

    # Handle "Artifact" - generate a high-tier epic/legendary item
    if treasure_lower == "artifact":
        return ItemGenerator.generate_random_loot(tier=max(2, tier))

    # Handle "Ring" - generate an armor piece (shield slot represents accessory)
    elif treasure_lower == "ring":
        rarity = ItemRarity.RARE if random.random() < 0.7 else ItemRarity.EPIC
        ring = ItemGenerator.generate_armor(tier=tier, rarity=rarity, armor_slot=ItemSlot.SHIELD)
        # Rename to be a ring
        ring.name = ring.name.replace("Shield", "Ring").replace("Buckler", "Ring")
        ring.description = f"A magical {rarity.display_name} ring. AC +{ring.ac_bonus}"
        return ring

    # Handle "Potion" - generate a consumable
    elif treasure_lower == "potion":
        return ItemGenerator.generate_consumable(tier=tier)

    # Handle dice expressions for coins/gems
    # Pattern: "d100 Silver", "3d6x100 Gold", "d20 Gems"
    total, item_type = handle_dice_expressions(treasure_string)

    # Create appropriate item based on type
    if "silver" in item_type:
        # Convert silver to gold value (10 silver = 1 gold)
        gold_value = total // 10
        return Item(
            name=f"{total} Silver Coins",
            item_type=ItemType.JUNK,
            slot=ItemSlot.NONE,
            rarity=ItemRarity.COMMON,
            value=gold_value,
            description=f"A pouch containing {total} silver coins (worth {gold_value} gold)"
        )

    elif "gold" in item_type:
        return Item(
            name=f"{total} Gold Coins",
            item_type=ItemType.JUNK,
            slot=ItemSlot.NONE,
            rarity=ItemRarity.COMMON,
            value=total,
            description=f"A pouch containing {total} gold coins"
        )

    elif "gem" in item_type:
        get_gem_data(total)

    # Fallback: create a generic treasure item
    return Item(
        name=f"Treasure: {treasure_string}",
        item_type=ItemType.JUNK,
        slot=ItemSlot.NONE,
        rarity=ItemRarity.COMMON,
        value=50,
        description=treasure_string
    )


def parse_treasure_a_to_item(treasure_string: str, tier: int = 1) -> Item:
    """
    Parse a treasure string from TREASURE_A table and generate an actual Item object.

    TREASURE_A table:
    1: "Weapon"
    2: "3d6 Gold"
    3: "d6 Gems"
    4: "Potion"
    5: "Artifact"
    6: "Scroll"

    Args:
        treasure_string: String from TREASURE_A table (e.g., "Weapon", "3d6 Gold", "Scroll")
        tier: Dungeon tier for scaling item quality

    Returns:
        Generated Item object
    """
    treasure_lower = treasure_string.lower().strip()

    # Handle "Weapon" - generate a random weapon
    if treasure_lower == "weapon":
        rarity = ItemRarity.UNCOMMON if random.random() < 0.6 else ItemRarity.RARE
        return ItemGenerator.generate_weapon(tier=tier, rarity=rarity)

    # Handle "Artifact" - generate a high-tier epic/legendary item
    elif treasure_lower == "artifact":
        return ItemGenerator.generate_random_loot(tier=max(2, tier))

    # Handle "Potion" - generate a consumable
    elif treasure_lower == "potion":
        return ItemGenerator.generate_consumable(tier=tier)

    # Handle "Scroll" - generate a spell scroll
    elif treasure_lower == "scroll":
        return ItemGenerator.generate_spell_scroll(tier=tier)

    # Handle dice expressions for coins/gems
    # Pattern: "3d6 Gold", "d6 Gems"
    total, item_type = handle_dice_expressions(treasure_string)
    # Create appropriate item based on type
    if "gold" in item_type:
        return Item(
            name=f"{total} Gold Coins",
            item_type=ItemType.JUNK,
            slot=ItemSlot.NONE,
            rarity=ItemRarity.COMMON,
            value=total,
            description=f"A pouch containing {total} gold coins"
        )

    elif "gem" in item_type:
        get_gem_data(total)

    # Fallback: create a generic treasure item
    return Item(
        name=f"Treasure: {treasure_string}",
        item_type=ItemType.JUNK,
        slot=ItemSlot.NONE,
        rarity=ItemRarity.COMMON,
        value=50,
        description=treasure_string
    )


class DungeonRoom:
    """Represents a single room or corridor in the dungeon grid"""

    def __init__(self, x, y, room_type="room", shape=None, entrance_pattern=None):
        """
        Initialize a dungeon room.

        Args:
            x (int): X coordinate on grid
            y (int): Y coordinate on grid
            room_type (str): "entrance", "room", or "corridor"
            shape (int): Shape pattern from PDF (1-6)
            entrance_pattern (int): Entrance pattern if this is entrance (1-6)
        """
        self.x = x
        self.y = y
        self.room_type = room_type
        self.shape = shape
        self.entrance_pattern = entrance_pattern

        # Room properties
        self.explored = False
        self.contents = {}
        self.doors = {}  # Direction -> {"type": "unlocked/stuck/locked/trapped", "to_room": (x, y)}
        self.exits = []  # Available directions: "north", "south", "east", "west"

        # Room dimensions (for multi-square rooms)
        self.width = 1
        self.height = 1

        # Room contents from tables
        self.monsters = []
        self.treasure = []
        self.features = []
        self.dressing = []
        self.is_special = False

    def add_door(self, direction, door_type, to_coords):
        """Add a door in the specified direction"""
        self.doors[direction] = {
            "type": door_type,
            "to_room": to_coords
        }
        if direction not in self.exits:
            self.exits.append(direction)

    def add_exit(self, direction):
        """Add an available exit direction"""
        if direction not in self.exits:
            self.exits.append(direction)

    def explore(self):
        """Mark room as explored"""
        self.explored = True

    def to_dict(self):
        """Convert room to dictionary"""
        # Serialize monsters properly
        from generators.monster import Monster
        monsters_data = []
        for monster in self.monsters:
            if isinstance(monster, Monster):
                monsters_data.append(monster.to_dict())
            else:
                # Backward compatibility for dict monsters
                monsters_data.append(monster)

        return {
            "x": self.x,
            "y": self.y,
            "room_type": self.room_type,
            "shape": self.shape,
            "entrance_pattern": self.entrance_pattern,
            "explored": self.explored,
            "contents": self.contents,
            "doors": self.doors,
            "exits": self.exits,
            "width": self.width,
            "height": self.height,
            "monsters": monsters_data,
            "treasure": self.treasure,
            "features": self.features,
            "dressing": self.dressing,
            "is_special": self.is_special
        }

    @classmethod
    def from_dict(cls, data):
        """Create DungeonRoom from dictionary"""
        room = cls(
            data["x"],
            data["y"],
            data.get("room_type", "room"),
            data.get("shape"),
            data.get("entrance_pattern")
        )
        room.explored = data.get("explored", False)
        room.contents = data.get("contents", {})
        room.doors = data.get("doors", {})
        room.exits = data.get("exits", [])
        room.width = data.get("width", 1)
        room.height = data.get("height", 1)

        # Deserialize monsters from dicts to Monster objects
        from generators.monster import Monster
        room.monsters = []
        for monster_data in data.get("monsters", []):
            if isinstance(monster_data, dict) and "name" in monster_data:
                room.monsters.append(Monster.from_dict(monster_data))
            else:
                # Backward compatibility
                room.monsters.append(monster_data)

        room.treasure = data.get("treasure", [])
        room.features = data.get("features", [])
        room.dressing = data.get("dressing", [])
        room.is_special = data.get("is_special", False)
        return room

    def __str__(self):
        return f"{self.room_type.capitalize()} at ({self.x}, {self.y})"

    def __repr__(self):
        return f"DungeonRoom(x={self.x}, y={self.y}, type='{self.room_type}')"


class DungeonGrid:
    """Manages the spatial layout of a dungeon on a square grid"""

    def __init__(self, dungeon):
        """
        Initialize dungeon grid.

        Args:
            dungeon (Dungeon): The dungeon metadata object
        """
        self.dungeon = dungeon
        self.rooms = {}  # (x, y) -> DungeonRoom
        self.entrance_pos = None
        self.player_pos = None
        self.rooms_generated = 0

        # Direction vectors for grid movement
        self.directions = {
            "north": (0, 1),
            "south": (0, -1),
            "east": (1, 0),
            "west": (-1, 0)
        }

        # Opposite directions for backtracking
        self.opposite_dir = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }

        # Generate entrance
        self.generate_entrance()

    def generate_entrance(self):
        """Generate entrance room with pattern from PDF (1-6)"""
        entrance_pattern = roll_d6()
        entrance_room = DungeonRoom(0, 0, room_type="entrance", entrance_pattern=entrance_pattern)

        # Set up entrance based on pattern
        # Each pattern has different available exits
        if entrance_pattern == 1:  # Single entrance with small room
            entrance_room.exits = ["north"]
            entrance_room.width = 1
            entrance_room.height = 1
        elif entrance_pattern == 2:  # L-shaped entrance
            entrance_room.exits = ["north", "east"]
            entrance_room.width = 2
            entrance_room.height = 2
        elif entrance_pattern == 3:  # Entrance with side alcove
            entrance_room.exits = ["north", "west"]
            entrance_room.width = 2
            entrance_room.height = 1
        elif entrance_pattern == 4:  # L-shaped with offset
            entrance_room.exits = ["north", "east"]
            entrance_room.width = 2
            entrance_room.height = 2
        elif entrance_pattern == 5:  # T-junction entrance
            entrance_room.exits = ["north", "east", "west"]
            entrance_room.width = 3
            entrance_room.height = 1
        elif entrance_pattern == 6:  # Straight entrance with side room
            entrance_room.exits = ["north", "east"]
            entrance_room.width = 2
            entrance_room.height = 2

        entrance_room.explore()
        entrance_room.contents["type"] = "Entrance"
        self.rooms[(0, 0)] = entrance_room
        self.entrance_pos = (0, 0)
        self.player_pos = (0, 0)
        self.rooms_generated = 1

    def get_room(self, x, y):
        """Get room at coordinates"""
        return self.rooms.get((x, y))

    def get_current_room(self):
        """Get the room where player currently is"""
        if self.player_pos:
            return self.rooms.get(self.player_pos)
        return None

    def get_adjacent_pos(self, x, y, direction):
        """Get coordinates of adjacent position in direction"""
        dx, dy = self.directions.get(direction, (0, 0))
        return x + dx, y + dy

    def can_move(self, direction):
        """Check if player can move in direction"""
        current_room = self.get_current_room()
        if not current_room:
            return False

        return direction in current_room.exits

    def move_player(self, direction):
        """
        Move player in direction, generating new room if needed.

        Args:
            direction (str): Direction to move ("north", "south", "east", "west")

        Returns:
            DungeonRoom: The room moved to, or None if move invalid
        """
        current_room = self.get_current_room()
        if not current_room or not self.can_move(direction):
            return None

        # Get target position
        new_x, new_y = self.get_adjacent_pos(current_room.x, current_room.y, direction)

        # Check if room already exists
        if (new_x, new_y) in self.rooms:
            self.player_pos = (new_x, new_y)
            target_room = self.rooms[(new_x, new_y)]
            target_room.explore()
            return target_room

        # Generate new room/corridor
        if self.rooms_generated < self.dungeon.total_rooms:
            new_room = self.generate_room_or_corridor(new_x, new_y, direction)

            # Add door connection between current and new room
            door_type = roll_on_table(dungeon_tables.DOOR)
            current_room.add_door(direction, door_type, (new_x, new_y))
            new_room.add_door(self.opposite_dir[direction], door_type, (current_room.x, current_room.y))

            # Move player
            self.player_pos = (new_x, new_y)
            new_room.explore()

            # Populate room contents
            self.populate_room_contents(new_room)

            return new_room

        return None

    def generate_room_or_corridor(self, x, y, from_direction):
        """
        Generate a room or corridor at position.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            from_direction (str): Direction we're coming from

        Returns:
            DungeonRoom: Generated room or corridor
        """
        # Roll 1d6: 1-2 = corridor, 3-6 = room
        roll = roll_d6()

        if roll <= 2:
            # Generate corridor (1 square wide)
            room = self.generate_corridor(x, y, from_direction)
        else:
            # Generate room
            room = self.generate_room(x, y, from_direction)

        self.rooms[(x, y)] = room
        self.rooms_generated += 1

        return room

    def generate_corridor(self, x, y, from_direction):
        """Generate a corridor (1 square wide, straight line)"""
        corridor = DungeonRoom(x, y, room_type="corridor", shape=1)
        corridor.width = 1
        corridor.height = 1

        # Corridors typically continue straight and/or branch
        # Always has exit back where we came from
        corridor.add_exit(self.opposite_dir[from_direction])

        # 50% chance to continue straight
        if random.random() < 0.5:
            corridor.add_exit(from_direction)

        # 25% chance to branch left/right
        perpendicular = self.get_perpendicular_directions(from_direction)
        if random.random() < 0.25:
            corridor.add_exit(perpendicular[0])
        if random.random() < 0.25:
            corridor.add_exit(perpendicular[1])

        return corridor

    def generate_room(self, x, y, from_direction):
        """Generate a room with shape from PDF patterns"""
        # Roll for room shape (1-6)
        shape = roll_d6()
        room = DungeonRoom(x, y, room_type="room", shape=shape)

        # Set room properties based on shape
        # These match the PDF patterns
        if shape == 1:  # Simple square room
            room.width = 2
            room.height = 2
            room.exits = [self.opposite_dir[from_direction], from_direction]
            if random.random() < 0.5:
                room.exits.append(random.choice(self.get_perpendicular_directions(from_direction)))

        elif shape == 2:  # Rectangular room with alcove
            room.width = 3
            room.height = 2
            room.exits = [self.opposite_dir[from_direction], from_direction]
            room.exits.append(random.choice(self.get_perpendicular_directions(from_direction)))

        elif shape == 3:  # Round/circular room
            room.width = 2
            room.height = 2
            room.exits = [self.opposite_dir[from_direction]]
            # Circular rooms have exits in multiple directions
            for direction in ["north", "south", "east", "west"]:
                if direction != self.opposite_dir[from_direction] and random.random() < 0.4:
                    room.exits.append(direction)

        elif shape == 4:  # Circular room with projections
            room.width = 3
            room.height = 3
            room.exits = [self.opposite_dir[from_direction]]
            # Multiple exits
            for direction in ["north", "south", "east", "west"]:
                if direction != self.opposite_dir[from_direction] and random.random() < 0.5:
                    room.exits.append(direction)

        elif shape == 5:  # Angular multi-exit room
            room.width = 2
            room.height = 2
            room.exits = [self.opposite_dir[from_direction]]
            # Guaranteed multiple exits
            perpendicular = self.get_perpendicular_directions(from_direction)
            room.exits.extend(perpendicular)
            if random.random() < 0.5:
                room.exits.append(from_direction)

        elif shape == 6:  # Small rectangular room
            room.width = 2
            room.height = 1
            room.exits = [self.opposite_dir[from_direction]]
            if random.random() < 0.3:
                room.exits.append(random.choice(self.get_perpendicular_directions(from_direction)))

        return room

    @staticmethod
    def get_perpendicular_directions(direction):
        """Get perpendicular directions to given direction"""
        if direction in ["north", "south"]:
            return ["east", "west"]
        else:
            return ["north", "south"]

    def populate_room_contents(self, room):
        """Populate room with contents using dungeon tables"""
        # Determine if this is a special room
        special_rooms_placed = sum(1 for r in self.rooms.values() if r.is_special)
        if special_rooms_placed < self.dungeon.special_rooms_count:
            # Chance to make this a special room
            if random.random() < 0.3:
                room.is_special = True

        # Roll for room contents based on type
        if room.room_type == "corridor":
            contents_roll = roll_on_table(dungeon_tables.CORRIDOR)
        else:
            contents_roll = roll_on_table(dungeon_tables.ROOM)

        room.contents["type"] = contents_roll

        # Populate based on contents type
        if contents_roll == "Spoor":
            room.contents["spoor"] = roll_on_table(dungeon_tables.SPOOR)

        elif contents_roll == "Discovery":
            discovery_type = roll_on_table(dungeon_tables.DISCOVERY)
            room.contents["discovery"] = discovery_type

            if discovery_type == "Special Room 1":
                room.is_special = True
                room.contents["special"] = roll_on_table(dungeon_tables.SPECIAL_ROOM_1)
            elif discovery_type == "Special Room 2":
                room.is_special = True
                room.contents["special"] = roll_on_table(dungeon_tables.SPECIAL_ROOM_2)
            elif discovery_type == "Feature":
                room.features.append(roll_on_table(dungeon_tables.FEATURE))
            elif discovery_type == "Item":
                room.contents["item"] = roll_on_table(dungeon_tables.ITEM)
            elif discovery_type.startswith("Treasure"):
                if "A" in discovery_type:
                    # Treasure A: parse and generate actual Item object
                    treasure_string = roll_on_table(dungeon_tables.TREASURE_A)
                    treasure_item = parse_treasure_a_to_item(treasure_string, tier=1)
                    # Store as serialized dict for persistence
                    room.treasure.append(treasure_item.to_dict())
                else:
                    # Treasure B: parse and generate actual Item object
                    treasure_string = roll_on_table(dungeon_tables.TREASURE_B)
                    treasure_item = parse_treasure_to_item(treasure_string, tier=1)
                    # Store as serialized dict for persistence
                    room.treasure.append(treasure_item.to_dict())

        elif contents_roll == "Danger":
            danger_type = roll_on_table(dungeon_tables.DANGER)
            room.contents["danger"] = danger_type

            if danger_type == "Hazard":
                room.contents["hazard"] = roll_on_table(dungeon_tables.HAZARD)
            elif danger_type == "Trap":
                room.contents["trap"] = roll_on_table(dungeon_tables.TRAP)
            elif danger_type == "Encounter":
                encounter_text = roll_on_table(dungeon_tables.DUNGEON_ENCOUNTERS)
                room.contents["encounter"] = encounter_text

                # 50% chance encounter spawns monsters
                if random.random() < 0.5:
                    from generators.monster import Monster, roll_number_appearing

                    # Use tier 1 monsters for encounters
                    tier = 1
                    denizen_table = select_denizen_table(tier)
                    roll_2d6 = roll_d6() + roll_d6()
                    monster_data = denizen_table.get(roll_2d6, denizen_table[7])

                    # 1-2 monsters
                    num_appearing = random.randint(1, 2)
                    for i in range(num_appearing):
                        monster = Monster.from_table_entry(monster_data)
                        if num_appearing > 1:
                            monster.name = f"{monster.name} #{i + 1}"
                        room.monsters.append(monster)
                    room.contents["encounter_has_monsters"] = True

                # 30% chance encounter has reward treasure
                elif random.random() < 0.3:
                    treasure_string = roll_on_table(dungeon_tables.TREASURE_A)
                    treasure_item = parse_treasure_a_to_item(treasure_string, tier=1)
                    room.treasure.append(treasure_item.to_dict())
                    room.contents["encounter_has_treasure"] = True
            elif danger_type.startswith("Monster"):
                # Determine tier based on dungeon depth and create Monster instances
                from generators.monster import Monster, roll_number_appearing

                # Determine tier
                tier = 1 if "Tier 1" in danger_type or "(T1)" in danger_type else 2

                # Select DENIZEN table based on tier and d6 roll
                denizen_table = select_denizen_table(tier)

                # Roll 2d6 on the selected table to get monster
                roll_2d6 = roll_d6() + roll_d6()
                monster_data = denizen_table.get(roll_2d6)

                # Fallback if roll not in table (shouldn't happen with 2d6 on 2-12 table)
                if not monster_data:
                    monster_data = denizen_table[7]  # Use middle result as fallback

                # Roll for number appearing (1-2 for tier 1, 1 for tier 2)
                num_appearing = roll_number_appearing(tier, solo_pc=True)

                # Create multiple monster instances
                for i in range(num_appearing):
                    monster = Monster.from_table_entry(monster_data)
                    if num_appearing > 1:
                        monster.name = f"{monster.name} #{i + 1}"
                    room.monsters.append(monster)

        # Add room dressing
        if random.random() < 0.4:  # 40% chance of dressing
            dressing_types = ["DRESSING_NATURAL", "DRESSING_MAN_MADE", "DRESSING_LIGHTING",
                              "DRESSING_ODOR", "DRESSING_ODD", "DRESSING_MYSTICAL"]
            dressing_type = random.choice(dressing_types)
            dressing_table = getattr(dungeon_tables, dressing_type)
            room.dressing.append(roll_on_table(dressing_table))

    def to_dict(self):
        """Convert grid to dictionary"""
        return {
            "rooms": {f"{x},{y}": room.to_dict() for (x, y), room in self.rooms.items()},
            "entrance_pos": self.entrance_pos,
            "player_pos": self.player_pos,
            "rooms_generated": self.rooms_generated
        }

    @classmethod
    def from_dict(cls, data, dungeon):
        """Create DungeonGrid from dictionary"""
        grid = cls.__new__(cls)
        grid.dungeon = dungeon
        grid.entrance_pos = tuple(data["entrance_pos"]) if data["entrance_pos"] else None
        grid.player_pos = tuple(data["player_pos"]) if data["player_pos"] else None
        grid.rooms_generated = data.get("rooms_generated", 0)

        # Restore rooms
        grid.rooms = {}
        for key, room_data in data["rooms"].items():
            x, y = map(int, key.split(","))
            grid.rooms[(x, y)] = DungeonRoom.from_dict(room_data)

        # Initialize directions
        grid.directions = {
            "north": (0, 1),
            "south": (0, -1),
            "east": (1, 0),
            "west": (-1, 0)
        }
        grid.opposite_dir = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east"
        }

        return grid


class Dungeon:
    """Represents a generated dungeon"""

    def __init__(self, theme=None, dungeon_type=None, adjective=None, noun=None,
                 size=None, special_rooms_count=None, builder=None, purpose=None, destruction=None):
        """
        Initialize a dungeon.

        Args:
            theme (str, optional): Dungeon theme
            dungeon_type (str, optional): Dungeon type
            adjective (str, optional): Adjective for name
            noun (str, optional): Noun for name
            size (str, optional): Size description (e.g., "2d6+2 Rooms")
            special_rooms_count (int, optional): Number of special rooms
            builder (str, optional): Who built the dungeon
            purpose (str, optional): Original purpose
            destruction (str, optional): What caused its downfall
        """
        # Generate dungeon name components
        self.theme = theme if theme else roll_on_table(dungeon_tables.THEME)
        self.dungeon_type = dungeon_type if dungeon_type else roll_on_table(dungeon_tables.DUNGEON_TYPE)

        # Roll for adjective: 1-3 use ADJECTIVE_1, 4-6 use ADJECTIVE_2
        if adjective:
            self.adjective = adjective
        else:
            adj_roll = roll_d6()
            if adj_roll <= 3:
                self.adjective = roll_on_table(dungeon_tables.ADJECTIVE_1)
            else:
                self.adjective = roll_on_table(dungeon_tables.ADJECTIVE_2)

        # Roll for noun: 1-3 use NOUN_1, 4-6 use NOUN_2
        if noun:
            self.noun = noun
        else:
            noun_roll = roll_d6()
            if noun_roll <= 3:
                self.noun = roll_on_table(dungeon_tables.NOUN_1)
            else:
                self.noun = roll_on_table(dungeon_tables.NOUN_2)

        # Generate dungeon attributes
        self.size = size if size else roll_on_table(dungeon_tables.SIZE)
        self.special_rooms_count = special_rooms_count if special_rooms_count else roll_on_table(
            dungeon_tables.SPECIAL_ROOMS_COUNT
        )
        self.builder = builder if builder else roll_on_table(dungeon_tables.BUILDER)
        self.purpose = purpose if purpose else roll_on_table(dungeon_tables.PURPOSE)
        self.destruction = destruction if destruction else roll_on_table(dungeon_tables.DESTRUCTION)

        # Dungeon state (for exploration)
        self.entered = False
        self.completed = False
        self.current_room = 0
        self.total_rooms = self._calculate_room_count()
        self.explored_rooms = []

        # Dungeon grid (spatial layout)
        self.grid = None

    @property
    def name(self):
        """Generate the full dungeon name"""
        return f"{self.theme} {self.dungeon_type} of {self.adjective} {self.noun}"

    def _calculate_room_count(self):
        """Calculate actual number of rooms from size description"""
        # Parse size string like "2d6+2 Rooms"
        import re
        match = re.match(r'(\d+)d(\d+)\+(\d+)', self.size)
        if match:
            num_dice = int(match.group(1))
            die_size = int(match.group(2))
            modifier = int(match.group(3))
            # Roll dice
            total = sum(roll_d6() for _ in range(num_dice))
            # Clamp to die size * num_dice
            total = min(total, die_size * num_dice)
            return total + modifier
        return 5  # Default fallback

    def enter(self):
        """Mark dungeon as entered and initialize grid"""
        self.entered = True
        self.current_room = 0
        # Initialize dungeon grid with entrance
        if self.grid is None:
            self.grid = DungeonGrid(self)

    def advance_room(self):
        """Move to next room"""
        if self.current_room < self.total_rooms:
            self.current_room += 1
            return True
        return False

    def complete(self):
        """Mark dungeon as completed"""
        self.completed = True

    def get_current_grid_room(self):
        """Get the current room from the grid"""
        if self.grid:
            return self.grid.get_current_room()
        return None

    def move_in_direction(self, direction):
        """
        Move player in direction within dungeon grid.

        Args:
            direction (str): Direction to move ("north", "south", "east", "west")

        Returns:
            DungeonRoom: Room moved to, or None if invalid
        """
        if self.grid:
            room = self.grid.move_player(direction)
            if room:
                self.current_room = self.grid.rooms_generated
            return room
        return None

    def get_available_exits(self):
        """Get list of available exits from current room"""
        current_room = self.get_current_grid_room()
        if current_room:
            return current_room.exits
        return []

    def get_room_description(self):
        """Get detailed description of current room"""
        room = self.get_current_grid_room()
        if not room:
            return "You are not in the dungeon."

        description = []

        # Room type and basic info
        if room.room_type == "entrance":
            description.append(f"You are at the entrance to the {self.name}.")
            description.append(f"Entrance Pattern: {room.entrance_pattern}")
        elif room.room_type == "corridor":
            description.append("You are in a narrow corridor.")
        else:
            description.append(f"You are in a {room.width}x{room.height} room (Shape {room.shape}).")

        # Special room
        if room.is_special:
            description.append("[SPECIAL ROOM]")
            if "special" in room.contents:
                description.append(f"Special: {room.contents['special']}")

        # Contents
        if room.contents.get("type"):
            description.append(f"\nContents: {room.contents['type']}")

            if room.contents.get("spoor"):
                description.append(f"  Spoor: {room.contents['spoor']}")

            if room.contents.get("discovery"):
                description.append(f"  Discovery: {room.contents['discovery']}")
                if room.features:
                    description.append(f"  Features: {', '.join(room.features)}")
                if room.treasure:
                    description.append(f"  Treasure: {', '.join(room.treasure)}")
                if room.contents.get("item"):
                    description.append(f"  Item: {room.contents['item']}")

            if room.contents.get("danger"):
                description.append(f"  Danger: {room.contents['danger']}")
                if room.contents.get("hazard"):
                    description.append(f"  Hazard: {room.contents['hazard']}")
                if room.contents.get("trap"):
                    description.append(f"  Trap: {room.contents['trap']}")
                if room.contents.get("encounter"):
                    description.append(f"  Encounter: {room.contents['encounter']}")
                if room.monsters:
                    description.append(f"  Monsters: {', '.join(room.monsters)}")

        # Dressing
        if room.dressing:
            description.append(f"\nRoom Dressing: {', '.join(room.dressing)}")

        # Exits and doors
        description.append(f"\nExits: {', '.join(room.exits) if room.exits else 'None'}")

        if room.doors:
            description.append("\nDoors:")
            for direction, door_info in room.doors.items():
                description.append(f"  {direction.capitalize()}: {door_info['type']}")

        return "\n".join(description)

    def to_dict(self):
        """Convert dungeon to dictionary"""
        data = {
            "name": self.name,
            "theme": self.theme,
            "dungeon_type": self.dungeon_type,
            "adjective": self.adjective,
            "noun": self.noun,
            "size": self.size,
            "special_rooms_count": self.special_rooms_count,
            "builder": self.builder,
            "purpose": self.purpose,
            "destruction": self.destruction,
            "entered": self.entered,
            "completed": self.completed,
            "current_room": self.current_room,
            "total_rooms": self.total_rooms,
            "explored_rooms": self.explored_rooms
        }

        # Include grid data if grid exists
        if self.grid:
            data["grid"] = self.grid.to_dict()

        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create Dungeon from dictionary.

        Args:
            data (dict): Dungeon data dictionary

        Returns:
            Dungeon: Reconstructed dungeon object
        """
        dungeon = cls(
            theme=data["theme"],
            dungeon_type=data["dungeon_type"],
            adjective=data["adjective"],
            noun=data["noun"],
            size=data["size"],
            special_rooms_count=data["special_rooms_count"],
            builder=data.get("builder"),
            purpose=data.get("purpose"),
            destruction=data.get("destruction")
        )
        dungeon.entered = data.get("entered", False)
        dungeon.completed = data.get("completed", False)
        dungeon.current_room = data.get("current_room", 0)
        dungeon.total_rooms = data["total_rooms"]
        dungeon.explored_rooms = data.get("explored_rooms", [])

        # Restore grid if present
        if "grid" in data and data["grid"]:
            dungeon.grid = DungeonGrid.from_dict(data["grid"], dungeon)

        return dungeon

    def __str__(self):
        """String representation of dungeon"""
        return f"{self.name} ({self.total_rooms} rooms)"

    def __repr__(self):
        return f"Dungeon(name='{self.name}', rooms={self.total_rooms})"


def generate_dungeon():
    """
    Generate a random dungeon.

    Returns:
        Dungeon: A generated dungeon object

    Example:
        >>> dungeon = generate_dungeon()
        >>> print(dungeon)
        Criminal Cave of Forgotten Gods (7 rooms)
    """
    return Dungeon()


def main():
    """Main function to demonstrate dungeon generation"""
    print("=" * 70)
    print("DUNGEON GENERATOR")
    print("=" * 70)
    print()

    # Generate a single dungeon
    print("Generated Dungeon:")
    print("-" * 70)
    dungeon = generate_dungeon()
    print(f"Name: {dungeon.name}")
    print(f"Theme: {dungeon.theme}")
    print(f"Type: {dungeon.dungeon_type}")
    print(f"Size: {dungeon.size} ({dungeon.total_rooms} actual rooms)")
    print(f"Special Rooms: {dungeon.special_rooms_count}")
    print(f"Builder: {dungeon.builder}")
    print(f"Purpose: {dungeon.purpose}")
    print(f"Destruction: {dungeon.destruction}")
    print()

    # Generate multiple dungeons
    print("\nMore Examples:")
    print("-" * 70)
    for i in range(5):
        dungeon = generate_dungeon()
        print(f"{i+1}. {dungeon}")


if __name__ == "__main__":
    main()
