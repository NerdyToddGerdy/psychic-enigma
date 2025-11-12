"""
Unit tests for quest_generator module
"""

import unittest
import sys
import os
from generators.quest_generator import Quest, generate_quest, generate_multiple_quests, display_quest_with_clues

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestQuestClass(unittest.TestCase):
    """Test the Quest class"""

    def setUp(self):
        """Set up test quest"""
        self.quest = Quest(
            action="Locate",
            target="Treasure",
            where="Ruin",
            opposition="Rivals",
            source="Cleric",
            reward="Gold"
        )

    def test_quest_initialization(self):
        """Test that quest initializes with correct attributes"""
        self.assertEqual(self.quest.action, "Locate")
        self.assertEqual(self.quest.target, "Treasure")
        self.assertEqual(self.quest.where, "Ruin")
        self.assertEqual(self.quest.opposition, "Rivals")
        self.assertEqual(self.quest.source, "Cleric")
        self.assertEqual(self.quest.reward, "Gold")

    def test_quest_str(self):
        """Test quest string representation"""
        expected = (
            "You must locate a treasure at ruin held by rivals. "
            "Request was given by cleric and offered gold."
        )
        self.assertEqual(str(self.quest), expected)

    def test_quest_to_dict(self):
        """Test quest conversion to dictionary"""
        quest_dict = self.quest.to_dict()

        self.assertIsInstance(quest_dict, dict)
        self.assertIn("action", quest_dict)
        self.assertIn("target", quest_dict)
        self.assertIn("where", quest_dict)
        self.assertIn("opposition", quest_dict)
        self.assertIn("source", quest_dict)
        self.assertIn("reward", quest_dict)
        self.assertIn("description", quest_dict)

        self.assertEqual(quest_dict["action"], "Locate")
        self.assertEqual(quest_dict["target"], "Treasure")

    def test_quest_formatted_display(self):
        """Test quest formatted display"""
        display = self.quest.formatted_display()

        self.assertIsInstance(display, str)
        self.assertIn("QUEST", display)
        self.assertIn("Action:", display)
        self.assertIn("Target:", display)
        self.assertIn("Location:", display)
        self.assertIn("Opposition:", display)
        self.assertIn("Source:", display)
        self.assertIn("Reward:", display)
        self.assertIn("Description:", display)


class TestGenerateQuest(unittest.TestCase):
    """Test quest generation functions"""

    def test_generate_quest_returns_quest_object(self):
        """Test that generate_quest returns a Quest object"""
        quest = generate_quest()
        self.assertIsInstance(quest, Quest)

    def test_generate_quest_has_all_attributes(self):
        """Test that generated quest has all required attributes"""
        quest = generate_quest()

        self.assertIsNotNone(quest.action)
        self.assertIsNotNone(quest.target)
        self.assertIsNotNone(quest.where)
        self.assertIsNotNone(quest.opposition)
        self.assertIsNotNone(quest.source)
        self.assertIsNotNone(quest.reward)

    def test_generate_quest_has_valid_values(self):
        """Test that generated quest has valid values from tables"""
        quest = generate_quest()

        # Check that values are strings
        self.assertIsInstance(quest.action, str)
        self.assertIsInstance(quest.target, str)
        self.assertIsInstance(quest.where, str)
        self.assertIsInstance(quest.opposition, str)
        self.assertIsInstance(quest.source, str)
        self.assertIsInstance(quest.reward, str)

        # Check that values are not empty
        self.assertGreater(len(quest.action), 0)
        self.assertGreater(len(quest.target), 0)
        self.assertGreater(len(quest.where), 0)
        self.assertGreater(len(quest.opposition), 0)
        self.assertGreater(len(quest.source), 0)
        self.assertGreater(len(quest.reward), 0)

    def test_generate_quest_variability(self):
        """Test that generate_quest produces different quests"""
        quests = [generate_quest() for _ in range(20)]

        # Check that we got some variety (not all identical)
        quest_strings = [str(q) for q in quests]
        unique_quests = set(quest_strings)

        # With 20 quests, we should have at least a few unique ones
        self.assertGreater(len(unique_quests), 1)

    def test_generate_quest_str_format(self):
        """Test that generated quest string follows expected format"""
        quest = generate_quest()
        quest_str = str(quest)

        self.assertIn("You must", quest_str)
        self.assertIn("held by", quest_str)
        self.assertIn("Request was given by", quest_str)
        self.assertIn("offered", quest_str)


class TestGenerateMultipleQuests(unittest.TestCase):
    """Test generating multiple quests"""

    def test_generate_multiple_quests_returns_list(self):
        """Test that generate_multiple_quests returns a list"""
        quests = generate_multiple_quests(3)
        self.assertIsInstance(quests, list)
        self.assertEqual(len(quests), 3)

    def test_generate_multiple_quests_all_quest_objects(self):
        """Test that all returned items are Quest objects"""
        quests = generate_multiple_quests(5)

        for quest in quests:
            self.assertIsInstance(quest, Quest)

    def test_generate_multiple_quests_custom_count(self):
        """Test generating custom number of quests"""
        for count in [1, 3, 5, 10]:
            quests = generate_multiple_quests(count)
            self.assertEqual(len(quests), count)

    def test_generate_multiple_quests_variability(self):
        """Test that multiple quests have some variability"""
        quests = generate_multiple_quests(10)
        quest_strings = [str(q) for q in quests]
        unique_quests = set(quest_strings)

        # We should have at least some variety
        self.assertGreater(len(unique_quests), 1)


class TestDisplayQuestWithClues(unittest.TestCase):
    """Test quest generation with clue checking"""

    def test_display_quest_with_clues_returns_tuple(self):
        """Test that function returns a tuple"""
        result = display_quest_with_clues()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)

    def test_display_quest_with_clues_structure(self):
        """Test the structure of returned values"""
        quest, has_clues, clue_type, clue_detail = display_quest_with_clues()

        # Check types
        self.assertIsInstance(quest, Quest)
        self.assertIsInstance(has_clues, bool)
        self.assertIsInstance(clue_type, str)

        # Check clue_type values
        self.assertIn(clue_type, ["No", "Narrative Shift", "Clues"])

        # If has_clues is True, clue_detail should not be None
        if has_clues:
            self.assertIsNotNone(clue_detail)
            self.assertIsInstance(clue_detail, str)

        # If has_clues is False, clue_type should be "No"
        if not has_clues:
            self.assertEqual(clue_type, "No")
            self.assertIsNone(clue_detail)

    def test_display_quest_with_clues_quest_validity(self):
        """Test that the quest part is valid"""
        quest, _, _, _ = display_quest_with_clues()

        self.assertIsNotNone(quest.action)
        self.assertIsNotNone(quest.target)
        self.assertIsNotNone(quest.where)
        self.assertIsNotNone(quest.opposition)
        self.assertIsNotNone(quest.source)
        self.assertIsNotNone(quest.reward)


class TestQuestIntegration(unittest.TestCase):
    """Integration tests for quest generation"""

    def test_quest_generation_pipeline(self):
        """Test the full quest generation pipeline"""
        # Generate quest
        quest = generate_quest()

        # Convert to dict
        quest_dict = quest.to_dict()

        # Create new quest from dict values
        new_quest = Quest(
            action=quest_dict["action"],
            target=quest_dict["target"],
            where=quest_dict["where"],
            opposition=quest_dict["opposition"],
            source=quest_dict["source"],
            reward=quest_dict["reward"]
        )

        # Check that the two quests are equivalent
        self.assertEqual(str(quest), str(new_quest))

    def test_quest_batch_generation(self):
        """Test generating a batch of quests"""
        batch_size = 10
        quests = generate_multiple_quests(batch_size)

        # Check all quests are valid
        for quest in quests:
            # Each quest should have a valid string representation
            quest_str = str(quest)
            self.assertIsInstance(quest_str, str)
            self.assertGreater(len(quest_str), 50)  # Should be reasonably long

            # Each quest should have a valid dict representation
            quest_dict = quest.to_dict()
            self.assertEqual(len(quest_dict), 7)  # 6 fields + description


if __name__ == "__main__":
    unittest.main()
