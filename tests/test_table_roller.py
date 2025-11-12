"""
Unit tests for table_roller module
"""

import os
import sys
import unittest
from tables.table_roller import (
    roll_on_table,
    roll_on_table_by_name,
    roll_d4,
    roll_d6,
    roll_2d6,
    roll_3d6,
    roll_d66,
    roll_d20,
    roll_d100,
    roll_dice,
    get_all_table_names
)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDiceRolls(unittest.TestCase):
    """Test individual dice rolling functions"""

    def test_roll_d4_range(self):
        """Test that d4 rolls are in valid range"""
        for _ in range(100):
            roll = roll_d4()
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 4)

    def test_roll_d6_range(self):
        """Test that d6 rolls are in valid range"""
        for _ in range(100):
            roll = roll_d6()
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 6)

    def test_roll_2d6_range(self):
        """Test that 2d6 rolls are in valid range"""
        for _ in range(100):
            roll = roll_2d6()
            self.assertGreaterEqual(roll, 2)
            self.assertLessEqual(roll, 12)

    def test_roll_3d6_range(self):
        """Test that 3d6 rolls are in valid range"""
        for _ in range(100):
            roll = roll_3d6()
            self.assertGreaterEqual(roll, 3)
            self.assertLessEqual(roll, 18)

    def test_roll_d66_range(self):
        """Test that d66 rolls are in valid range"""
        for _ in range(100):
            roll = roll_d66()
            self.assertGreaterEqual(roll, 11)
            self.assertLessEqual(roll, 66)
            # Check it's a valid d66 value (no 7, 8, 9 in ones place)
            ones_digit = roll % 10
            self.assertGreaterEqual(ones_digit, 1)
            self.assertLessEqual(ones_digit, 6)

    def test_roll_d20_range(self):
        """Test that d20 rolls are in valid range"""
        for _ in range(100):
            roll = roll_d20()
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 20)

    def test_roll_d100_range(self):
        """Test that d100 rolls are in valid range"""
        for _ in range(100):
            roll = roll_d100()
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 100)

    def test_roll_dice_custom(self):
        """Test custom dice rolls"""
        # Test 3d6
        for _ in range(50):
            roll = roll_dice(3, 6)
            self.assertGreaterEqual(roll, 3)
            self.assertLessEqual(roll, 18)

        # Test 2d10
        for _ in range(50):
            roll = roll_dice(2, 10)
            self.assertGreaterEqual(roll, 2)
            self.assertLessEqual(roll, 20)


class TestRollOnTable(unittest.TestCase):
    """Test rolling on tables"""

    def test_roll_on_d6_table(self):
        """Test rolling on a standard d6 table"""
        test_table = {
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six"
        }

        results = set()
        for _ in range(100):
            result = roll_on_table(test_table)
            self.assertIn(result, test_table.values())
            results.add(result)

        # We should hit multiple values in 100 rolls
        self.assertGreater(len(results), 1)

    def test_roll_on_d66_table(self):
        """Test rolling on a d66 grid table"""
        # Create a complete d66 table with all possible values
        test_table = {}
        for tens in range(1, 7):
            for ones in range(1, 7):
                key = tens * 10 + ones
                test_table[key] = f"Item {key}"

        results = set()
        for _ in range(100):
            result = roll_on_table(test_table)
            self.assertIn(result, test_table.values())
            self.assertIsNotNone(result)
            results.add(result)

        # We should hit multiple values in 100 rolls
        self.assertGreater(len(results), 1)

    def test_roll_on_2d6_table(self):
        """Test rolling on a 2d6 table"""
        # Create a complete 2d6 table with all possible values (2-12)
        test_table = {
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
            10: "Ten",
            11: "Eleven",
            12: "Twelve"
        }

        results = set()
        for _ in range(200):
            result = roll_on_table(test_table)
            self.assertIn(result, test_table.values())
            self.assertIsNotNone(result)
            results.add(result)

        # We should hit multiple values in 200 rolls
        self.assertGreater(len(results), 1)

    def test_roll_on_list(self):
        """Test rolling on a list table"""
        test_list = ["Apple", "Banana", "Cherry", "Date"]

        results = set()
        for _ in range(50):
            result = roll_on_table(test_list)
            self.assertIn(result, test_list)
            results.add(result)

        # We should hit multiple values
        self.assertGreater(len(results), 1)

    def test_roll_on_empty_table_raises_error(self):
        """Test that empty tables raise ValueError"""
        with self.assertRaises(ValueError):
            roll_on_table({})

        with self.assertRaises(ValueError):
            roll_on_table([])

    def test_roll_on_none_raises_error(self):
        """Test that None raises ValueError"""
        with self.assertRaises(ValueError):
            roll_on_table(None)

    def test_roll_on_invalid_type_raises_error(self):
        """Test that invalid types raise ValueError"""
        with self.assertRaises(ValueError):
            roll_on_table("not a table")

        with self.assertRaises(ValueError):
            roll_on_table(42)


class TestRollOnTableByName(unittest.TestCase):
    """Test rolling on tables by name from a module"""

    def test_roll_on_table_by_name(self):
        """Test rolling on a table by name"""
        from tables import overland_tables

        result = roll_on_table_by_name("TERRAIN", overland_tables)
        self.assertIn(result, ["Grasslands", "Woods", "Hills", "Mountains", "Swamp", "Wasteland"])

    def test_roll_on_nonexistent_table_raises_error(self):
        """Test that nonexistent table names raise ValueError"""
        from tables import overland_tables

        with self.assertRaises(ValueError):
            roll_on_table_by_name("NONEXISTENT_TABLE", overland_tables)


class TestGetAllTableNames(unittest.TestCase):
    """Test getting all table names from a module"""

    def test_get_all_table_names_overland(self):
        """Test getting all table names from overland_tables"""
        from tables import overland_tables

        tables = get_all_table_names(overland_tables)

        # Check that it's a list
        self.assertIsInstance(tables, list)

        # Check that it's sorted
        self.assertEqual(tables, sorted(tables))

        # Check that some known tables are in the list
        self.assertIn("TERRAIN", tables)
        self.assertIn("WEATHER", tables)
        self.assertIn("EXPLORE_DIE", tables)

    def test_get_all_table_names_dungeon(self):
        """Test getting all table names from dungeon_tables"""
        from tables import dungeon_tables

        tables = get_all_table_names(dungeon_tables)

        # Check that it's a list
        self.assertIsInstance(tables, list)

        # Check that some known tables are in the list
        self.assertIn("THEME", tables)
        self.assertIn("DUNGEON_TYPE", tables)
        self.assertIn("DANGER", tables)


if __name__ == "__main__":
    unittest.main()
