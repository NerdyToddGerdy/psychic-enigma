"""
Example usage of the quest generator
"""

from generators.quest_generator import (
    generate_quest,
    generate_multiple_quests,
    display_quest_with_clues
)


def example_simple_quest():
    """Example 1: Generate a simple quest"""
    print("=" * 70)
    print("EXAMPLE 1: Simple Quest Generation")
    print("=" * 70)

    quest = generate_quest()
    print(quest.formatted_display())
    print()


def example_multiple_quests():
    """Example 2: Generate multiple quests for quest board"""
    print("=" * 70)
    print("EXAMPLE 2: Quest Board (Multiple Quests)")
    print("=" * 70)

    quests = generate_multiple_quests(5)

    print("\nAvailable Quests:\n")
    for i, quest in enumerate(quests, 1):
        print(f"{i}. {quest}")
        print()


def example_quest_with_clues():
    """Example 3: Generate quest with clue checking"""
    print("=" * 70)
    print("EXAMPLE 3: Quest with Clue Discovery")
    print("=" * 70)

    quest, has_clues, clue_type, clue_detail = display_quest_with_clues()

    print("\n" + quest.formatted_display())
    print()

    if has_clues:
        print("During your journey, you discovered clues!")
        print(f"  Type: {clue_type}")
        print(f"  Detail: {clue_detail}")
    else:
        print("No clues were found during this quest.")
    print()


def example_quest_as_json():
    """Example 4: Get quest as dictionary for storage/API"""
    print("=" * 70)
    print("EXAMPLE 4: Quest as Dictionary (JSON-ready)")
    print("=" * 70)

    quest = generate_quest()
    quest_dict = quest.to_dict()

    print("\nQuest Dictionary:")
    import json
    print(json.dumps(quest_dict, indent=2))
    print()


def example_quest_filtering():
    """Example 5: Generate quests until you find one you like"""
    print("=" * 70)
    print("EXAMPLE 5: Finding Specific Quest Types")
    print("=" * 70)

    print("\nSearching for a 'Rescue' quest at a 'Castle'...")

    attempts = 0
    max_attempts = 50

    while attempts < max_attempts:
        quest = generate_quest()
        attempts += 1

        if quest.action == "Rescue" and quest.where == "Castle":
            print(f"\nFound after {attempts} attempts!")
            print(quest.formatted_display())
            break
    else:
        print(f"\nDidn't find matching quest in {max_attempts} attempts.")
        print("Here's a random quest instead:")
        print(generate_quest().formatted_display())

    print()


def example_quest_campaign():
    """Example 6: Generate a campaign of related quests"""
    print("=" * 70)
    print("EXAMPLE 6: Quest Campaign Chain")
    print("=" * 70)

    print("\nGenerating a 3-quest campaign...\n")

    quests = generate_multiple_quests(3)

    print("QUEST CAMPAIGN: The Dark Prophecy\n")
    print("-" * 70)

    for i, quest in enumerate(quests, 1):
        print(f"\nChapter {i}:")
        print(f"  {quest}")

    print("\n" + "=" * 70)
    print()


def main():
    """Run all examples"""
    examples = [
        example_simple_quest,
        example_multiple_quests,
        example_quest_with_clues,
        example_quest_as_json,
        example_quest_filtering,
        example_quest_campaign
    ]

    for example in examples:
        example()
        input("Press Enter to continue to next example...")
        print("\n\n")


if __name__ == "__main__":
    main()
