"""
Single Sheet Overland Game System - Reference Tables
All tables extracted from the Overland PDF for programmatic access
"""

# Import table roller utilities for convenience

# ============================================================================
# EXPLORATION TABLES
# ============================================================================

EXPLORE_DIE = {
    1: "Nothing",
    2: "Spoor",
    3: "Discovery",
    4: "Discovery",
    5: "Danger",
    6: "Danger"
}

TERRAIN = {
    1: "Grasslands",
    2: "Woods",
    3: "Hills",
    4: "Mountains",
    5: "Swamp",
    6: "Wasteland"
}

NEW_TERRAIN = {
    1: "Same",
    2: "Same",
    3: "Same",
    4: "Same",
    5: "New",
    6: "New"
}

WATER = {
    1: "None",
    2: "None",
    3: "None",
    4: "None",
    5: "River",
    6: "Lake"
}

WEATHER = {
    1: "Overcast",
    2: "Sunny",
    3: "Fog",
    4: "Rain",
    5: "Thunderstorm",
    6: "Snow"
}

# ============================================================================
# DISCOVERY TABLES
# ============================================================================

DISCOVERY = {
    1: "Unnatural",
    2: "Natural",
    3: "Ruin",
    4: "Settlement",
    5: "Evidence",
    6: "Passive"
}

DISCOVERY_UNNATURAL = {
    1: "Portal",
    2: "Glowing",
    3: "Residue",
    4: "Cursed",
    5: "Scorching",
    6: "Mutation"
}

DISCOVERY_NATURAL = {
    1: "Cave",
    2: "Landmark",
    3: "Nest",
    4: "Water",
    5: "Grove",
    6: "Ravine"
}

DISCOVERY_RUIN = {
    1: "Tower",
    2: "Castle",
    3: "Barrow",
    4: "Dungeon",
    5: "Dungeon",
    6: "Dungeon"
}

DISCOVERY_SETTLEMENT = {
    1: "Refugee",
    2: "Village",
    3: "Village",
    4: "Town",
    5: "Outpost",
    6: "City"
}

DISCOVERY_EVIDENCE = {
    1: "Tracks",
    2: "Camp",
    3: "Bones",
    4: "Tools",
    5: "Supplies",
    6: "Violence"
}

DISCOVERY_PASSIVE = {
    1: "Refugee",
    2: "Merchant",
    3: "Merchant",
    4: "Camp",
    5: "Bard",
    6: "Animal"
}

# ============================================================================
# DANGER TABLES
# ============================================================================

DANGER = {
    1: "Unnatural",
    2: "Unnatural",
    3: "Hazard",
    4: "Hazard",
    5: "Hostile",
    6: "Hostile"
}

DANGER_UNNATURAL = {
    1: "Ghoul",
    2: "Zombie",
    3: "Skeleton",
    4: "Demon",
    5: "Elemental",
    6: "Wraith"
}

DANGER_HAZARD = {
    1: "Bog",
    2: "Landslide",
    3: "Sinkhole",
    4: "Poison",
    5: "Resources",
    6: "Ambush"
}

# ============================================================================
# DETAIL TABLES
# ============================================================================

DETAILS = {
    1: "Ruined",
    2: "Rotting",
    3: "Blocked",
    4: "Odorous",
    5: "Sealed",
    6: "Sunken"
}

THEME = {
    1: "Haunted",
    2: "Infested",
    3: "Mystical",
    4: "Ancient",
    5: "Defended",
    6: "Corrupted"
}

OCCUPANT_ACTIVITY = {
    1: "Hiding",
    2: "Exploring",
    3: "Guarding",
    4: "Hunting",
    5: "Sacrificing",
    6: "Taking"
}

SPOOR = {
    1: "Foul odor",
    2: "Monster tracks",
    3: "Black smoke",
    4: "Carrion birds",
    5: "War sounds",
    6: "Human tracks"
}

# ============================================================================
# ENCOUNTER REACTION TABLES
# ============================================================================

REACTION = {
    1: "Helpful",
    2: "Curious",
    3: "Indifferent",
    4: "Wary",
    5: "Rude",
    6: "Hostile"
}

DISTANCE = {
    1: "At hand",
    2: "Close",
    3: "Middle",
    4: "Middle",
    5: "Range",
    6: "Horizon"
}

DEGREE = {
    1: "Bad/Small",
    2: "Bad/Small",
    3: "Bad/Small",
    4: "Good/Large",
    5: "Good/Large",
    6: "Good/Large"
}

# ============================================================================
# LOOT TABLES
# ============================================================================

LOOT_HUMANS_NOIDS = {
    1: "Nothing",
    2: "Nothing",
    3: "Nothing",
    4: "Mundane item",
    5: "Special item",
    6: "2d6 silver pieces"
}

LOOT_ANIMALS = {
    1: "Nothing",
    2: "Nothing",
    3: "Nothing",
    4: "Mundane part",
    5: "Mundane part",
    6: "Rare part"
}

LOOT_MONSTERS = {
    1: "Nothing",
    2: "Nothing",
    3: "Nothing",
    4: "Mundane part (*1sp)",
    5: "Rare part (*3sp)",
    6: "1d6 gems (1gp/ea)"
}

LOOT_UNNATURAL = {
    1: "Nothing",
    2: "Nothing",
    3: "Nothing",
    4: "Minor healing elixir",
    5: "Major healing elixir",
    6: "Rare elixir"
}

# ============================================================================
# COMMERCE - TRAVEL
# ============================================================================

TRAVEL = {
    1: {"name": "Horse", "cost_sp": 10},
    2: {"name": "Cart", "cost_sp": 10},
    3: {"name": "Ferry", "cost_sp": 5},
    4: {"name": "Boat Passage", "cost_sp": 10}
}

# ============================================================================
# COMMERCE - HELP
# ============================================================================

HELP = {
    1: {"name": "Warrior", "cost_sp_per_day": 20},
    2: {"name": "Archer", "cost_sp_per_day": 20},
    3: {"name": "Healer", "cost_sp_per_day": 500},
    4: {"name": "Porter", "cost_sp_per_day": 10}
}

# ============================================================================
# COMMERCE - HERBALIST
# ============================================================================

HERBALIST = {
    1: {"name": "Minor Healing Elixir", "cost_sp": 10, "effect": "Recover 3 Hit Points"},
    2: {"name": "Major Healing Elixir", "cost_sp": 50, "effect": "Recover 6 Hit Points"},
    3: {"name": "Antidote", "cost_sp": 50, "effect": "Cure poison"}
}

# ============================================================================
# COMMERCE - MERCHANT (3sp each)
# ============================================================================

MERCHANT_ITEMS = [
    "Bandages", "Chain", "Chalk", "Compass", "Fishing Rod",
    "Flint and Steel", "Garlic", "Grapple Hook", "Hammer",
    "Lantern", "Needle", "Net", "Parchment", "Pole", "Ration",
    "Repellent", "Rope", "Sack", "Saw", "Shovel", "Spikes",
    "Tent", "Lockpicks", "Waterskin"
]

MERCHANT_COST_SP = 3

# ============================================================================
# COMMERCE - ARMORER - WEAPONS
# ============================================================================

WEAPONS = {
    "dagger": {"damage": "d6", "cost_sp": 100, "bulky": False},
    "short_sword": {"damage": "d6", "cost_sp": 100, "bulky": False},
    "hand_axe": {"damage": "d6", "cost_sp": 100, "bulky": False},
    "sling": {"damage": "d6", "cost_sp": 100, "bulky": False},
    "staff": {"damage": "d6", "cost_sp": 100, "bulky": False},
    "long_sword": {"damage": "2d6 (take higher)", "cost_sp": 200, "bulky": False},
    "spear": {"damage": "2d6 (take higher)", "cost_sp": 200, "bulky": False},
    "mace": {"damage": "2d6 (take higher)", "cost_sp": 200, "bulky": False},
    "halberd": {"damage": "2d6 (take higher)", "cost_sp": 200, "bulky": False},
    "warhammer": {"damage": "d8", "cost_sp": 200, "bulky": True},
    "great_sword": {"damage": "d8", "cost_sp": 200, "bulky": True},
    "battle_axe": {"damage": "d8", "cost_sp": 200, "bulky": True},
    "bow": {"damage": "2d6 (take higher)", "cost_sp": 150, "bulky": False},
    "crossbow": {"damage": "d8", "cost_sp": 200, "bulky": True},
    "quiver": {"damage": "N/A", "cost_sp": 50, "arrows": 20, "bulky": False}
}

# ============================================================================
# COMMERCE - ARMORER - ARMOR
# ============================================================================

ARMOR = {
    "leather": {"ac_bonus": 2, "cost_sp": 50, "bulky": False},
    "chain": {"ac_bonus": 3, "cost_sp": 300, "bulky": True},
    "plate": {"ac_bonus": 4, "cost_sp": 400, "bulky": True},
    "helmet": {"ac_bonus": 1, "cost_sp": 100, "bulky": False},
    "shield": {"ac_bonus": 1, "cost_sp": 50, "bulky": False}
}

# ============================================================================
# COMMERCE - INN
# ============================================================================

INN = {
    1: {"name": "Simple room", "cost_sp": 5},
    2: {"name": "Fine room", "cost_sp": 5},
    3: {"name": "Meal", "cost_sp": 1},
    4: {"name": "Fine meal", "cost_sp": 2},
    5: {"name": "Ale", "cost_sp": 1}
}

# ============================================================================
# TRAVELING ENCOUNTERS (2d6 & d6)
# ============================================================================

TRAVELING_ENCOUNTERS = {
    2: "A large tree: [1-2] hung with something [3-4] radiating light or sound [5-6] opens when approached",
    3: "A mystical glade: [1-2] radiates calm [3-4] causes sleep [5-6] induces forgetfulness",
    4: "A field of mushrooms: [1-2] that are poisonous [3-4] that satiate hunger [5-6] that give strength",
    5: "A man locked in a cage: [1-2] that promises to help if let out [3-4] that promises treasure if let out [5-6] "
       "that speaks of revenge",
    6: "A procession: [1-2] of refugees [3-4] of soldiers [5-6] of performers",
    7: "A soldier: [1-2] loots the corpse of another soldier [3-4] tries to make his donkey proceed [5-6] is fending "
       "off hostile monsters",
    8: "A small camp of hunters: [1-2] welcomes you [3-4] stands and threatens you [5-6] asks for your help with a "
       "problem",
    9: "A patrol of d6 creatures: [1-2] escorts captives [3-4] argues over an abandoned cart [5-6] harasses a group of"
       " travelers",
    10: "A raucous crowd is gathered: [1-2] shouting for death [3-4] shouting for forgiveness [5-6] shouting in"
        " disbelief",
    11: "A merchant that sells: [1-2] Minor Healing Elixirs [3-4] Mundane items [5-6] Special Items",
    12: "A scarred woman: [1-2] offers to trade food for a weapon [3-4] speaks of a wizard in a tower [5-6] roasts a"
        " monster over a fire"
}

# ============================================================================
# CHARACTER GENERATION
# ============================================================================

RACE = {
    1: "Human",
    2: "Human",
    3: "Human",
    4: "Halfling",
    5: "Elf",
    6: "Dwarf"
}

CHARACTER_TYPE = {
    1: "Magic User",
    2: "Adventurer",
    3: "Merchant",
    4: "Soldier",
    5: "Noble",
    6: "Commoner"
}

FINANCIAL = {
    1: "Very poor",
    2: "Poor",
    3: "Modest",
    4: "Modest",
    5: "Rich",
    6: "Very rich"
}

CARRIES = {
    1: "Exotic pet",
    2: "Much gold",
    3: "Cursed item",
    4: "Map fragment",
    5: "Powerful key",
    6: "Ancient ring"
}

SECRET = {
    1: "Is a criminal",
    2: "Is royalty",
    3: "Is famous",
    4: "Location of magic",
    5: "Location of gold",
    6: "Location of NPC"
}

TRAITS_1 = {
    1: "Scarred",
    2: "Stutters",
    3: "Tattooed",
    4: "Dirty",
    5: "Florid",
    6: "Haughty"
}

TRAITS_2 = {
    1: "Cruel",
    2: "Humble",
    3: "Heroic",
    4: "Daring",
    5: "Friendly",
    6: "Greedy"
}

TRAITS_3 = {
    1: "Bald",
    2: "Bearded",
    3: "Greasy",
    4: "Amputee",
    5: "Blind",
    6: "Mute"
}

MOTIVATION = {
    1: "Crime",
    2: "Revenge",
    3: "Adventure",
    4: "Wealth",
    5: "Power",
    6: "Escape"
}

INTERESTS = {
    1: "Treasure",
    2: "Art",
    3: "Music",
    4: "Politics",
    5: "Archaeology",
    6: "Gambling"
}

METHODS = {
    1: "Wit",
    2: "Charm",
    3: "Violence",
    4: "Money",
    5: "Blackmail",
    6: "Sabotage"
}

MALE_NAMES_1 = ["Francis", "Drake", "Morton", "Garth", "Richard", "Aldred"]
MALE_NAMES_2 = ["Storn", "Rildor", "Duncan", "Grindor", "Rudolph", "Bainard"]
MALE_NAMES_3 = ["Razz", "Drint", "Rusk", "Greeteg", "Vlesk", "Zabian"]

FEMALE_NAMES_1 = ["Fiona", "Isolde", "Kate", "Evelyn", "Ronda", "Rebecca"]
FEMALE_NAMES_2 = ["Jean", "Samantha", "Tera", "Olivia", "Elke", "Francis"]
FEMALE_NAMES_3 = ["Vornith", "Trilt", "Ristal", "Wirth", "Nus", "Zeena"]

# ============================================================================
# SETTLEMENT GENERATION
# ============================================================================

SETTLEMENT_PREFIX_1 = ["Storm", "Rock", "Clouded", "Mourn", "New", "High"]
SETTLEMENT_PREFIX_2 = ["Bright", "Thorn", "Hill", "Frost", "Fort", "Low"]
SETTLEMENT_PREFIX_3 = ["Grey", "Great", "Little", "Black", "White", "Stone"]

SETTLEMENT_SUFFIX_1 = ["ville", "moor", "haven", "fall(s)", "field", "ton"]
SETTLEMENT_SUFFIX_2 = ["bridge", "brook", "stead", "wick", "valley", "river"]
SETTLEMENT_SUFFIX_3 = ["mount", "plane", "mire", "wood(s)", "ridge", "mound"]

SETTLEMENT_ADJECTIVE = {
    1: "Harsh",
    2: "Remote",
    3: "Perilous",
    4: "Haunted",
    5: "Ancient",
    6: "Rich"
}

SETTLEMENT_DETAIL = {
    1: "Grimy",
    2: "Ornate",
    3: "Plain",
    4: "Heavy",
    5: "Carved",
    6: "Glows"
}

SETTLEMENT_INDUSTRY = {
    1: "Textiles",
    2: "Agriculture",
    3: "War",
    4: "Religion",
    5: "Mining",
    6: "Economy"
}

SETTLEMENT_CONCERNS = {
    1: "Cult",
    2: "Monster",
    3: "Sorcerer",
    4: "Bandits",
    5: "Soldiers",
    6: "Blight"
}

SETTLEMENT_QUALITY = {
    1: "Worn",
    2: "Poor",
    3: "Quiet",
    4: "Desperate",
    5: "Wealthy",
    6: "Fearful"
}

SETTLEMENT_AVAILABLE = {
    1: "Armorer",
    2: "Inn",
    3: "Inn",
    4: "Merchant",
    5: "Merchant",
    6: "Herbalist"
}

SETTLEMENT_STATUS = {
    1: "Calm",
    2: "War",
    3: "Trade",
    4: "Illness",
    5: "Festival",
    6: "Rebellion"
}

SETTLEMENT_LEADER = {
    1: "Noble",
    2: "Bandits",
    3: "Soldiers",
    4: "Elder",
    5: "Mayor",
    6: "None"
}

# ============================================================================
# ENCOUNTER BY TERRAIN
# ============================================================================

ENCOUNTER_GRASSLANDS = {
    1: "Human",
    2: "Human",
    3: "Animal",
    4: "Animal",
    5: "Humanoid",
    6: "Monster (S)"
}

ENCOUNTER_WOODS = {
    1: "Human",
    2: "Animal",
    3: "Humanoid",
    4: "Humanoid",
    5: "Monster (S)",
    6: "Monster (L)"
}

ENCOUNTER_HILLS = {
    1: "Human",
    2: "Animal",
    3: "Humanoid",
    4: "Monster (S)",
    5: "Monster (L)",
    6: "Monster (L)"
}

ENCOUNTER_MOUNTAINS = {
    1: "Human",
    2: "Animal",
    3: "Humanoid",
    4: "Humanoid",
    5: "Monster (L)",
    6: "Monster (L)"
}

ENCOUNTER_SWAMPS = {
    1: "Human",
    2: "Animal",
    3: "Humanoid",
    4: "Unnatural",
    5: "Unnatural",
    6: "Monster (S)"
}

ENCOUNTER_WASTELANDS = {
    1: "Human",
    2: "Humanoid",
    3: "Humanoid",
    4: "Unnatural",
    5: "Monster (S)",
    6: "Monster (L)"
}

# ============================================================================
# CREATURE STATS
# ============================================================================

CREATURES_HUMAN = {
    1: {"name": "Commoner", "hd": "1", "ac": 10, "special": None},
    2: {"name": "Bandit", "hd": "1", "ac": 12, "special": "Wpn"},
    3: {"name": "Bandit", "hd": "1", "ac": 12, "special": "Wpn"},
    4: {"name": "Soldier", "hd": "1", "ac": 12, "special": "Wpn[+1]"},
    5: {"name": "Berserker", "hd": "1+2", "ac": 12, "special": "Wpn[+1], Berserking"},
    6: {"name": "Mage", "hd": "1+1", "ac": 10, "special": "Dagger[-1], Spell"}
}

CREATURES_ANIMAL = {
    1: {"name": "Fire Beetle", "hd": "1+3", "ac": 15, "attack": "Bite"},
    2: {"name": "Centipede", "hd": "1d2HP", "ac": 10, "attack": "Bite, Poison"},
    3: {"name": "Bear", "hd": "4+1", "ac": 12, "attack": "Claw(d3), Bite[+2]", "na": 1},
    4: {"name": "Giant Rat", "hd": "1-1", "ac": 12, "attack": "Bite, Disease"},
    5: {"name": "Spider", "hd": "2+2", "ac": 13, "attack": "Bite, Poison"},
    6: {"name": "Stirge", "hd": "1-1", "ac": 14, "attack": "Sting, Suck Blood"}
}

CREATURES_HUMANOID = {
    1: {"name": "Goblin", "hd": "1-1", "ac": 13, "attack": "Wpn"},
    2: {"name": "Gnoll", "hd": "2", "ac": 14, "attack": "Bite"},
    3: {"name": "Kobold", "hd": "1/2", "ac": 13, "attack": "Weapon"},
    4: {"name": "Giant", "hd": "10", "ac": 15, "attack": "Wpn(2d6)[+1], Hurls"},
    5: {"name": "Troll", "hd": "6+3", "ac": 15, "attack": "Club[+2], Regeneration"},
    6: {"name": "Orc", "hd": "1", "ac": 13, "attack": "Wpn[+2]"}
}

CREATURES_MONSTER_S = {
    1: {"name": "Wererat", "hd": "3", "ac": 13, "attack": "Wpn, Rats"},
    2: {"name": "Bugbear", "hd": "3+1", "ac": 14, "attack": "Wpn or Bite, Quick Hit"},
    3: {"name": "Blink Dog", "hd": "6", "ac": 14, "attack": "Bite, Teleport"},
    4: {"name": "Hobgoblin", "hd": "1+1", "ac": 14, "attack": "Wpn"},
    5: {"name": "Dryad", "hd": "2", "ac": 14, "attack": "Wpn[-1], Charm"},
    6: {"name": "Werewolf", "hd": "3", "ac": 14, "attack": "Bite or Claw[+1]"}
}

CREATURES_MONSTER_L = {
    1: {"name": "Basilisk", "hd": "6", "ac": 15, "attack": "Bite, Gaze"},
    2: {"name": "Manticore", "hd": "6+4", "ac": 15, "attack": "Bite[+1], Tail Spikes"},
    3: {"name": "Hydra", "hd": "5-12 (# of heads)", "ac": 14, "attack": "Bite/head"},
    4: {"name": "Cockatrice", "hd": "5", "ac": 13, "attack": "Bite, Petrify"},
    5: {"name": "Owlbear", "hd": "5", "ac": 14, "attack": "Claw x2(d3) or Bite(2d6)"},
    6: {"name": "Wyvern", "hd": "7", "ac": 16, "attack": "Bite or Sting, Fly, Poison"}
}

CREATURES_UNNATURAL = {
    1: {"name": "Skeleton", "hd": "1/2", "ac": 11, "attack": "Wpn"},
    2: {"name": "Zombie", "hd": "1", "ac": 11, "attack": "Strike, Immune Sleep"},
    3: {"name": "Ghoul", "hd": "2", "ac": 13, "attack": "Claw, Paralyze"},
    4: {"name": "Demon", "hd": "3", "ac": 16, "attack": "Tail Sting, Immune Wpn"},
    5: {"name": "Wight", "hd": "3", "ac": 14, "attack": "Claw(1hp + Lvl drain)"},
    6: {"name": "Wraith", "hd": "4", "ac": 16, "attack": "Touch(1d6 + Lvl drain)"}
}

# Note: Skeletons & Zombies: d6 always appear
# Human: d4, Animal: d6, Humanoid: d4, Monster(S): d2, Monster(L): 1, Unnatural: 1

# ============================================================================
# MUNDANE ITEMS (Grid 11-66) (Roll 2 d6. 1st die is 10's place, 2nd is 1's place)
# ============================================================================

MUNDANE_ITEMS = {
    11: "Candle", 12: "Tin of wax", 13: "Hammer", 14: "Lockpicks", 15: "Pocketknife", 16: "Ball of yarn",
    21: "Waterskin", 22: "Marbles", 23: "Fine cloak", 24: "Poetry", 25: "Ink pot", 26: "Pot of grease",
    31: "Deck of cards", 32: "Playing dice", 33: "Handsaw", 34: "Tent", 35: "Needle", 36: "Sack of nails",
    41: "Necklace", 42: "Rabbit foot", 43: "Red ribbon", 44: "Ring", 45: "Spear tip", 46: "Fruit bread",
    51: "Comb", 52: "Torch", 53: "Belt", 54: "Warm Hat", 55: "Fishing rod", 56: "Parchment",
    61: "Dried fruit", 62: "Healing herbs", 63: "Antidote vial", 64: "Quiver/arrows", 65: "Flint & steel",
    66: "Magni-Glass"
}

# Special notes:
# 34 (Tent): Heal all Party Hit Points when in Wilderness
# 62 (Healing herbs): Heal 1 HP

# ============================================================================
# SPECIAL ITEMS (Grid 11-66)
# ============================================================================

SPECIAL_ITEMS = {
    11: "Orb", 12: "Ring", 13: "Carpet", 14: "Boots", 15: "Sword", 16: "Helmet",
    21: "Dart", 22: "Key", 23: "Playing cards", 24: "Spellbook", 25: "Cloak", 26: "Shield",
    31: "Elixir", 32: "Shard", 33: "Bag", 34: "d20 Silver", 35: "Flute", 36: "Wand",
    41: "Staff", 42: "Spellbook", 43: "Pouch", 44: "Ring", 45: "Cup", 46: "Arrow",
    51: "Scroll", 52: "Bracelet", 53: "Earrings", 54: "Feather", 55: "Amulet", 56: "Mask",
    61: "Scroll", 62: "Dagger", 63: "d20 Gold", 64: "Gloves", 65: "d6 Gems", 66: "Animal"
}

# ============================================================================
# MAGICAL ITEM EFFECTS (Grid 11-66)
# ============================================================================

MAGICAL_ITEM_EFFECTS = {
    11: "+1", 12: "+1", 13: "+2", 14: "+0", 15: "-1", 16: "-1",
    21: "Speed", 22: "Light", 23: "Levitation", 24: "Perception", 25: "Damage", 26: "Shielding",
    31: "Locating", 32: "Holding", 33: "Growth", 34: "Devouring", 35: "Charming", 36: "Poison",
    41: "Opening", 42: "Fire", 43: "Ice", 44: "Piercing", 45: "Sleep", 46: "Strength",
    51: "Shrinking", 52: "Antidote", 53: "Control", 54: "Water", 55: "Wisdom", 56: "Healing",
    61: "Curse", 62: "Life", 63: "Power", 64: "Weight", 65: "Gravity", 66: "Animal"
}

# ============================================================================
# SOLO ENGINE
# ============================================================================

ORACLE = {
    1: "Extreme no",
    2: "Moderate no",
    3: "Narrative Shift",
    4: "Moderate yes",
    5: "Moderate yes",
    6: "Extreme yes"
}

NARRATIVE_SHIFT = {
    1: "Good NPC appears",
    2: "Info revealed",
    3: "Bad event occurs",
    4: "Bad NPC appears",
    5: "Object introduced",
    6: "Environment Changes"
}

CLUES = {
    1: "Documents",
    2: "Rumor",
    3: "Identity",
    4: "Weakness",
    5: "Location",
    6: "Key"
}

SOLO_DETAIL = {
    1: "Grimy",
    2: "Ornate",
    3: "Plain",
    4: "Heavy",
    5: "Carved",
    6: "Glows"
}

SOLO_NOUN = {
    1: "Person",
    2: "Object",
    3: "Creature",
    4: "Location",
    5: "Resource",
    6: "Belief"
}

SOLO_VERB = {
    1: "Betray",
    2: "Corrupt",
    3: "Control",
    4: "Attack",
    5: "Attain",
    6: "Surprise"
}

SOLO_THEME = {
    1: "Community",
    2: "Power",
    3: "Wealth",
    4: "Nature",
    5: "Spirit",
    6: "Growth"
}

# ============================================================================
# NPC INTERACTION
# ============================================================================

NPC_CONCERNS = {
    1: "Followed",
    2: "Recover",
    3: "Locate",
    4: "War",
    5: "Lost",
    6: "Creature"
}

NPC_BEARING = {
    1: "Flustered",
    2: "Anxious",
    3: "Jovial",
    4: "Paranoid",
    5: "Desperate",
    6: "Hostile"
}

NPC_TOPIC = {
    1: "Weather",
    2: "Festival",
    3: "Rumor",
    4: "History",
    5: "Arcane",
    6: "Creature"
}

NPC_METHODS = {
    1: "Wit",
    2: "Charm",
    3: "Violence",
    4: "Money",
    5: "Blackmail",
    6: "Sabotage"
}

# ============================================================================
# QUESTS
# ============================================================================

QUEST_ACTION = {
    1: "Locate",
    2: "Deliver",
    3: "Explore",
    4: "Destroy",
    5: "Rescue",
    6: "Protect"
}

QUEST_OPPOSITION = {
    1: "Rivals",
    2: "Soldiers",
    3: "Bandits",
    4: "Monsters",
    5: "Spy",
    6: "Cult"
}

QUEST_TARGET = {
    1: "Treasure",
    2: "Item",
    3: "Location",
    4: "Enemy",
    5: "NPC",
    6: "Message"
}

QUEST_WHERE = {
    1: "Ruin",
    2: "Forest",
    3: "Castle",
    4: "Cave",
    5: "City",
    6: "Mountain"
}

QUEST_REWARD = {
    1: "Gold",
    2: "Silver",
    3: "NPC",
    4: "Secret",
    5: "Item(Spc.)",
    6: "Item(Spc.)"
}

QUEST_SOURCE = {
    1: "Cleric",
    2: "Mayor",
    3: "Friend",
    4: "Wizard",
    5: "Witch",
    6: "Rumor"
}

CLUE_FOUND = {
    1: "No",
    2: "No",
    3: "No",
    4: "No",
    5: "Narrative Shift",
    6: "Clues"
}

# ============================================================================
# CURRENCY
# ============================================================================

# 10 Silver Pieces = 1 Gold Piece
SILVER_TO_GOLD_RATIO = 10
