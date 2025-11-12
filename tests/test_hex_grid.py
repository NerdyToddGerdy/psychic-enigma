"""
Unit tests for hex_grid module
"""

import unittest
from generators.hex_grid import (
    Hex, HexGrid,
    NORTH, NORTHEAST, SOUTHEAST, SOUTH, SOUTHWEST, NORTHWEST,
    DIRECTION_NAMES, AXIAL_DIRECTIONS,
    roll_direction, roll_distance
)


class TestHex(unittest.TestCase):
    """Test cases for Hex class"""

    def test_hex_initialization(self):
        """Test hex initializes with coordinates"""
        hex_obj = Hex(0, 0)
        self.assertEqual(hex_obj.q, 0)
        self.assertEqual(hex_obj.r, 0)
        self.assertIsNotNone(hex_obj.terrain)
        self.assertIsNotNone(hex_obj.weather)
        self.assertIsInstance(hex_obj.water, bool)

    def test_hex_with_specific_terrain(self):
        """Test hex can be created with specific terrain"""
        hex_obj = Hex(1, 1, terrain="Woods", weather="Clear")
        self.assertEqual(hex_obj.terrain, "Woods")
        self.assertEqual(hex_obj.weather, "Clear")

    def test_hex_with_water(self):
        """Test hex can be created with specific water value"""
        hex_obj = Hex(0, 0, water=True)
        self.assertTrue(hex_obj.water)

        hex_obj2 = Hex(1, 1, water=False)
        self.assertFalse(hex_obj2.water)

    def test_hex_coordinates_property(self):
        """Test coordinates property returns tuple"""
        hex_obj = Hex(2, 3)
        self.assertEqual(hex_obj.coordinates, (2, 3))

    def test_hex_starts_unexplored(self):
        """Test hex starts as unexplored"""
        hex_obj = Hex(0, 0)
        self.assertFalse(hex_obj.explored)
        self.assertFalse(hex_obj.revealed)

    def test_hex_reveal(self):
        """Test hex can be revealed"""
        hex_obj = Hex(0, 0)
        hex_obj.reveal()
        self.assertTrue(hex_obj.revealed)
        self.assertFalse(hex_obj.explored)

    def test_hex_explore(self):
        """Test hex exploration"""
        hex_obj = Hex(0, 0)
        result = hex_obj.explore()

        self.assertTrue(hex_obj.explored)
        self.assertFalse(result["already_explored"])
        self.assertIsInstance(result["discoveries"], list)
        self.assertIsInstance(result["dangers"], list)

    def test_hex_explore_already_explored(self):
        """Test exploring an already explored hex"""
        hex_obj = Hex(0, 0)
        hex_obj.explore()
        result = hex_obj.explore()

        self.assertTrue(result["already_explored"])

    def test_hex_to_dict(self):
        """Test hex serialization"""
        hex_obj = Hex(1, 2, terrain="Hills", weather="Rain", water=True)
        hex_dict = hex_obj.to_dict()

        self.assertEqual(hex_dict["q"], 1)
        self.assertEqual(hex_dict["r"], 2)
        self.assertEqual(hex_dict["terrain"], "Hills")
        self.assertEqual(hex_dict["weather"], "Rain")
        self.assertTrue(hex_dict["water"])
        self.assertFalse(hex_dict["explored"])
        self.assertFalse(hex_dict["revealed"])

    def test_hex_str_representation(self):
        """Test hex string representation"""
        hex_obj = Hex(0, 0, terrain="Woods", weather="Clear", water=False)
        str_repr = str(hex_obj)

        self.assertIn("Hex(0,0)", str_repr)
        self.assertIn("Woods", str_repr)
        self.assertIn("Clear", str_repr)

    def test_hex_str_with_water(self):
        """Test hex string shows water"""
        hex_obj = Hex(0, 0, water=True)
        str_repr = str(hex_obj)
        self.assertIn("[Water]", str_repr)


class TestHexGrid(unittest.TestCase):
    """Test cases for HexGrid class"""

    def test_grid_initialization(self):
        """Test grid initializes with starting position"""
        grid = HexGrid()
        self.assertEqual(grid.player_position, (0, 0))
        self.assertEqual(len(grid.hexes), 1)

    def test_grid_custom_start_position(self):
        """Test grid can start at custom position"""
        grid = HexGrid(start_position=(2, 3))
        self.assertEqual(grid.player_position, (2, 3))

    def test_starting_hex_is_explored(self):
        """Test starting hex is marked as explored"""
        grid = HexGrid()
        start_hex = grid.get_current_hex()
        self.assertTrue(start_hex.explored)

    def test_get_or_create_hex(self):
        """Test getting or creating hexes"""
        grid = HexGrid()

        # Create new hex
        hex1 = grid.get_or_create_hex(1, 1)
        self.assertEqual(hex1.q, 1)
        self.assertEqual(hex1.r, 1)
        self.assertEqual(len(grid.hexes), 2)

        # Get existing hex
        hex1_again = grid.get_or_create_hex(1, 1)
        self.assertIs(hex1, hex1_again)
        self.assertEqual(len(grid.hexes), 2)

    def test_get_hex_at(self):
        """Test getting hex at coordinates"""
        grid = HexGrid()

        # Non-existent hex returns None
        self.assertIsNone(grid.get_hex_at(5, 5))

        # Existing hex returns hex
        grid.get_or_create_hex(1, 1)
        hex_obj = grid.get_hex_at(1, 1)
        self.assertIsNotNone(hex_obj)
        self.assertEqual(hex_obj.coordinates, (1, 1))

    def test_get_current_hex(self):
        """Test getting current hex"""
        grid = HexGrid()
        current = grid.get_current_hex()
        self.assertEqual(current.coordinates, (0, 0))

    def test_move_player_north(self):
        """Test moving player north"""
        grid = HexGrid()
        result = grid.move_player(NORTH, distance=1)

        self.assertEqual(result["direction"], "North")
        self.assertEqual(result["distance"], 1)
        self.assertEqual(grid.player_position, (0, -1))

    def test_move_player_northeast(self):
        """Test moving player northeast"""
        grid = HexGrid()
        result = grid.move_player(NORTHEAST, distance=2)

        self.assertEqual(result["direction"], "Northeast")
        self.assertEqual(result["distance"], 2)
        self.assertEqual(grid.player_position, (2, -2))

    def test_move_player_creates_path(self):
        """Test movement creates hexes along path"""
        grid = HexGrid()
        result = grid.move_player(SOUTH, distance=3)

        self.assertEqual(len(result["path"]), 3)
        self.assertEqual(grid.player_position, (0, 3))

    def test_move_player_explores_hexes(self):
        """Test movement explores new hexes"""
        grid = HexGrid()
        result = grid.move_player(SOUTHEAST, distance=2)

        # All hexes along path should be explored
        for path_hex in result["path"]:
            self.assertTrue(path_hex.explored)

    def test_reveal_hex(self):
        """Test revealing a hex"""
        grid = HexGrid()
        hex_obj = grid.reveal_hex(1, 1)

        self.assertTrue(hex_obj.revealed)
        self.assertFalse(hex_obj.explored)

    def test_generate_quest_destination(self):
        """Test quest destination generation"""
        grid = HexGrid()
        dest = grid.generate_quest_destination()

        self.assertIn("direction", dest)
        self.assertIn("direction_name", dest)
        self.assertIn("distance", dest)
        self.assertIn("coordinates", dest)
        self.assertIn("hex", dest)

        # Direction should be 1-6
        self.assertIn(dest["direction"], range(1, 7))

        # Distance should be 1-6
        self.assertIn(dest["distance"], range(1, 7))

        # Hex should be revealed by default
        self.assertTrue(dest["hex"].revealed)

    def test_generate_quest_destination_no_reveal(self):
        """Test quest destination without revealing"""
        grid = HexGrid()
        dest = grid.generate_quest_destination(reveal=False)

        self.assertFalse(dest["hex"].revealed)

    def test_distance_between(self):
        """Test distance calculation between hexes"""
        grid = HexGrid()

        # Same hex
        self.assertEqual(grid.distance_between((0, 0), (0, 0)), 0)

        # Adjacent hexes
        self.assertEqual(grid.distance_between((0, 0), (1, 0)), 1)
        self.assertEqual(grid.distance_between((0, 0), (0, 1)), 1)

        # Distant hexes
        self.assertEqual(grid.distance_between((0, 0), (3, 3)), 6)

    def test_get_visible_hexes(self):
        """Test getting visible hexes"""
        grid = HexGrid()

        # Initially only starting hex is visible
        visible = grid.get_visible_hexes()
        self.assertEqual(len(visible), 1)

        # Reveal a hex
        grid.reveal_hex(1, 1)
        visible = grid.get_visible_hexes()
        self.assertEqual(len(visible), 2)

        # Explore a hex
        grid.get_or_create_hex(2, 2).explore()
        visible = grid.get_visible_hexes()
        self.assertEqual(len(visible), 3)

    def test_get_hex_info(self):
        """Test getting hex info for UI"""
        grid = HexGrid()

        # Non-existent hex
        self.assertIsNone(grid.get_hex_info(10, 10))

        # Revealed but not explored hex
        grid.reveal_hex(1, 1)
        info = grid.get_hex_info(1, 1)
        self.assertEqual(info["coordinates"], (1, 1))
        self.assertTrue(info["revealed"])
        self.assertFalse(info["explored"])
        self.assertNotIn("weather", info)  # Weather not shown until explored

        # Explored hex
        grid.get_current_hex().explore()
        info = grid.get_hex_info(0, 0)
        self.assertTrue(info["explored"])
        self.assertIn("weather", info)  # Weather shown after exploration
        self.assertIn("discoveries", info)
        self.assertIn("dangers", info)

    def test_grid_to_dict(self):
        """Test grid serialization"""
        grid = HexGrid()
        grid.move_player(NORTH, 1)

        grid_dict = grid.to_dict()
        self.assertIn("player_position", grid_dict)
        self.assertIn("hexes", grid_dict)
        self.assertEqual(grid_dict["player_position"], (0, -1))


class TestDirectionConstants(unittest.TestCase):
    """Test cases for direction constants"""

    def test_direction_values(self):
        """Test direction constants have correct values"""
        self.assertEqual(NORTH, 1)
        self.assertEqual(NORTHEAST, 2)
        self.assertEqual(SOUTHEAST, 3)
        self.assertEqual(SOUTH, 4)
        self.assertEqual(SOUTHWEST, 5)
        self.assertEqual(NORTHWEST, 6)

    def test_direction_names(self):
        """Test direction names mapping"""
        self.assertEqual(DIRECTION_NAMES[NORTH], "North")
        self.assertEqual(DIRECTION_NAMES[NORTHEAST], "Northeast")
        self.assertEqual(DIRECTION_NAMES[SOUTHEAST], "Southeast")
        self.assertEqual(DIRECTION_NAMES[SOUTH], "South")
        self.assertEqual(DIRECTION_NAMES[SOUTHWEST], "Southwest")
        self.assertEqual(DIRECTION_NAMES[NORTHWEST], "Northwest")

    def test_axial_directions(self):
        """Test axial direction vectors"""
        self.assertEqual(AXIAL_DIRECTIONS[NORTH], (0, -1))
        self.assertEqual(AXIAL_DIRECTIONS[NORTHEAST], (1, -1))
        self.assertEqual(AXIAL_DIRECTIONS[SOUTHEAST], (1, 0))
        self.assertEqual(AXIAL_DIRECTIONS[SOUTH], (0, 1))
        self.assertEqual(AXIAL_DIRECTIONS[SOUTHWEST], (-1, 1))
        self.assertEqual(AXIAL_DIRECTIONS[NORTHWEST], (-1, 0))


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions"""

    def test_roll_direction(self):
        """Test direction rolling"""
        for _ in range(20):
            direction = roll_direction()
            self.assertIn(direction, range(1, 7))

    def test_roll_distance(self):
        """Test distance rolling"""
        for _ in range(20):
            distance = roll_distance()
            self.assertIn(distance, range(1, 7))


if __name__ == '__main__':
    unittest.main()
