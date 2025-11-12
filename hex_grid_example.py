"""
Example usage of the hex grid system with quest integration
Demonstrates the gameplay flow you described:
1. Start with one hex (player's starting position)
2. Generate quest with destination
3. Quest reveals destination hex (greyed out)
4. Moving to hex reveals exploration results
"""

from generators import (
    HexGrid, generate_quest_with_location,
    DIRECTION_NAMES
)


def print_separator(char="=", length=70):
    """Print a separator line"""
    print(char * length)


def print_hex_info(hex_obj, show_exploration=False):
    """Print detailed hex information"""
    print(f"  Coordinates: {hex_obj.coordinates}")
    print(f"  Terrain:     {hex_obj.terrain}")
    print(f"  Water:       {'Yes' if hex_obj.water else 'No'}")
    print(f"  Weather:     {hex_obj.weather}")
    print(f"  Status:      {'Explored' if hex_obj.explored else ('Revealed' if hex_obj.revealed else 'Hidden')}")

    if show_exploration and hex_obj.explored:
        if hex_obj.discoveries:
            print(f"\n  Discoveries:")
            for disc in hex_obj.discoveries:
                print(f"    - {disc['type']}: {disc['detail']}")
        if hex_obj.dangers:
            print(f"\n  Dangers:")
            for danger in hex_obj.dangers:
                print(f"    - {danger['type']}: {danger['detail']}")


def example_basic_hex_grid():
    """Example 1: Basic hex grid creation and exploration"""
    print_separator()
    print("EXAMPLE 1: Basic Hex Grid")
    print_separator()
    print()

    # Create hex grid (starts at 0,0)
    grid = HexGrid()
    print(f"Grid created: {grid}")
    print(f"Player starting position: {grid.player_position}")
    print()

    # Show starting hex
    start_hex = grid.get_current_hex()
    print("Starting Hex:")
    print_hex_info(start_hex, show_exploration=True)
    print()


def example_quest_with_destination():
    """Example 2: Generate quest with hex grid destination"""
    print_separator()
    print("EXAMPLE 2: Quest with Hex Grid Destination")
    print_separator()
    print()

    # Create grid
    grid = HexGrid()
    print("Game started. Only one hex visible (your starting location).")
    print(f"Current position: {grid.player_position}")
    print()

    # Generate quest with location
    print("Generating quest...")
    quest = generate_quest_with_location(grid)
    print()
    print(quest.formatted_display())
    print()

    # Show that destination is now revealed
    print("Quest accepted! Destination hex is now revealed (but not explored):")
    dest_hex = grid.get_hex_at(quest.coordinates[0], quest.coordinates[1])
    print_hex_info(dest_hex)
    print()

    # Show visible hexes
    visible = grid.get_visible_hexes()
    print(f"Visible hexes: {len(visible)}")
    print("  - Starting hex (explored)")
    print("  - Destination hex (revealed, awaiting exploration)")
    print()


def example_quest_and_travel():
    """Example 3: Complete quest flow - generate quest, travel, explore"""
    print_separator()
    print("EXAMPLE 3: Complete Quest Flow")
    print_separator()
    print()

    # Step 1: Start game
    grid = HexGrid()
    print("=== GAME START ===")
    print(f"You are at position {grid.player_position}")
    current_hex = grid.get_current_hex()
    print(f"Terrain: {current_hex.terrain}")
    print(f"Weather: {current_hex.weather}")
    print(f"Water: {'Yes' if current_hex.water else 'No'}")
    print()

    # Step 2: Get quest
    print("=== RECEIVING QUEST ===")
    quest = generate_quest_with_location(grid)
    print(quest.formatted_display())
    print()

    # Step 3: Show that destination is revealed
    print("=== DESTINATION REVEALED ===")
    print(f"A hex appears {quest.direction.lower()}, {quest.distance} hex{'es' if quest.distance > 1 else ''} away.")
    print("The hex is greyed out, awaiting your arrival.")
    print()

    # Step 4: Travel to destination (using the direction and distance from quest)
    print("=== TRAVELING TO DESTINATION ===")
    direction_map = {v: k for k, v in DIRECTION_NAMES.items()}
    direction_num = direction_map[quest.direction]

    print(f"Moving {quest.direction.lower()} for {quest.distance} hex{'es' if quest.distance > 1 else ''}...")
    result = grid.move_player(direction_num, quest.distance)
    print()

    # Step 5: Show exploration results
    print("=== ARRIVAL & EXPLORATION ===")
    print(f"You have arrived at {grid.player_position}")
    print()

    if result["explorations"]:
        for i, exploration in enumerate(result["explorations"], 1):
            hex_coords = exploration["hex"]
            hex_result = exploration["result"]

            print(f"Hex {i} - {hex_coords}:")

            # Get the hex object
            explored_hex = grid.get_hex_at(hex_coords[0], hex_coords[1])

            # Show basic info that's always visible
            print(f"  Terrain: {explored_hex.terrain}")
            print(f"  Same as current? {'Yes' if explored_hex.terrain == current_hex.terrain else 'No'}")
            print(f"  Water: {'Yes' if explored_hex.water else 'No'}")
            print(f"  Weather: {explored_hex.weather}")

            # Show exploration die results
            if not hex_result["already_explored"]:
                if hex_result["discoveries"]:
                    print(f"  EXPLORE DIE: Discovery!")
                    for disc in hex_result["discoveries"]:
                        print(f"    - {disc['type']}: {disc['detail']}")

                if hex_result["dangers"]:
                    print(f"  EXPLORE DIE: Danger!")
                    for danger in hex_result["dangers"]:
                        print(f"    - {danger['type']}: {danger['detail']}")

                if "spoor" in hex_result:
                    print(f"  EXPLORE DIE: Spoor - {hex_result['spoor']}")

                if not hex_result["discoveries"] and not hex_result["dangers"] and "spoor" not in hex_result:
                    print(f"  EXPLORE DIE: Nothing encountered")
            print()

    print("=== QUEST LOCATION REACHED ===")
    print("You can now complete your quest objective!")
    print()


def example_multiple_quests():
    """Example 4: Managing multiple quests and revealed hexes"""
    print_separator()
    print("EXAMPLE 4: Multiple Quests")
    print_separator()
    print()

    grid = HexGrid()
    print("=== QUEST BOARD ===")
    print()

    # Generate 3 quests
    quests = []
    for i in range(3):
        quest = generate_quest_with_location(grid)
        quests.append(quest)
        print(f"Quest {i+1}:")
        print(f"  {quest}")
        print()

    # Show all visible hexes
    visible = grid.get_visible_hexes()
    print(f"Visible hexes on map: {len(visible)}")
    print(f"  - 1 explored (starting position)")
    print(f"  - {len(visible)-1} revealed (quest destinations)")
    print()

    # Show each quest destination
    print("=== REVEALED DESTINATIONS ===")
    for i, quest in enumerate(quests, 1):
        dest_hex = grid.get_hex_at(quest.coordinates[0], quest.coordinates[1])
        print(f"Quest {i} destination ({quest.coordinates}):")
        print(f"  Direction: {quest.direction}")
        print(f"  Distance: {quest.distance} hex{'es' if quest.distance > 1 else ''}")
        print(f"  Terrain: {dest_hex.terrain} (greyed out)")
        print(f"  Status: {'Revealed, awaiting exploration' if dest_hex.revealed else 'Explored'}")
        print()


def example_hex_info_for_ui():
    """Example 5: Getting hex info for UI display"""
    print_separator()
    print("EXAMPLE 5: Hex Info for UI Display")
    print_separator()
    print()

    grid = HexGrid()

    # Generate quest to create a revealed hex
    quest = generate_quest_with_location(grid)

    print("=== HEX INFO FOR UI ===")
    print()

    # Get info for starting hex (explored)
    print("Starting hex (explored):")
    start_info = grid.get_hex_info(0, 0)
    print(f"  Info: {start_info}")
    print(f"  Note: Full info available (weather, discoveries, etc.)")
    print()

    # Get info for quest destination (revealed but not explored)
    print(f"Quest destination hex (revealed but not explored):")
    dest_info = grid.get_hex_info(quest.coordinates[0], quest.coordinates[1])
    print(f"  Info: {dest_info}")
    print(f"  Note: Limited info - terrain and water visible, but no weather/discoveries yet")
    print()

    # Get info for non-existent hex
    print("Non-existent hex:")
    none_info = grid.get_hex_info(10, 10)
    print(f"  Info: {none_info}")
    print(f"  Note: None returned for hexes that haven't been created")
    print()


def main():
    """Run all examples"""
    examples = [
        example_basic_hex_grid,
        example_quest_with_destination,
        example_quest_and_travel,
        example_multiple_quests,
        example_hex_info_for_ui
    ]

    for example in examples:
        example()
        input("Press Enter to continue to next example...")
        print("\n\n")


if __name__ == "__main__":
    main()
