# Migration Guide - New Package Structure

## Overview

The project has been reorganized into logical packages for better organization and maintainability.

## Changes

### Directory Structure

**Before:**
```
rpgGame/
├── overland_tables.py
├── dungeon_tables.py
├── table_roller.py
├── quest_generator.py
└── tests/
```

**After:**
```
rpgGame/
├── tables/
│   ├── __init__.py
│   ├── overland_tables.py
│   ├── dungeon_tables.py
│   └── table_roller.py
├── generators/
│   ├── __init__.py
│   └── quest_generator.py
└── tests/
```

## Import Changes

### Tables Module

**Before:**
```python
import overland_tables
import dungeon_tables
from table_roller import roll_on_table, roll_d6
```

**After:**
```python
from tables import overland_tables, dungeon_tables
from tables.table_roller import roll_on_table, roll_d6

# Or use the package-level imports:
from tables import roll_on_table, roll_d6
```

### Generators Module

**Before:**
```python
from quest_generator import generate_quest, Quest
```

**After:**
```python
from generators.quest_generator import generate_quest, Quest

# Or use the package-level imports:
from generators import generate_quest, Quest
```

## Usage Examples

### Rolling on Tables

```python
from tables import overland_tables
from tables.table_roller import roll_on_table

# Roll on a table
terrain = roll_on_table(overland_tables.TERRAIN)
weather = roll_on_table(overland_tables.WEATHER)

print(f"Terrain: {terrain}")
print(f"Weather: {weather}")
```

### Generating Quests

```python
from generators import generate_quest

# Generate a quest
quest = generate_quest()
print(quest)

# Or use the formatted display
print(quest.formatted_display())
```

### Complete Example

```python
from tables import overland_tables, dungeon_tables
from tables.table_roller import roll_on_table, roll_d6
from generators import generate_quest

# Roll on overland tables
print("=== Overland ===")
print(f"Terrain: {roll_on_table(overland_tables.TERRAIN)}")
print(f"Weather: {roll_on_table(overland_tables.WEATHER)}")

# Roll on dungeon tables
print("\n=== Dungeon ===")
print(f"Theme: {roll_on_table(dungeon_tables.THEME)}")
print(f"Type: {roll_on_table(dungeon_tables.DUNGEON_TYPE)}")

# Generate a quest
print("\n=== Quest ===")
quest = generate_quest()
print(quest)
```

## Package-Level Exports

Both packages export commonly used functions at the package level:

### tables Package

```python
from tables import (
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
    get_all_table_names,
    overland_tables,
    dungeon_tables
)
```

### generators Package

```python
from generators import (
    Quest,
    generate_quest,
    generate_multiple_quests,
    display_quest_with_clues
)
```

## Testing

All tests have been updated and continue to pass:

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test module
python3 -m unittest tests.test_table_roller
python3 -m unittest tests.test_quest_generator
```

## Benefits of New Structure

1. **Clear Organization**: Tables and generators are logically separated
2. **Scalability**: Easy to add new generator types or table sets
3. **Maintainability**: Related code is grouped together
4. **Python Best Practices**: Follows standard Python package conventions
5. **Import Clarity**: Clear import paths show where code lives

## Backwards Compatibility

The old import style is no longer supported. All code must be updated to use the new package structure.

## Future Additions

With this structure, you can easily add:

- `generators/character_generator.py` - Generate NPCs
- `generators/dungeon_generator.py` - Generate complete dungeons
- `generators/settlement_generator.py` - Generate settlements
- `tables/custom_tables.py` - Custom table sets
- And more!

Each new generator or table set fits naturally into the package structure.
