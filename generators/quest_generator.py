"""
Quest Generator for RPG Game
Uses the quest tables to generate random quests
"""

from tables.table_roller import roll_on_table, roll_d6
from tables import overland_tables


class Quest:
    """Represents a generated quest"""

    def __init__(self, action, target, where, opposition, source, reward, direction=None, distance=None,
                 coordinates=None, completed=False, completion_timestamp=None,
                 completion_coordinates=None, dungeon=None):
        self.action = action
        self.target = target
        self.where = where
        self.opposition = opposition
        self.source = source
        self.reward = reward
        self.direction = direction  # Direction name (e.g., "North")
        self.distance = distance    # Distance in hexes
        self.coordinates = coordinates  # Destination (q, r) if using hex grid
        self.completed = completed  # Whether quest has been completed
        self.completion_timestamp = completion_timestamp  # When quest was completed
        self.completion_coordinates = completion_coordinates  # Where quest was completed
        self.dungeon = dungeon  # Dungeon object (generated when arriving at destination)

    @classmethod
    def from_dict(cls, data):
        """
        Create Quest from dictionary.

        Args:
            data (dict): Quest data dictionary

        Returns:
            Quest: Reconstructed quest object
        """
        # Import Dungeon here to avoid circular imports
        from generators.dungeon_generator import Dungeon

        dungeon = None
        if data.get("dungeon"):
            dungeon = Dungeon.from_dict(data["dungeon"])

        return cls(
            action=data["action"],
            target=data["target"],
            where=data["where"],
            opposition=data["opposition"],
            source=data["source"],
            reward=data["reward"],
            direction=data.get("direction"),
            distance=data.get("distance"),
            coordinates=tuple(data["coordinates"]) if data.get("coordinates") else None,
            completed=data.get("completed", False),
            completion_timestamp=data.get("completion_timestamp"),
            completion_coordinates=tuple(data["completion_coordinates"]) if data.get("completion_coordinates") else None,
            dungeon=dungeon
        )

    def __str__(self):
        """Generate the quest description"""
        base_description = (
            f"You must {self.action.lower()} a {self.target.lower()} "
            f"at {self.where.lower()} held by {self.opposition.lower()}. "
            f"Request was given by {self.source.lower()} "
            f"and offered {self.reward.lower()}."
        )

        # Add direction and distance if available
        if self.direction and self.distance:
            location_info = f" The location is {self.distance} hex{'es' if self.distance > 1 else ''} {self.direction.lower()}."
            return base_description + location_info

        return base_description

    def to_dict(self):
        """Convert quest to dictionary"""
        result = {
            "action": self.action,
            "target": self.target,
            "where": self.where,
            "opposition": self.opposition,
            "source": self.source,
            "reward": self.reward,
            "description": str(self),
            "completed": self.completed
        }

        # Add hex grid info if available
        if self.direction is not None:
            result["direction"] = self.direction
        if self.distance is not None:
            result["distance"] = self.distance
        if self.coordinates is not None:
            result["coordinates"] = self.coordinates

        # Add completion info if completed
        if self.completion_timestamp is not None:
            result["completion_timestamp"] = self.completion_timestamp
        if self.completion_coordinates is not None:
            result["completion_coordinates"] = self.completion_coordinates

        # Add dungeon info if exists
        if self.dungeon is not None:
            result["dungeon"] = self.dungeon.to_dict()

        return result

    def formatted_display(self):
        """Display quest in a formatted, readable way"""
        lines = [
            "=" * 60,
            "QUEST",
            "=" * 60,
            f"  Action:      {self.action}",
            f"  Target:      {self.target}",
            f"  Location:    {self.where}",
            f"  Opposition:  {self.opposition}",
            f"  Source:      {self.source}",
            f"  Reward:      {self.reward}",
        ]

        # Add hex grid info if available
        if self.direction is not None:
            lines.append(f"  Direction:   {self.direction}")
        if self.distance is not None:
            lines.append(f"  Distance:    {self.distance} hex{'es' if self.distance > 1 else ''}")
        if self.coordinates is not None:
            lines.append(f"  Coordinates: {self.coordinates}")

        lines.extend([
            "-" * 60,
            "Description:",
            f"  {str(self)}",
            "=" * 60
        ])
        return "\n".join(lines)


def generate_quest():
    """
    Generate a random quest using the quest tables.

    Returns:
        Quest: A generated quest object

    Example:
        >>> quest = generate_quest()
        >>> print(quest)
        You must locate a treasure at ruin held by rivals. Request was
        given by cleric and offered gold.
    """
    action = roll_on_table(overland_tables.QUEST_ACTION)
    target = roll_on_table(overland_tables.QUEST_TARGET)
    where = roll_on_table(overland_tables.QUEST_WHERE)
    opposition = roll_on_table(overland_tables.QUEST_OPPOSITION)
    source = roll_on_table(overland_tables.QUEST_SOURCE)
    reward = roll_on_table(overland_tables.QUEST_REWARD)

    return Quest(action, target, where, opposition, source, reward)


def generate_multiple_quests(count=3):
    """
    Generate multiple random quests.

    Args:
        count (int): Number of quests to generate

    Returns:
        list[Quest]: List of generated quests
    """
    return [generate_quest() for _ in range(count)]


def generate_quest_with_location(hex_grid, excluded_coordinates=None):
    """
    Generate a quest with a specific hex grid location.

    Args:
        hex_grid (HexGrid): The hex grid to generate destination on
        excluded_coordinates (list): List of coordinate tuples to avoid (optional)

    Returns:
        Quest: A generated quest with direction, distance, and coordinates

    Example:
        >>> from generators.hex_grid import HexGrid
        >>> grid = HexGrid()
        >>> quest = generate_quest_with_location(grid)
        >>> print(quest)
        You must rescue a merchant at castle held by bandits. Request was
        given by noble and offered magic item. The location is 3 hexes northeast.
    """
    # Generate base quest
    action = roll_on_table(overland_tables.QUEST_ACTION)
    target = roll_on_table(overland_tables.QUEST_TARGET)
    where = roll_on_table(overland_tables.QUEST_WHERE)
    opposition = roll_on_table(overland_tables.QUEST_OPPOSITION)
    source = roll_on_table(overland_tables.QUEST_SOURCE)
    reward = roll_on_table(overland_tables.QUEST_REWARD)

    # Generate quest destination on hex grid with uniqueness check
    # Try up to 20 times to get a unique location
    max_attempts = 20
    destination = None

    if excluded_coordinates is None:
        excluded_coordinates = []

    # Convert excluded coordinates to set of tuples for faster lookup
    excluded_set = {tuple(coord) if isinstance(coord, list) else coord
                   for coord in excluded_coordinates}

    for attempt in range(max_attempts):
        destination = hex_grid.generate_quest_destination()
        dest_coords = tuple(destination["coordinates"])

        # Check if this destination is unique
        if dest_coords not in excluded_set:
            break  # Found a unique location

        # If this is the last attempt, accept the duplicate
        if attempt == max_attempts - 1:
            break

    return Quest(
        action, target, where, opposition, source, reward,
        direction=destination["direction_name"],
        distance=destination["distance"],
        coordinates=destination["coordinates"]
    )


def display_quest_with_clues():
    """
    Generate a quest and check if clues are available.

    Returns:
        tuple: (Quest, has_clues, clue_type)
    """
    quest = generate_quest()

    # Roll on CLUE_FOUND table
    clue_roll = roll_d6()
    if clue_roll == 5:
        clue_type = "Narrative Shift"
        has_clues = True
        narrative_shift = roll_on_table(overland_tables.NARRATIVE_SHIFT)
        clue_detail = narrative_shift
    elif clue_roll == 6:
        clue_type = "Clues"
        has_clues = True
        clue = roll_on_table(overland_tables.CLUES)
        clue_detail = clue
    else:
        clue_type = "No"
        has_clues = False
        clue_detail = None

    return quest, has_clues, clue_type, clue_detail


def main():
    """Main function to demonstrate quest generation"""
    print("=" * 70)
    print("QUEST GENERATOR")
    print("=" * 70)
    print()

    # Generate a single quest
    print("Single Quest:")
    print("-" * 70)
    quest = generate_quest()
    print(quest.formatted_display())
    print()

    # Generate multiple quests
    print("\nMultiple Quests:")
    print("-" * 70)
    quests = generate_multiple_quests(3)
    for i, quest in enumerate(quests, 1):
        print(f"\nQuest {i}:")
        print(f"  {quest}")
    print()

    # Generate quest with clue check
    print("\n" + "=" * 70)
    print("QUEST WITH CLUE CHECK")
    print("=" * 70)
    quest, has_clues, clue_type, clue_detail = display_quest_with_clues()
    print(quest.formatted_display())
    print()
    print("Clue Check:")
    print(f"  Clues Found: {clue_type}")
    if has_clues:
        print(f"  Clue Detail: {clue_detail}")
    print()


if __name__ == "__main__":
    main()
