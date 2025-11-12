# Quest Generator

A quest generation system for RPG games that uses the 6 quest tables from the Overland game system to create randomized, procedural quests.

## Quest Format

Each quest follows this template:
```
You must <ACTION> a <TARGET> at <WHERE> held by <OPPOSITION>.
Request was given by <SOURCE> and offered <REWARD>.
```

## Quest Tables

The generator uses these 6 tables from `overland_tables.py`:

1. **QUEST_ACTION** (d6): Locate, Deliver, Explore, Destroy, Rescue, Protect
2. **QUEST_TARGET** (d6): Treasure, Item, Location, Enemy, NPC, Message
3. **QUEST_WHERE** (d6): Ruin, Forest, Castle, Cave, City, Mountain
4. **QUEST_OPPOSITION** (d6): Rivals, Soldiers, Bandits, Monsters, Spy, Cult
5. **QUEST_SOURCE** (d6): Cleric, Mayor, Friend, Wizard, Witch, Rumor
6. **QUEST_REWARD** (d6): Gold, Silver, NPC, Secret, Item(Spc.), Item(Spc.)

## Quick Start

### Basic Usage

```python
from quest_generator import generate_quest

# Generate a single quest
quest = generate_quest()
print(quest)
# Output: You must locate a treasure at ruin held by rivals.
#         Request was given by cleric and offered gold.
```

### Generate Multiple Quests

```python
from quest_generator import generate_multiple_quests

# Generate a quest board with 5 quests
quests = generate_multiple_quests(5)
for i, quest in enumerate(quests, 1):
    print(f"{i}. {quest}")
```

### Formatted Display

```python
quest = generate_quest()
print(quest.formatted_display())

# Output:
# ============================================================
# QUEST
# ============================================================
#   Action:      Locate
#   Target:      Treasure
#   Location:    Ruin
#   Opposition:  Rivals
#   Source:      Cleric
#   Reward:      Gold
# ------------------------------------------------------------
# Description:
#   You must locate a treasure at ruin held by rivals.
#   Request was given by cleric and offered gold.
# ============================================================
```

### Quest with Clue Discovery

```python
from quest_generator import display_quest_with_clues

quest, has_clues, clue_type, clue_detail = display_quest_with_clues()

print(quest)
if has_clues:
    print(f"Clue found: {clue_detail}")
```

### Export as Dictionary

```python
quest = generate_quest()
quest_dict = quest.to_dict()

# Returns:
# {
#     "action": "Locate",
#     "target": "Treasure",
#     "where": "Ruin",
#     "opposition": "Rivals",
#     "source": "Cleric",
#     "reward": "Gold",
#     "description": "You must locate a treasure at..."
# }
```

## Quest Class

The `Quest` class has the following attributes:

- `action`: The action to perform (e.g., "Locate", "Rescue")
- `target`: What to find/rescue/destroy (e.g., "Treasure", "NPC")
- `where`: The location (e.g., "Ruin", "Castle")
- `opposition`: Who holds it (e.g., "Rivals", "Bandits")
- `source`: Who gave the quest (e.g., "Cleric", "Wizard")
- `reward`: What you'll receive (e.g., "Gold", "Item(Spc.)")

### Methods

- `__str__()`: Returns the full quest description
- `to_dict()`: Converts quest to dictionary
- `formatted_display()`: Returns a nicely formatted display string

## Examples

See `quest_example.py` for complete examples including:
- Simple quest generation
- Quest board with multiple quests
- Quest with clue discovery
- Exporting quests as JSON
- Filtering quests by criteria
- Generating quest campaigns

## Running Examples

```bash
# Run the main quest generator
python3 quest_generator.py

# Run interactive examples
python3 quest_example.py
```

## Testing

The quest generator has comprehensive unit tests:

```bash
# Run quest generator tests
python3 -m unittest tests.test_quest_generator -v

# Run all tests
python3 -m unittest discover tests
```

## Integration with Game Systems

The quest generator integrates with:
- **overland_tables.py**: Source of quest tables
- **table_roller.py**: Dice rolling system
- All other Overland game tables (for clue discovery, narrative shifts, etc.)

## Example Output

```
You must protect a message at city held by bandits.
Request was given by wizard and offered silver.

You must rescue a treasure at ruin held by spy.
Request was given by mayor and offered silver.

You must explore a item at cave held by monsters.
Request was given by rumor and offered gold.
```

## Customization

To create custom quest types, you can:

1. **Filter generated quests:**
```python
# Keep generating until you get a rescue quest
while True:
    quest = generate_quest()
    if quest.action == "Rescue":
        break
```

**Create custom Quest objects:**
```python
from quest_generator import Quest

custom_quest = Quest(
    action="Investigate",
    target="Mystery",
    where="Haunted Manor",
    opposition="Ghosts",
    source="Local Villagers",
    reward="Ancient Artifact"
)
```

## License

Part of the RPG Game project. Uses tables from Single Sheet Overland Game System by Perplexing Ruins.
