"""
Example usage of the overland_tables module
"""

from tables import overland_tables
from tables.table_roller import roll_on_table, get_all_table_names, roll_d6, roll_2d6, roll_d66

# Example 1: Roll on various tables
print("=== Example Table Rolls ===\n")

print(f"Terrain: {roll_on_table(overland_tables.TERRAIN)}")
print(f"Weather: {roll_on_table(overland_tables.WEATHER)}")
print(f"Explore Die: {roll_on_table(overland_tables.EXPLORE_DIE)}")
print(f"Discovery: {roll_on_table(overland_tables.DISCOVERY)}")
print(f"Danger: {roll_on_table(overland_tables.DANGER)}")
print(f"Reaction: {roll_on_table(overland_tables.REACTION)}")

print("\n=== Character Generation ===\n")
print(f"Race: {roll_on_table(overland_tables.RACE)}")
print(f"Type: {roll_on_table(overland_tables.CHARACTER_TYPE)}")
print(f"Financial Status: {roll_on_table(overland_tables.FINANCIAL)}")
print(f"Trait 1: {roll_on_table(overland_tables.TRAITS_1)}")
print(f"Trait 2: {roll_on_table(overland_tables.TRAITS_2)}")
print(f"Motivation: {roll_on_table(overland_tables.MOTIVATION)}")

print("\n=== Settlement Generation ===\n")
prefix = roll_on_table(overland_tables.SETTLEMENT_PREFIX_1)
suffix = roll_on_table(overland_tables.SETTLEMENT_SUFFIX_1)
print(f"Settlement Name: {prefix}{suffix}")
print(f"Industry: {roll_on_table(overland_tables.SETTLEMENT_INDUSTRY)}")
print(f"Quality: {roll_on_table(overland_tables.SETTLEMENT_QUALITY)}")
print(f"Status: {roll_on_table(overland_tables.SETTLEMENT_STATUS)}")

print("\n=== Loot Rolls ===\n")
print(f"Loot from Human: {roll_on_table(overland_tables.LOOT_HUMANS_NOIDS)}")
print(f"Loot from Animal: {roll_on_table(overland_tables.LOOT_ANIMALS)}")
print(f"Loot from Monster: {roll_on_table(overland_tables.LOOT_MONSTERS)}")

print("\n=== Item Rolls (d66) ===\n")
print(f"Mundane Item: {roll_on_table(overland_tables.MUNDANE_ITEMS)}")
print(f"Special Item: {roll_on_table(overland_tables.SPECIAL_ITEMS)}")
print(f"Magical Effect: {roll_on_table(overland_tables.MAGICAL_ITEM_EFFECTS)}")

print("\n=== Quest Generation ===\n")
print(f"Action: {roll_on_table(overland_tables.QUEST_ACTION)}")
print(f"Target: {roll_on_table(overland_tables.QUEST_TARGET)}")
print(f"Where: {roll_on_table(overland_tables.QUEST_WHERE)}")
print(f"Opposition: {roll_on_table(overland_tables.QUEST_OPPOSITION)}")
print(f"Reward: {roll_on_table(overland_tables.QUEST_REWARD)}")
print(f"Source: {roll_on_table(overland_tables.QUEST_SOURCE)}")

print("\n=== Encounter by Terrain ===\n")
terrain = roll_on_table(overland_tables.TERRAIN)
print(f"Current Terrain: {terrain}")
if terrain == "Grasslands":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_GRASSLANDS)}")
elif terrain == "Woods":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_WOODS)}")
elif terrain == "Hills":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_HILLS)}")
elif terrain == "Mountains":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_MOUNTAINS)}")
elif terrain == "Swamp":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_SWAMPS)}")
elif terrain == "Wasteland":
    print(f"Encounter Type: {roll_on_table(overland_tables.ENCOUNTER_WASTELANDS)}")

print("\n=== Manual Dice Rolls ===\n")
print(f"d6 roll: {roll_d6()}")
print(f"2d6 roll: {roll_2d6()}")
print(f"d66 roll: {roll_d66()}")

print("\n=== Available Tables ===\n")
tables = get_all_table_names(overland_tables)
print(f"Total tables available: {len(tables)}")
print("First 10 tables:", ", ".join(tables[:10]))
