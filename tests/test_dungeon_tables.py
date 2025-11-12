"""
Unit tests for dungeon_tables module
"""

import unittest
import sys
import os
from tables import dungeon_tables
from tables.table_roller import roll_on_table

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDungeonTableStructure(unittest.TestCase):
    """Test that all Dungeon tables have correct structure"""

    def test_dungeon_generation_tables(self):
        """Test dungeon generation tables"""
        self.assertEqual(len(dungeon_tables.THEME), 6)
        self.assertEqual(len(dungeon_tables.DUNGEON_TYPE), 6)
        self.assertEqual(len(dungeon_tables.SIZE), 6)
        self.assertIn("Cave", dungeon_tables.DUNGEON_TYPE.values())
        self.assertIn("Temple", dungeon_tables.DUNGEON_TYPE.values())

    def test_adjective_noun_tables(self):
        """Test adjective and noun tables for dungeon names"""
        self.assertEqual(len(dungeon_tables.ADJECTIVE_1), 6)
        self.assertEqual(len(dungeon_tables.ADJECTIVE_2), 6)
        self.assertEqual(len(dungeon_tables.NOUN_1), 6)
        self.assertEqual(len(dungeon_tables.NOUN_2), 6)

    def test_room_corridor_contents(self):
        """Test room and corridor content tables"""
        self.assertEqual(len(dungeon_tables.CORRIDOR), 6)
        self.assertEqual(len(dungeon_tables.ROOM), 6)
        self.assertEqual(len(dungeon_tables.SPOOR), 6)
        self.assertEqual(len(dungeon_tables.DOOR), 6)

    def test_discovery_tables(self):
        """Test discovery tables"""
        self.assertEqual(len(dungeon_tables.DISCOVERY), 6)
        self.assertEqual(len(dungeon_tables.SPECIAL_ROOM_1), 6)
        self.assertEqual(len(dungeon_tables.SPECIAL_ROOM_2), 6)
        self.assertEqual(len(dungeon_tables.FEATURE), 6)
        self.assertEqual(len(dungeon_tables.ITEM), 6)
        self.assertEqual(len(dungeon_tables.TREASURE_A), 6)
        self.assertEqual(len(dungeon_tables.TREASURE_B), 6)

    def test_danger_tables(self):
        """Test danger tables"""
        self.assertEqual(len(dungeon_tables.DANGER), 6)
        self.assertEqual(len(dungeon_tables.HAZARD), 6)
        self.assertEqual(len(dungeon_tables.TRAP), 6)
        self.assertEqual(len(dungeon_tables.REACTION), 6)

    def test_dressing_tables(self):
        """Test dressing tables"""
        self.assertEqual(len(dungeon_tables.DRESSING_NATURAL), 6)
        self.assertEqual(len(dungeon_tables.DRESSING_MAN_MADE), 6)
        self.assertEqual(len(dungeon_tables.DRESSING_LIGHTING), 6)
        self.assertEqual(len(dungeon_tables.DRESSING_ODOR), 6)
        self.assertEqual(len(dungeon_tables.DRESSING_ODD), 6)
        self.assertEqual(len(dungeon_tables.DRESSING_MYSTICAL), 6)

    def test_description_tables(self):
        """Test description tables"""
        self.assertEqual(len(dungeon_tables.DESCRIPTION_1), 6)
        self.assertEqual(len(dungeon_tables.DESCRIPTION_2), 6)
        self.assertEqual(len(dungeon_tables.DESCRIPTION_3), 6)
        self.assertEqual(len(dungeon_tables.DESTRUCTION), 6)
        self.assertEqual(len(dungeon_tables.BUILDER), 6)
        self.assertEqual(len(dungeon_tables.PURPOSE), 6)

    def test_encounter_type_tables(self):
        """Test encounter type tables"""
        self.assertEqual(len(dungeon_tables.HUMANOIDS), 6)
        self.assertEqual(len(dungeon_tables.CREATURES), 6)
        self.assertEqual(len(dungeon_tables.UNNATURAL), 6)

    def test_encounter_tier_tables(self):
        """Test encounter tier tables"""
        # Tier 1-2 (2d6 results: 2-12)
        self.assertEqual(len(dungeon_tables.ENCOUNTER_TIER_1_2), 11)
        self.assertIn(2, dungeon_tables.ENCOUNTER_TIER_1_2)
        self.assertIn(12, dungeon_tables.ENCOUNTER_TIER_1_2)

        # Tier 3-4
        self.assertEqual(len(dungeon_tables.ENCOUNTER_TIER_3_4), 11)

        # Tier 5-6
        self.assertEqual(len(dungeon_tables.ENCOUNTER_TIER_5_6), 11)

    def test_denizen_tables(self):
        """Test denizen tables"""
        # Check that denizen tables exist and have correct size (2d6 = 11 results)
        self.assertEqual(len(dungeon_tables.DENIZEN_TIER_1_RANGE_1_2), 11)
        self.assertEqual(len(dungeon_tables.DENIZEN_TIER_1_RANGE_3_4), 11)
        self.assertEqual(len(dungeon_tables.DENIZEN_TIER_1_RANGE_5_6), 11)
        self.assertEqual(len(dungeon_tables.DENIZEN_TIER_2_RANGE_1_2), 11)
        self.assertEqual(len(dungeon_tables.DENIZEN_TIER_2_RANGE_3_5), 11)

    def test_monster_behavior_tables(self):
        """Test monster behavior tables"""
        self.assertEqual(len(dungeon_tables.ACTIVITY), 6)
        self.assertEqual(len(dungeon_tables.TACTIC), 6)
        self.assertEqual(len(dungeon_tables.GUARDING), 6)

    def test_dungeon_encounters_table(self):
        """Test dungeon encounters table (2d6)"""
        # 2d6 results in 2-12
        self.assertIn(2, dungeon_tables.DUNGEON_ENCOUNTERS)
        self.assertIn(12, dungeon_tables.DUNGEON_ENCOUNTERS)
        self.assertEqual(len(dungeon_tables.DUNGEON_ENCOUNTERS), 11)

    def test_loot_corpse_tables(self):
        """Test loot corpse tables"""
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_1), 6)
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_2), 6)
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_3), 6)
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_4), 6)
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_5), 6)
        self.assertEqual(len(dungeon_tables.LOOT_CORPSE_6), 6)

    def test_boss_tables(self):
        """Test boss tables"""
        self.assertIsInstance(dungeon_tables.BOSSES, dict)
        self.assertIn("lazrothe", dungeon_tables.BOSSES)
        self.assertIn("grilsa", dungeon_tables.BOSSES)

        # Check boss structure
        boss = dungeon_tables.BOSSES["lazrothe"]
        self.assertIn("name", boss)
        self.assertIn("hd", boss)
        self.assertIn("ac", boss)
        self.assertIn("attacks", boss)
        self.assertIn("tactics", boss)

        # Check tactics structure
        self.assertIsInstance(boss["tactics"], dict)
        self.assertEqual(len(boss["tactics"]), 6)


class TestDungeonTableRolling(unittest.TestCase):
    """Test that Dungeon tables can be rolled on successfully"""

    def test_roll_theme(self):
        """Test rolling on THEME"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.THEME)
            self.assertIsInstance(result, str)
            self.assertIn(result, dungeon_tables.THEME.values())

    def test_roll_dungeon_type(self):
        """Test rolling on DUNGEON_TYPE"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.DUNGEON_TYPE)
            self.assertIsInstance(result, str)

    def test_roll_door(self):
        """Test rolling on DOOR"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.DOOR)
            self.assertIsInstance(result, str)

    def test_roll_danger(self):
        """Test rolling on DANGER"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.DANGER)
            self.assertIsInstance(result, str)

    def test_roll_encounter(self):
        """Test rolling on encounter tables"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.ENCOUNTER_TIER_1_2)
            self.assertIsInstance(result, dict)
            self.assertIn("name", result)
            self.assertIn("hd", result)
            self.assertIn("ac", result)

    def test_roll_loot_corpse(self):
        """Test rolling on loot corpse tables"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.LOOT_CORPSE_1)
            self.assertIsInstance(result, str)

    def test_roll_dungeon_encounters(self):
        """Test rolling on DUNGEON_ENCOUNTERS (2d6)"""
        for _ in range(10):
            result = roll_on_table(dungeon_tables.DUNGEON_ENCOUNTERS)
            self.assertIsInstance(result, str)


class TestDungeonNameGeneration(unittest.TestCase):
    """Test dungeon name generation"""

    def test_generate_dungeon_name(self):
        """Test that we can generate a full dungeon name"""
        dungeon_type = roll_on_table(dungeon_tables.DUNGEON_TYPE)
        adjective = roll_on_table(dungeon_tables.ADJECTIVE_1)
        noun = roll_on_table(dungeon_tables.NOUN_1)

        name = f"The {adjective} {dungeon_type} of {noun}"

        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 10)
        self.assertIn("The", name)
        self.assertIn("of", name)


class TestEncounterStructure(unittest.TestCase):
    """Test that encounter entries have proper structure"""

    def test_encounter_has_required_fields(self):
        """Test that all encounters have required fields"""
        for encounter in dungeon_tables.ENCOUNTER_TIER_1_2.values():
            self.assertIn("name", encounter)
            self.assertIn("hd", encounter)
            self.assertIn("ac", encounter)
            self.assertIn("attack", encounter)

    def test_denizen_has_required_fields(self):
        """Test that all denizens have required fields"""
        for denizen in dungeon_tables.DENIZEN_TIER_1_RANGE_1_2.values():
            self.assertIn("name", denizen)
            self.assertIn("hd", denizen)
            self.assertIn("ac", denizen)


if __name__ == "__main__":
    unittest.main()
