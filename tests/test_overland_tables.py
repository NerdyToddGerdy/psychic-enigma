"""
Unit tests for overland_tables module
"""

import unittest
import sys
import os
from tables import overland_tables
from tables.table_roller import roll_on_table

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestOverlandTableStructure(unittest.TestCase):
    """Test that all Overland tables have correct structure"""

    def test_terrain_table(self):
        """Test TERRAIN table"""
        self.assertEqual(len(overland_tables.TERRAIN), 6)
        self.assertIn("Grasslands", overland_tables.TERRAIN.values())
        self.assertIn("Wasteland", overland_tables.TERRAIN.values())

    def test_weather_table(self):
        """Test WEATHER table"""
        self.assertEqual(len(overland_tables.WEATHER), 6)
        self.assertIn("Overcast", overland_tables.WEATHER.values())
        self.assertIn("Snow", overland_tables.WEATHER.values())

    def test_explore_die_table(self):
        """Test EXPLORE_DIE table"""
        self.assertEqual(len(overland_tables.EXPLORE_DIE), 6)
        # Check weighted distribution
        values = list(overland_tables.EXPLORE_DIE.values())
        self.assertEqual(values.count("Danger"), 2)
        self.assertEqual(values.count("Discovery"), 2)

    def test_discovery_tables(self):
        """Test DISCOVERY related tables"""
        self.assertEqual(len(overland_tables.DISCOVERY), 6)
        self.assertEqual(len(overland_tables.DISCOVERY_NATURAL), 6)
        self.assertEqual(len(overland_tables.DISCOVERY_UNNATURAL), 6)
        self.assertEqual(len(overland_tables.DISCOVERY_RUIN), 6)

    def test_danger_tables(self):
        """Test DANGER related tables"""
        self.assertEqual(len(overland_tables.DANGER), 6)
        self.assertEqual(len(overland_tables.DANGER_UNNATURAL), 6)
        self.assertEqual(len(overland_tables.DANGER_HAZARD), 6)

    def test_loot_tables(self):
        """Test loot tables"""
        self.assertEqual(len(overland_tables.LOOT_HUMANS_NOIDS), 6)
        self.assertEqual(len(overland_tables.LOOT_ANIMALS), 6)
        self.assertEqual(len(overland_tables.LOOT_MONSTERS), 6)
        self.assertEqual(len(overland_tables.LOOT_UNNATURAL), 6)

    def test_mundane_items_table(self):
        """Test MUNDANE_ITEMS table (d66)"""
        # Should have entries for valid d66 rolls
        self.assertIn(11, overland_tables.MUNDANE_ITEMS)
        self.assertIn(66, overland_tables.MUNDANE_ITEMS)
        # Should not have invalid d66 values
        self.assertNotIn(17, overland_tables.MUNDANE_ITEMS)
        self.assertNotIn(70, overland_tables.MUNDANE_ITEMS)

    def test_special_items_table(self):
        """Test SPECIAL_ITEMS table (d66)"""
        self.assertIn(11, overland_tables.SPECIAL_ITEMS)
        self.assertIn(66, overland_tables.SPECIAL_ITEMS)

    def test_magical_item_effects_table(self):
        """Test MAGICAL_ITEM_EFFECTS table (d66)"""
        self.assertIn(11, overland_tables.MAGICAL_ITEM_EFFECTS)
        self.assertIn(66, overland_tables.MAGICAL_ITEM_EFFECTS)

    def test_character_generation_tables(self):
        """Test character generation tables"""
        self.assertEqual(len(overland_tables.RACE), 6)
        self.assertEqual(len(overland_tables.CHARACTER_TYPE), 6)
        self.assertEqual(len(overland_tables.TRAITS_1), 6)
        self.assertEqual(len(overland_tables.TRAITS_2), 6)
        self.assertEqual(len(overland_tables.TRAITS_3), 6)

    def test_settlement_generation_tables(self):
        """Test settlement generation tables"""
        self.assertIsInstance(overland_tables.SETTLEMENT_PREFIX_1, list)
        self.assertIsInstance(overland_tables.SETTLEMENT_SUFFIX_1, list)
        self.assertEqual(len(overland_tables.SETTLEMENT_ADJECTIVE), 6)
        self.assertEqual(len(overland_tables.SETTLEMENT_STATUS), 6)

    def test_encounter_tables(self):
        """Test encounter by terrain tables"""
        self.assertEqual(len(overland_tables.ENCOUNTER_GRASSLANDS), 6)
        self.assertEqual(len(overland_tables.ENCOUNTER_WOODS), 6)
        self.assertEqual(len(overland_tables.ENCOUNTER_HILLS), 6)
        self.assertEqual(len(overland_tables.ENCOUNTER_MOUNTAINS), 6)
        self.assertEqual(len(overland_tables.ENCOUNTER_SWAMPS), 6)
        self.assertEqual(len(overland_tables.ENCOUNTER_WASTELANDS), 6)

    def test_creature_tables(self):
        """Test creature stat tables"""
        self.assertEqual(len(overland_tables.CREATURES_HUMAN), 6)
        self.assertEqual(len(overland_tables.CREATURES_ANIMAL), 6)
        self.assertEqual(len(overland_tables.CREATURES_HUMANOID), 6)
        self.assertEqual(len(overland_tables.CREATURES_MONSTER_S), 6)
        self.assertEqual(len(overland_tables.CREATURES_MONSTER_L), 6)
        self.assertEqual(len(overland_tables.CREATURES_UNNATURAL), 6)

        # Check creature structure
        creature = overland_tables.CREATURES_HUMAN[1]
        self.assertIn("name", creature)
        self.assertIn("hd", creature)
        self.assertIn("ac", creature)

    def test_commerce_tables(self):
        """Test commerce-related tables"""
        self.assertEqual(len(overland_tables.TRAVEL), 4)
        self.assertEqual(len(overland_tables.HELP), 4)
        self.assertEqual(len(overland_tables.HERBALIST), 3)
        self.assertIsInstance(overland_tables.MERCHANT_ITEMS, list)
        self.assertIsInstance(overland_tables.WEAPONS, dict)
        self.assertIsInstance(overland_tables.ARMOR, dict)

        # Check structure of commerce items
        travel_item = overland_tables.TRAVEL[1]
        self.assertIn("name", travel_item)
        self.assertIn("cost_sp", travel_item)

    def test_quest_tables(self):
        """Test quest generation tables"""
        self.assertEqual(len(overland_tables.QUEST_ACTION), 6)
        self.assertEqual(len(overland_tables.QUEST_TARGET), 6)
        self.assertEqual(len(overland_tables.QUEST_WHERE), 6)
        self.assertEqual(len(overland_tables.QUEST_OPPOSITION), 6)
        self.assertEqual(len(overland_tables.QUEST_REWARD), 6)


class TestOverlandTableRolling(unittest.TestCase):
    """Test that Overland tables can be rolled on successfully"""

    def test_roll_terrain(self):
        """Test rolling on TERRAIN"""
        for _ in range(10):
            result = roll_on_table(overland_tables.TERRAIN)
            self.assertIsInstance(result, str)
            self.assertIn(result, overland_tables.TERRAIN.values())

    def test_roll_weather(self):
        """Test rolling on WEATHER"""
        for _ in range(10):
            result = roll_on_table(overland_tables.WEATHER)
            self.assertIsInstance(result, str)

    def test_roll_mundane_items(self):
        """Test rolling on MUNDANE_ITEMS (d66)"""
        for _ in range(10):
            result = roll_on_table(overland_tables.MUNDANE_ITEMS)
            self.assertIsInstance(result, str)

    def test_roll_traveling_encounters(self):
        """Test rolling on TRAVELING_ENCOUNTERS (2d6)"""
        for _ in range(10):
            result = roll_on_table(overland_tables.TRAVELING_ENCOUNTERS)
            self.assertIsInstance(result, str)

    def test_roll_name_lists(self):
        """Test rolling on name lists"""
        for _ in range(10):
            result = roll_on_table(overland_tables.MALE_NAMES_1)
            self.assertIsInstance(result, str)

            result = roll_on_table(overland_tables.FEMALE_NAMES_2)
            self.assertIsInstance(result, str)

    def test_roll_creature(self):
        """Test rolling on creature tables"""
        for _ in range(10):
            result = roll_on_table(overland_tables.CREATURES_ANIMAL)
            self.assertIsInstance(result, dict)
            self.assertIn("name", result)


class TestOverlandConstants(unittest.TestCase):
    """Test Overland constants"""

    def test_currency_ratio(self):
        """Test SILVER_TO_GOLD_RATIO"""
        self.assertEqual(overland_tables.SILVER_TO_GOLD_RATIO, 10)

    def test_merchant_cost(self):
        """Test MERCHANT_COST_SP"""
        self.assertEqual(overland_tables.MERCHANT_COST_SP, 3)


if __name__ == "__main__":
    unittest.main()
