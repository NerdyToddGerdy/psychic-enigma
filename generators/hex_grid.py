"""
Hex Grid System for Overland Exploration
Implements hex grid with axial coordinates for tracking terrain, exploration, and player movement
"""

from tables.table_roller import roll_on_table, roll_d6
from tables import overland_tables


# Direction constants (clockwise from North)
NORTH = 1
NORTHEAST = 2
SOUTHEAST = 3
SOUTH = 4
SOUTHWEST = 5
NORTHWEST = 6

DIRECTION_NAMES = {
    NORTH: "North",
    NORTHEAST: "Northeast",
    SOUTHEAST: "Southeast",
    SOUTH: "South",
    SOUTHWEST: "Southwest",
    NORTHWEST: "Northwest"
}

# Axial direction vectors for hex grid (flat-top orientation)
# Each direction moves in specific q,r coordinates
AXIAL_DIRECTIONS = {
    NORTH: (0, -1),       # North: same column, row up
    NORTHEAST: (1, -1),   # Northeast: column right, row up
    SOUTHEAST: (1, 0),    # Southeast: column right, same row
    SOUTH: (0, 1),        # South: same column, row down
    SOUTHWEST: (-1, 1),   # Southwest: column left, row down
    NORTHWEST: (-1, 0)    # Northwest: column left, same row
}


class Hex:
    """Represents a single hex on the overland map"""

    def __init__(self, q, r, terrain=None, weather=None, water=None, reference_terrain=None):
        """
        Initialize a hex with axial coordinates.

        Args:
            q (int): Column coordinate (axial q)
            r (int): Row coordinate (axial r)
            terrain (str, optional): Terrain type. If None, will be rolled.
            weather (str, optional): Weather condition. If None, will be rolled.
            water (bool, optional): Whether hex has water. If None, will be rolled.
            reference_terrain (str, optional): Reference terrain for NEW_TERRAIN table.
        """
        self.q = q
        self.r = r

        # Roll for terrain if not provided
        if terrain:
            self.terrain = terrain
        else:
            # Use terrain continuity logic with NEW_TERRAIN table
            if reference_terrain == "Village":
                # Village adjacents are completely random
                self.terrain = roll_on_table(overland_tables.TERRAIN)
            elif reference_terrain:
                # Use NEW_TERRAIN table (1-4 same, 5-6 new)
                terrain_roll = roll_on_table(overland_tables.NEW_TERRAIN)
                if terrain_roll == "Same":
                    self.terrain = reference_terrain
                else:  # "New"
                    self.terrain = roll_on_table(overland_tables.TERRAIN)
            else:
                # No reference, roll randomly
                self.terrain = roll_on_table(overland_tables.TERRAIN)

        # Roll for weather if not provided
        self.weather = weather if weather else roll_on_table(overland_tables.WEATHER)

        # Roll for water if not provided (1-2 on d6 = has water)
        if water is None:
            water_roll = roll_d6()
            self.water = water_roll <= 2
        else:
            self.water = water

        # Revealed state (visible but not explored, e.g., quest destination)
        self.revealed = False

        # Exploration status
        self.explored = False

        # Settlement status (Village or discovered settlement)
        self.is_settlement = (terrain == "Village")

        # Settlement type (Refugee, Village, Town, Outpost, City)
        # Set for starting Village, or when Settlement discovered
        self.settlement_type = "Village" if terrain == "Village" else None

        # Available vendors/services in settlement (Armorer, Inn, Merchant, Herbalist)
        # Roll when settlement is created/discovered
        self.available_vendors = []
        if self.is_settlement:
            self.available_vendors = self._roll_settlement_vendors()

        # Discoveries in this hex
        self.discoveries = []

        # Dangers in this hex
        self.dangers = []

    @property
    def coordinates(self):
        """Return coordinates as tuple"""
        return self.q, self.r

    def explore(self):
        """
        Mark hex as explored and roll for any discoveries/dangers.

        Returns:
            dict: Results of exploration (discoveries and dangers)
        """
        if self.explored:
            return {"already_explored": True, "discoveries": self.discoveries, "dangers": self.dangers}

        self.explored = True
        results = {"already_explored": False, "discoveries": [], "dangers": []}

        # Roll on EXPLORE_DIE
        explore_result = roll_on_table(overland_tables.EXPLORE_DIE)

        if explore_result == "Discovery":
            # Roll for discovery type
            discovery_type = roll_on_table(overland_tables.DISCOVERY)
            discovery_detail = self._get_discovery_detail(discovery_type)
            discovery = {"type": discovery_type, "detail": discovery_detail}
            self.discoveries.append(discovery)
            results["discoveries"].append(discovery)

            # Mark hex as settlement if Settlement discovery
            if discovery_type == "Settlement":
                self.is_settlement = True
                # Store the specific settlement type
                self.settlement_type = discovery_detail
                # Roll for available vendors
                self.available_vendors = self._roll_settlement_vendors()

        elif explore_result == "Danger":
            # Roll for danger type
            danger_type = roll_on_table(overland_tables.DANGER)
            danger_detail = self._get_danger_detail(danger_type)
            danger = {"type": danger_type, "detail": danger_detail}
            self.dangers.append(danger)
            results["dangers"].append(danger)

        elif explore_result == "Spoor":
            # Roll for spoor type
            spoor = roll_on_table(overland_tables.SPOOR)
            results["spoor"] = spoor

        return results

    @staticmethod
    def _get_discovery_detail(discovery_type):
        """Get specific discovery details based on type"""
        if discovery_type == "Natural":
            return roll_on_table(overland_tables.DISCOVERY_NATURAL)
        elif discovery_type == "Unnatural":
            return roll_on_table(overland_tables.DISCOVERY_UNNATURAL)
        elif discovery_type == "Ruin":
            return roll_on_table(overland_tables.DISCOVERY_RUIN)
        elif discovery_type == "Settlement":
            return roll_on_table(overland_tables.DISCOVERY_SETTLEMENT)
        elif discovery_type == "Evidence":
            return roll_on_table(overland_tables.DISCOVERY_EVIDENCE)
        elif discovery_type == "Passive":
            return roll_on_table(overland_tables.DISCOVERY_PASSIVE)
        return None

    @staticmethod
    def _roll_settlement_vendors():
        """
        Roll on SETTLEMENT_AVAILABLE table to determine which vendors/services exist.

        Returns:
            list: Available vendor types (e.g., ["Merchant", "Inn", "Herbalist"])
        """
        vendors = []
        # Roll 3 times on SETTLEMENT_AVAILABLE (d6 each)
        for _ in range(3):
            vendor = roll_on_table(overland_tables.SETTLEMENT_AVAILABLE)
            if vendor and vendor not in vendors:
                vendors.append(vendor)
        return vendors

    def _get_danger_detail(self, danger_type):
        """Get specific danger details based on type"""
        print(f"[HEX DEBUG] _get_danger_detail called with danger_type: {danger_type}")
        if danger_type == "Unnatural":
            # Spawn unnatural monsters (undead/demons)
            return self._spawn_unnatural_encounter()
        elif danger_type == "Hazard":
            return roll_on_table(overland_tables.DANGER_HAZARD)
        elif danger_type == "Hostile":
            # Roll for encounter and spawn monsters
            print(f"[HEX DEBUG] Calling _spawn_hostile_encounter()")
            result = self._spawn_hostile_encounter()
            print(f"[HEX DEBUG] Hostile encounter result: {result.keys() if isinstance(result, dict) else type(result)}")
            if isinstance(result, dict) and "monsters" in result:
                print(f"[HEX DEBUG] Number of monsters spawned: {len(result['monsters'])}")
            return result
        return None

    def _get_terrain_encounter(self):
        """Get an encounter appropriate for this hex's terrain"""
        terrain_encounters = {
            "Grasslands": overland_tables.ENCOUNTER_GRASSLANDS,
            "Woods": overland_tables.ENCOUNTER_WOODS,
            "Hills": overland_tables.ENCOUNTER_HILLS,
            "Mountains": overland_tables.ENCOUNTER_MOUNTAINS,
            "Swamp": overland_tables.ENCOUNTER_SWAMPS,
            "Wasteland": overland_tables.ENCOUNTER_WASTELANDS
        }

        encounter_table = terrain_encounters.get(self.terrain, overland_tables.ENCOUNTER_GRASSLANDS)
        return roll_on_table(encounter_table)

    def _spawn_hostile_encounter(self):
        """Spawn monsters for a hostile encounter"""
        from generators.monster import Monster
        import random

        # Get encounter type based on terrain
        encounter_type = self._get_terrain_encounter()

        # Map encounter type to creature table
        creature_tables = {
            "Human": overland_tables.CREATURES_HUMAN,
            "Animal": overland_tables.CREATURES_ANIMAL,
            "Humanoid": overland_tables.CREATURES_HUMANOID,
            "Monster (S)": overland_tables.CREATURES_MONSTER_S,
            "Monster (L)": overland_tables.CREATURES_MONSTER_L,
            "Unnatural": overland_tables.CREATURES_UNNATURAL
        }

        # Get creature table and roll for specific creature
        creature_table = creature_tables.get(encounter_type, overland_tables.CREATURES_ANIMAL)
        creature_data = roll_on_table(creature_table)

        # Determine number appearing based on encounter type
        num_appearing_dice = {
            "Human": 4,           # d4
            "Animal": 6,          # d6
            "Humanoid": 4,        # d4
            "Monster (S)": 2,     # d2
            "Monster (L)": 1,     # 1
            "Unnatural": 1        # 1
        }

        dice_size = num_appearing_dice.get(encounter_type, 1)
        if dice_size == 1:
            num_appearing = 1
        else:
            num_appearing = random.randint(1, dice_size)

        # Special case for Skeletons/Zombies - always d6
        if "Skeleton" in creature_data or "Zombie" in creature_data:
            num_appearing = random.randint(1, 6)

        # Create monster instances
        monsters = []
        for i in range(num_appearing):
            monster = Monster.from_table_entry(creature_data)
            if num_appearing > 1:
                monster.name = f"{monster.name} #{i + 1}"
            monsters.append(monster)

        # Return encounter info with monsters
        return {
            "encounter_type": encounter_type,
            "creature_name": creature_data.split(" (")[0] if isinstance(creature_data, str) else "Unknown",
            "num_appearing": num_appearing,
            "monsters": monsters
        }

    def _spawn_unnatural_encounter(self):
        """Spawn unnatural monsters (undead/demons) for an unnatural danger"""
        from generators.monster import Monster
        import random

        # Roll on DANGER_UNNATURAL table to get creature type
        creature_type = roll_on_table(overland_tables.DANGER_UNNATURAL)

        # Get creature data from CREATURES_UNNATURAL table
        creature_data = None
        for entry in overland_tables.CREATURES_UNNATURAL.values():
            if creature_type.lower() in entry.lower():
                creature_data = entry
                break

        # Fallback if not found in table
        if not creature_data:
            creature_data = f"{creature_type} (HD 2, AC 12, ATK +2, DMG 1d6)"

        # Determine number appearing based on creature type
        # Skeletons and Zombies appear in groups (d6)
        # Others appear solo or in pairs
        if "Skeleton" in creature_type or "Zombie" in creature_type:
            num_appearing = random.randint(1, 6)
        elif "Ghoul" in creature_type:
            num_appearing = random.randint(1, 4)
        else:
            num_appearing = 1

        # Create monster instances
        monsters = []
        for i in range(num_appearing):
            monster = Monster.from_table_entry(creature_data)
            if num_appearing > 1:
                monster.name = f"{monster.name} #{i + 1}"
            monsters.append(monster)

        # Return encounter info with monsters
        return {
            "encounter_type": "Unnatural",
            "creature_name": creature_type,
            "num_appearing": num_appearing,
            "monsters": monsters
        }

    def reveal(self):
        """Mark hex as revealed (visible but not yet explored)"""
        self.revealed = True

    @classmethod
    def from_dict(cls, data):
        """
        Create Hex from dictionary.

        Args:
            data (dict): Hex data dictionary

        Returns:
            Hex: Reconstructed hex object
        """
        hex_obj = cls(
            q=data["q"],
            r=data["r"],
            terrain=data["terrain"],
            weather=data["weather"],
            water=data["water"]
        )
        hex_obj.revealed = data["revealed"]
        hex_obj.explored = data["explored"]
        hex_obj.is_settlement = data.get("is_settlement", False)
        hex_obj.settlement_type = data.get("settlement_type")
        hex_obj.available_vendors = data.get("available_vendors", [])
        hex_obj.discoveries = data["discoveries"]
        hex_obj.dangers = data["dangers"]
        return hex_obj

    def to_dict(self):
        """Convert hex to dictionary for serialization"""
        return {
            "q": self.q,
            "r": self.r,
            "terrain": self.terrain,
            "weather": self.weather,
            "water": self.water,
            "revealed": self.revealed,
            "explored": self.explored,
            "is_settlement": self.is_settlement,
            "settlement_type": self.settlement_type,
            "available_vendors": self.available_vendors,
            "discoveries": self.discoveries,
            "dangers": self.dangers
        }

    def __str__(self):
        status = "Explored" if self.explored else ("Revealed" if self.revealed else "Hidden")
        water_info = " [Water]" if self.water else ""
        return f"Hex({self.q},{self.r}): {self.terrain}, {self.weather}{water_info} [{status}]"

    def __repr__(self):
        return f"Hex(q={self.q}, r={self.r}, terrain='{self.terrain}')"


class HexGrid:
    """Manages a collection of hexes and player position"""

    def __init__(self, start_position=(0, 0)):
        """
        Initialize hex grid.

        Args:
            start_position (tuple): Starting (q, r) coordinates for player
        """
        self.hexes = {}  # Dictionary of hexes by (q, r) coordinates
        self.player_position = start_position

        # Create starting hex as Village and mark as explored
        start_hex = self.get_or_create_hex(start_position[0], start_position[1], terrain="Village")
        start_hex.explored = True

        # Reveal adjacent hexes (will use Village as reference)
        self.reveal_adjacent_hexes()

    def get_or_create_hex(self, q, r, terrain=None, weather=None, water=None, reference_terrain=None):
        """
        Get hex at coordinates, or create if it doesn't exist.

        Args:
            q (int): Column coordinate
            r (int): Row coordinate
            terrain (str, optional): Terrain type
            weather (str, optional): Weather condition
            water (bool, optional): Whether hex has water
            reference_terrain (str, optional): Reference terrain for NEW_TERRAIN table

        Returns:
            Hex: The hex at that position
        """
        coords = (q, r)
        if coords not in self.hexes:
            self.hexes[coords] = Hex(q, r, terrain, weather, water, reference_terrain)
        return self.hexes[coords]

    def move_player(self, direction, distance=1):
        """
        Move player in specified direction.

        Args:
            direction (int): Direction constant (1-6)
            distance (int): Number of hexes to move

        Returns:
            dict: Movement results including hexes traversed and exploration
        """
        if direction not in AXIAL_DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}. Must be 1-6.")

        dq, dr = AXIAL_DIRECTIONS[direction]
        results = {
            "direction": DIRECTION_NAMES[direction],
            "distance": distance,
            "path": [],
            "explorations": []
        }

        # Move step by step
        for step in range(1, distance + 1):
            new_q = self.player_position[0] + (dq * step)
            new_r = self.player_position[1] + (dr * step)

            # Get or create hex at new position
            hex_obj = self.get_or_create_hex(new_q, new_r)
            results["path"].append(hex_obj)

            # Explore if not already explored
            if not hex_obj.explored:
                exploration_result = hex_obj.explore()
                results["explorations"].append({
                    "hex": hex_obj.coordinates,
                    "result": exploration_result
                })

        # Update player position to final destination
        self.player_position = (
            self.player_position[0] + (dq * distance),
            self.player_position[1] + (dr * distance)
        )
        results["final_position"] = self.player_position

        # Reveal adjacent hexes around new position
        self.reveal_adjacent_hexes()

        return results

    def get_hex_at(self, q, r):
        """Get hex at coordinates if it exists"""
        return self.hexes.get((q, r))

    def get_current_hex(self):
        """Get hex at player's current position"""
        return self.get_or_create_hex(self.player_position[0], self.player_position[1])

    def generate_quest_destination(self, reveal=True):
        """
        Generate a quest destination using 1d6 direction and 1d6 distance.

        Args:
            reveal (bool): Whether to reveal the destination hex (default True)

        Returns:
            dict: Quest destination information
        """
        direction = roll_d6()  # 1-6 for direction
        distance = roll_d6()   # 1-6 for distance

        # Calculate destination coordinates
        dq, dr = AXIAL_DIRECTIONS[direction]
        dest_q = self.player_position[0] + (dq * distance)
        dest_r = self.player_position[1] + (dr * distance)

        # Get or create hex at destination (but don't explore it)
        dest_hex = self.get_or_create_hex(dest_q, dest_r)

        # Reveal the destination if requested
        if reveal and not dest_hex.explored:
            dest_hex.reveal()

        return {
            "direction": direction,
            "direction_name": DIRECTION_NAMES[direction],
            "distance": distance,
            "coordinates": (dest_q, dest_r),
            "hex": dest_hex
        }

    def reveal_hex(self, q, r):
        """
        Reveal a hex at specific coordinates (make it visible but not explored).

        Args:
            q (int): Column coordinate
            r (int): Row coordinate

        Returns:
            Hex: The revealed hex
        """
        hex_obj = self.get_or_create_hex(q, r)
        if not hex_obj.explored:
            hex_obj.reveal()
        return hex_obj

    def reveal_adjacent_hexes(self, q=None, r=None):
        """
        Reveal all hexes adjacent to the given position (or current player position).

        Args:
            q (int, optional): Column coordinate. If None, uses player position.
            r (int, optional): Row coordinate. If None, uses player position.

        Returns:
            list[Hex]: List of revealed hexes
        """
        if q is None or r is None:
            q, r = self.player_position

        # Get current hex terrain to use as reference
        current_hex = self.get_hex_at(q, r)
        reference_terrain = current_hex.terrain if current_hex else None

        revealed = []
        # Reveal all 6 adjacent hexes using current terrain as reference
        for direction, (dq, dr) in AXIAL_DIRECTIONS.items():
            adj_q = q + dq
            adj_r = r + dr
            hex_obj = self.get_or_create_hex(adj_q, adj_r, reference_terrain=reference_terrain)
            if not hex_obj.explored and not hex_obj.revealed:
                hex_obj.reveal()
                revealed.append(hex_obj)

        return revealed

    @staticmethod
    def distance_between(coord1, coord2):
        """
        Calculate distance between two hex coordinates.

        Args:
            coord1 (tuple): First (q, r) coordinate
            coord2 (tuple): Second (q, r) coordinate

        Returns:
            int: Distance in hexes
        """
        q1, r1 = coord1
        q2, r2 = coord2
        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2

    def get_visible_hexes(self):
        """
        Get all hexes that are visible (revealed or explored).

        Returns:
            list[Hex]: List of visible hexes
        """
        return [hex_obj for hex_obj in self.hexes.values()
                if hex_obj.revealed or hex_obj.explored]

    def get_hex_info(self, q, r):
        """
        Get information about a hex (for UI display).

        Args:
            q (int): Column coordinate
            r (int): Row coordinate

        Returns:
            dict: Hex information or None if hex doesn't exist
        """
        hex_obj = self.get_hex_at(q, r)
        if hex_obj is None:
            return None

        info = {
            "coordinates": (q, r),
            "terrain": hex_obj.terrain,
            "water": hex_obj.water,
            "revealed": hex_obj.revealed,
            "explored": hex_obj.explored
        }

        # Only include detailed info if explored
        if hex_obj.explored:
            info["weather"] = hex_obj.weather
            info["discoveries"] = hex_obj.discoveries
            info["dangers"] = hex_obj.dangers

        return info

    @classmethod
    def from_dict(cls, data):
        """
        Create HexGrid from dictionary.

        Args:
            data (dict): Grid data dictionary

        Returns:
            HexGrid: Reconstructed grid object
        """
        player_pos = tuple(data["player_position"])
        grid = cls.__new__(cls)  # Create instance without calling __init__
        grid.player_position = player_pos
        grid.hexes = {}

        # Reconstruct all hexes
        for coord_str, hex_data in data["hexes"].items():
            q, r = map(int, coord_str.split(','))
            grid.hexes[(q, r)] = Hex.from_dict(hex_data)

        return grid

    def to_dict(self):
        """Convert grid to dictionary for serialization"""
        return {
            "player_position": self.player_position,
            "hexes": {f"{q},{r}": hex_obj.to_dict() for (q, r), hex_obj in self.hexes.items()}
        }

    def __str__(self):
        return f"HexGrid(player_at={self.player_position}, hexes={len(self.hexes)})"


def roll_direction():
    """Roll 1d6 for direction"""
    return roll_d6()


def roll_distance():
    """Roll 1d6 for distance"""
    return roll_d6()
