"""
Single Sheet Dungeon - Reference Tables
All tables extracted from the Dungeon PDF for programmatic access
"""

# ============================================================================
# DUNGEON GENERATION
# ============================================================================

THEME = {
    1: "Criminal",
    2: "Haunted",
    3: "Infested",
    4: "Unnatural",
    5: "Occult",
    6: "Monster"
}

DUNGEON_TYPE = {
    1: "Cave",
    2: "Crypt",
    3: "Temple",
    4: "Ruin",
    5: "Lair",
    6: "Hideout"
}

ADJECTIVE_1 = {
    1: "Forgotten",
    2: "Hidden",
    3: "Haunted",
    4: "Shattered",
    5: "Dark",
    6: "Cursed"
}

ADJECTIVE_2 = {
    1: "Many",
    2: "Desperate",
    3: "Shallow",
    4: "Frozen",
    5: "Infested",
    6: "Dying"
}

NOUN_1 = {
    1: "Gods",
    2: "Veils",
    3: "Ravens",
    4: "Omens",
    5: "Portals",
    6: "Shadows"
}

NOUN_2 = {
    1: "Stars",
    2: "Truths",
    3: "Deaths",
    4: "Depths",
    5: "Spirits",
    6: "Doom"
}

SIZE = {
    1: "1d6+1 Rooms",
    2: "1d6+1 Rooms",
    3: "2d6+2 Rooms",
    4: "2d6+2 Rooms",
    5: "3d6+3 Rooms",
    6: "3d6+3 Rooms"
}

SPECIAL_ROOMS_COUNT = {
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 3,
    6: 3
}

# ============================================================================
# ROOM & CORRIDOR CONTENTS
# ============================================================================

CORRIDOR = {
    1: "Empty",
    2: "Empty",
    3: "Empty",
    4: "Spoor",
    5: "Danger",
    6: "Danger"
}

ROOM = {
    1: "Empty",
    2: "Spoor",
    3: "Discovery",
    4: "Discovery",
    5: "Danger",
    6: "Danger"
}

SPOOR = {
    1: "Blood",
    2: "Tracks",
    3: "Voices",
    4: "Odor",
    5: "Corpse",
    6: "Knocking"
}

DOOR = {
    1: "Unlocked",
    2: "Stuck",
    3: "Stuck",
    4: "Locked",
    5: "Locked",
    6: "Trapped"
}

# ============================================================================
# DISCOVERIES
# ============================================================================

DISCOVERY = {
    1: "Special Room",
    2: "Special Room",
    3: "Feature",
    4: "Item",
    5: "Treasure A",
    6: "Treasure B"
}

# Note: After rolling Discovery, roll d6: 2-in-6 chance of Danger also

SPECIAL_ROOM_1 = {
    1: "Shrine",
    2: "Library",
    3: "Crypt",
    4: "Trophy",
    5: "Workshop",
    6: "Laboratory"
}

SPECIAL_ROOM_2 = {
    1: "Archive",
    2: "Weapon",
    3: "Ritual",
    4: "Torture",
    5: "Kitchen",
    6: "Throne"
}

FEATURE = {
    1: "Pool",
    2: "Garden",
    3: "River",
    4: "Obelisk",
    5: "Lever",
    6: "Mist"
}

ITEM = {
    1: "Key",
    2: "Torch",
    3: "Junk",
    4: "Tools",
    5: "Weapon",
    6: "Food"
}

TREASURE_A = {
    1: "Weapon",
    2: "3d6 Gold",
    3: "d6 Gems",
    4: "Potion",
    5: "Artifact",
    6: "Scroll"
}


TREASURE_B = {
    1: "Artifact",
    2: "d100 Silver",
    3: "3d6x100 Gold",
    4: "d20 Gems",
    5: "Ring",
    6: "Potion"
}

# ============================================================================
# DANGERS
# ============================================================================

DANGER = {
    1: "Hazard",
    2: "Trap",
    3: "Encounter",
    4: "Monster (T1)",
    5: "Monster (T1)",
    6: "Monster (T2)"
}

HAZARD = {
    1: "Debris",
    2: "Collapse",
    3: "Vapor",
    4: "Resources",
    5: "Toxin",
    6: "Darkness"
}

TRAP = {
    1: "Pit",
    2: "Dart",
    3: "Spike",
    4: "Pendulum",
    5: "Boulder",
    6: "Acid"
}

# Encounter: Roll 2d6 on Encounter Table

REACTION = {
    1: "Helpful",
    2: "Indifferent",
    3: "Rude",
    4: "Hostile",
    5: "Hostile",
    6: "Hostile"
}

# ============================================================================
# DRESSING
# ============================================================================

DRESSING_NATURAL = {
    1: "Dung",
    2: "Moss",
    3: "Dust",
    4: "Crystal",
    5: "Oil",
    6: "Mold"
}

DRESSING_MAN_MADE = {
    1: "Tapestry",
    2: "Graffiti",
    3: "Furniture",
    4: "Mirror",
    5: "Statue",
    6: "Fireplace"
}

DRESSING_LIGHTING = {
    1: "None",
    2: "Candles",
    3: "Sconces",
    4: "Glow",
    5: "Torches",
    6: "Lamps"
}

DRESSING_ODOR = {
    1: "Dung",
    2: "Urine",
    3: "Sweat",
    4: "Smoke",
    5: "Dust",
    6: "Food"
}

DRESSING_ODD = {
    1: "Talking corpse",
    2: "Hazy orb",
    3: "Singing flies",
    4: "Creature egg",
    5: "Helpful ghost",
    6: "Glowing tree"
}

DRESSING_MYSTICAL = {
    1: "Hovering flame",
    2: "Silver pool",
    3: "Metal orb",
    4: "Glowing portal",
    5: "Ritual marks",
    6: "Bloody altar"
}

# ============================================================================
# DESCRIPTIONS
# ============================================================================

DESCRIPTION_1 = {
    1: "High",
    2: "Remote",
    3: "Small",
    4: "Exposed",
    5: "Dark",
    6: "Rough"
}

DESCRIPTION_2 = {
    1: "Shadowy",
    2: "Grim",
    3: "Blocked",
    4: "Ancient",
    5: "Perilous",
    6: "Big"
}

DESCRIPTION_3 = {
    1: "Wide",
    2: "Empty",
    3: "Narrow",
    4: "Foul",
    5: "Dead",
    6: "Barren"
}

DESTRUCTION = {
    1: "Curse",
    2: "Invasion",
    3: "Lich",
    4: "Environment",
    5: "Infestation",
    6: "Plague"
}

BUILDER = {
    1: "Wizard",
    2: "Cult",
    3: "Man",
    4: "Humanoid",
    5: "Monster",
    6: "God"
}

PURPOSE = {
    1: "Mine",
    2: "Portal",
    3: "Crypt",
    4: "Hideout",
    5: "Prison",
    6: "Temple"
}

# ============================================================================
# ENCOUNTERS BY TYPE
# ============================================================================

HUMANOIDS = {
    1: "Acolytes",
    2: "Bandits",
    3: "Bandits",
    4: "Goblins",
    5: "Lizardmen",
    6: "Kobolds"
}

CREATURES = {
    1: "Spiders",
    2: "Centipedes",
    3: "Rats",
    4: "Rats",
    5: "Bugbears",
    6: "Bats"
}

UNNATURAL = {
    1: "Skeletons",
    2: "Ghouls",
    3: "Zombies",
    4: "Zombies",
    5: "Demons",
    6: "Vampires"
}

# ============================================================================
# DUNGEON ENCOUNTERS (2d6)
# ============================================================================
# Special: Roll 6 on 2d6 for Tier 5-6 results in rare encounters
ENCOUNTER_TIER_SPECIAL = {
    1: {"name": "Vampire", "hd": "7-9", "ac": 17, "attack": "Bite, Imn. Wpn, Regen."},
    2: {"name": "Vampire", "hd": "7-9", "ac": 17, "attack": "Bite, Imn. Wpn, Regen."},
    3: {"name": "Death Knight", "hd": "10", "ac": 20, "attack": "Sword(+3), Imn. Wpn"}
}

# ============================================================================
# DENIZENS - 2d6 BY TIER
# ============================================================================

DENIZEN_TIER_1_RANGE_1_2 = {
    2: {"name": "Acolyte", "hd": "1", "ac": 16, "attack": "Wpn"},
    3: {"name": "Centipede", "hd": "1d2HP", "ac": 10, "attack": "Bite, Poison"},
    4: {"name": "Giant Rat", "hd": "1-1", "ac": 12, "attack": "Bite, Disease"},
    5: {"name": "Giant Rat", "hd": "1-1", "ac": 12, "attack": "Bite, Disease"},
    6: {"name": "Spider", "hd": "2+2", "ac": 13, "attack": "Bite, Poison, Web"},
    7: {"name": "Kobold", "hd": "1/2", "ac": 13, "attack": "Weapon"},
    8: {"name": "Skeleton", "hd": "1/2", "ac": 11, "attack": "Wpn"},
    9: {"name": "Skeleton", "hd": "1/2", "ac": 11, "attack": "Wpn"},
    10: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"},
    11: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"},
    12: {"name": "Giant Rat", "hd": "1-1", "ac": 12, "attack": "Bite, Disease"}
}

DENIZEN_TIER_1_RANGE_3_4 = {
    2: {"name": "Giant Bat", "hd": "4", "ac": 12, "attack": "Bite, Disease(50%)"},
    3: {"name": "Ghoul", "hd": "2", "ac": 13, "attack": "Claw, Paralyze"},
    4: {"name": "Carrion Creeper", "hd": "3", "ac": 14, "attack": "Bite(1), Paralyze"},
    5: {"name": "Spider", "hd": "2+2", "ac": 13, "attack": "Bite, Poison, Web"},
    6: {"name": "Spider", "hd": "2+2", "ac": 13, "attack": "Bite, Poison, Web"},
    7: {"name": "Zombie", "hd": "1", "ac": 12, "attack": "Wpn & Shield"},
    8: {"name": "Giant Bat", "hd": "4", "ac": 12, "attack": "Bite, Disease(50%)"},
    9: {"name": "Lizardman", "hd": "2+1", "ac": 14, "attack": "Sword"},
    10: {"name": "Lizardman", "hd": "2+1", "ac": 14, "attack": "Sword"},
    11: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"},
    12: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"}
}

DENIZEN_TIER_1_RANGE_5_6 = {
    2: {"name": "Ghoul", "hd": "2", "ac": 13, "attack": "Claw, Paralyze"},
    3: {"name": "Demon", "hd": "3", "ac": 16, "attack": "Tail Sting, Immune Wpn"},
    4: {"name": "Bugbear", "hd": "3+1", "ac": 14, "attack": "Wpn or Bite"},
    5: {"name": "Grey Ooze", "hd": "3", "ac": 11, "attack": "Strike, Imn. Magic/Steel"},
    6: {"name": "Demon", "hd": "3", "ac": 16, "attack": "Tail Sting, Imn. Wpn"},
    7: {"name": "Giant Centipede", "hd": "4", "ac": 19, "attack": "Bite, Poison"},
    8: {"name": "Gargoyle", "hd": "4", "ac": 14, "attack": "Claw, Fly"},
    9: {"name": "Giant Skeleton", "hd": "2", "ac": 12, "attack": "Wpn"},
    10: {"name": "Minotaur", "hd": "6+4", "ac": 13, "attack": "Wpn(+1)"},
    11: {"name": "Troll", "hd": "6+3", "ac": 15, "attack": "Claw(+2), Regeneration"},
    12: {"name": "Hell Hound", "hd": "5", "ac": 15, "attack": "Bite, Fire(2HP/Rnd.)"}
}

DENIZEN_TIER_2_RANGE_1_2 = {
    2: {"name": "Lizardman", "hd": "2+1", "ac": 14, "attack": "Sword"},
    3: {"name": "Lizardman", "hd": "2+1", "ac": 14, "attack": "Sword"},
    4: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"},
    5: {"name": "Bandit", "hd": "1", "ac": 12, "attack": "Wpn"},
    6: {"name": "Ghoul", "hd": "2", "ac": 13, "attack": "Claw, Paralyze"},
    7: {"name": "Demon", "hd": "3", "ac": 16, "attack": "Tail Sting, Immune Wpn"},
    8: {"name": "Bugbear", "hd": "3+1", "ac": 14, "attack": "Wpn or Bite"},
    9: {"name": "Grey Ooze", "hd": "3", "ac": 11, "attack": "Strike, Imn. Magic/Steel"},
    10: {"name": "Demon", "hd": "3", "ac": 16, "attack": "Tail Sting, Imn. Wpn"},
    11: {"name": "Giant Centipede", "hd": "4", "ac": 19, "attack": "Bite, Poison"},
    12: {"name": "Gargoyle", "hd": "4", "ac": 14, "attack": "Claw, Fly"}
}

DENIZEN_TIER_2_RANGE_3_5 = {
    2: {"name": "Giant Skeleton", "hd": "2", "ac": 12, "attack": "Wpn"},
    3: {"name": "Minotaur", "hd": "6+4", "ac": 13, "attack": "Wpn(+1)"},
    4: {"name": "Troll", "hd": "6+3", "ac": 15, "attack": "Claw(+2), Regeneration"},
    5: {"name": "Hell Hound", "hd": "5", "ac": 15, "attack": "Bite, Fire(2HP/Rnd.)"},
    6: {"name": "Vampire", "hd": "7-9", "ac": 17, "attack": "Bite, Imn. Wpn, Regen."},
    7: {"name": "Vampire", "hd": "7-9", "ac": 17, "attack": "Bite, Imn. Wpn, Regen."},
    8: {"name": "Death Knight", "hd": "10", "ac": 20, "attack": "Sword(+3), Imn. Wpn"},
    9: {"name": "Minotaur", "hd": "6+4", "ac": 13, "attack": "Wpn(+1)"},
    10: {"name": "Troll", "hd": "6+3", "ac": 15, "attack": "Claw(+2), Regeneration"},
    11: {"name": "Hell Hound", "hd": "5", "ac": 15, "attack": "Bite, Fire(2HP/Rnd.)"},
    12: {"name": "Vampire", "hd": "7-9", "ac": 17, "attack": "Bite, Imn. Wpn, Regen."}
}

# ============================================================================
# MONSTER BEHAVIOR
# ============================================================================

ACTIVITY = {
    1: "Eating",
    2: "Sleeping",
    3: "Searching",
    4: "Fighting",
    5: "Preparing",
    6: "Breaking"
}

TACTIC = {
    1: "Taunt",
    2: "Hit & Run",
    3: "Aggressive",
    4: "Mirror",
    5: "Hide",
    6: "Gang up"
}

GUARDING = {
    1: "Hostage",
    2: "Chest",
    3: "Door",
    4: "Trap",
    5: "Cabinet",
    6: "Food"
}

# ============================================================================
# DUNGEON ENCOUNTERS (2d6 & d6)
# ============================================================================

DUNGEON_ENCOUNTERS = {
    2: "An altar: [1-2] with drops of fresh blood [3-4] lid shakes and rattles from inside [5-6] emits a clanging "
       "alarm sound if touched",
    3: "A pool: [1-2] heals d6 HP if sipped from [3-4] causes d4 poison damage if sipped [5-6] grants +1 to melee "
       "weapons washed within for 1 day",
    4: "Glowing fungus: [1-2] that replenishes 1 HP [3-4] that explodes when crushed (d6 dmg) [5-6] that makes a "
       "great lantern",
    5: "A man locked in a cage: [1-2] who swears he is a prophet [3-4] swears he can cast heal (false) [5-6] swears "
       "he can cast heal (true)",
    6: "An adventurer's corpse [1-2] is rigged with a trap (d8 dmg) [3-4] has a purse with d20 coins [5-6] has a "
       "magical cloak (causes shadow camouflage)",
    7: "Two creatures: [1-2] toss something between them as a game [3-4] argue over which should receive an item "
       "between them [5-6] are fighting another two creatures",
    8: "A creature sleeps: [1-2] draped over a chest [3-4] in a doorway [5-6] atop a sarcophagus",
    9: "A lost merchant: [1-2] is catatonic in the corner [3-4] pleads for your help [5-6] attacks in a fit of total"
       " madness",
    10: "Centipedes: [1-2] eat the carcass of a creature [3-4] surround an NPC in a corner [5-6] peck through the"
        " remains of an adventurer and their gear",
    11: "1d4 Adventurers: [1-2] are fighting a Tier 1 Unnatural [3-4] are trying to disarm a trap [5-6] are arguing"
        " about whether to open a treasure chest",
    12: "A large egg: [1-2] emanates warmth and a soft glow [3-4] begins to crack, and the snout of some reptile is"
        " beginning to emerge [5-6] is cracked open, with a trail of blood and slime leading out of the room"
}

# ============================================================================
# LOOT THE CORPSE (d6 tables, 6 columns)
# ============================================================================

LOOT_CORPSE_1 = {
    1: "Bone dice",
    2: "Gold piece",
    3: "Lint",
    4: "Twine",
    5: "Key",
    6: "Cloak"
}

LOOT_CORPSE_2 = {
    1: "Matches",
    2: "Bandanna",
    3: "Kite",
    4: "Potion",
    5: "Soft pillow",
    6: "Oil portrait"
}

LOOT_CORPSE_3 = {
    1: "Lute",
    2: "d6 Silver",
    3: "Belt buckle",
    4: "Worn shield",
    5: "Wrench",
    6: "Scroll"
}

LOOT_CORPSE_4 = {
    1: "Wand",
    2: "Trowel",
    3: "Shovel",
    4: "Hammer",
    5: "Pot of soup",
    6: "Ring"
}

LOOT_CORPSE_5 = {
    1: "Mug",
    2: "Nail hook",
    3: "Rubber ball",
    4: "Banner",
    5: "Awl",
    6: "Gem"
}

LOOT_CORPSE_6 = {
    1: "Paring knife",
    2: "Scrimshaw",
    3: "Hat",
    4: "Egg",
    5: "Empty wallet",
    6: "Manacles"
}

# ============================================================================
# BOSSES
# ============================================================================

# noinspection SpellCheckingInspection
BOSSES = {
    "lazrothe": {
        "name": "Lazrothe the Sorcerer",
        "hd": "7",
        "ac": 17,
        "attacks": ["Staff (-1)", "Fog", "Ice Touch", "Summon"],
        "special": "Fog: Obscures vision and hinders initiative. Ice Touch: at range causes loss of footing and focus;"
                   " at melee (+4). Summon: Summons d3 Skeletons. Must recharge next Round, will attempt to flee to"
                   " adjacent room.",
        "description": "Once a celebrated magic-user of the world, now a bitter man who's ambition jeopardized the"
                       " realm. Deeper delves into the arcane workings of evil magics put the realm at risk, and he "
                       "was removed from his station. Now hides in remote lairs, building an army for revenge.",
        "tactics": {1: "Staff", 2: "Staff", 3: "Staff", 4: "Fog", 5: "Ice Touch", 6: "Summon & Flee"}
    },
    "martin": {
        "name": "Martin de Flail, Captain",
        "hd": "8",
        "ac": 14,
        "attacks": ["Shield (+1)", "Sword(+1)", "Grenade"],
        "special": "Grenade: retreats far as possible and tosses grenade. Accompanied: 2 Soldiers.",
        "description": "A proud warrior who felt slighted when a promotion was not rewarded to him. Has taken to "
                       "terrorizing the countryside and attacking patrols of soldiers. Not really a Captain, but"
                       " this has become part of his myth.",
        "tactics": {1: "Direct attack", 2: "Direct attack", 3: "Direct attack", 4: "Direct attack", 5: "Command flank",
                    6: "Grenade Toss"}
    },
    "grilsa": {
        "name": "Grilsa, the Great Brood Mother",
        "hd": "10",
        "ac": 16,
        "attacks": ["Bite", "Poison", "Web", "Jump", "Call"],
        "special": "Web: PC must save to break free. Jump: Jumps, out of / into range. Call: A Young Spider joins the"
                   " fight. Weak against fire/cold.",
        "description": "Said to be ancient and wise, but also cruel and bloodthirsty. Sole motive is to continue aging"
                       " and growing her brood. It is said her eyes are rare fiery-red jewels worth 100 gold each.",
        "tactics": {1: "Bite", 2: "Bite", 3: "Web", 4: "Jump", 5: "Call", 6: "Call"}
    },
    "sorlak": {
        "name": "Sorlak, the Lich",
        "hd": "12",
        "ac": 19,
        "attacks": ["Staff (-1)", "Lightning (x2)", "Life Drain"],
        "special": "Life Drain: 1 damage a turn, and gives Lich 1 life per turn. Immune: cold, lightning, poison. "
                   "Reduces: blunt melee dmg -1. Weak: piercing, fire. Accompanied: 3 Zombies.",
        "description": "A fierce undead wizard fully corrupted by the practice of dark magic. Consumes souls for power."
                       " Unleashes the undead amongst the world. Controls many minions and spies. Seeks powerful"
                       " artifacts to augment its power.",
        "tactics": {1: "Staff", 2: "Staff", 3: "Lightning", 4: "Lightning", 5: "Lightning", 6: "Life Drain"}
    },
    "firebane": {
        "name": "Firebane, the Eater of Dragons",
        "hd": "10",
        "ac": 17,
        "attacks": ["Claw Claw", "Bite(+3)", "Wing(+2)", "Fire Breath"],
        "special": "Fire Breath: Range (2d6). Wing: pushes target away. Weak against his own reflection. Removing a "
                   "foot will deal 3d8 damage to him. Uses his wings and flame breath to keep enemies at a distance "
                   "from his vulnerable feet.",
        "description": "Terrorizes the inner mountain ranges, though sometimes ventures out into the valleys in pursuit"
                       " of smaller dragon prey. Is said to sit over the great hoard of a lost civilization. If exposed"
                       " to live fire, the removed foot will transform into a small dragon egg.",
        "tactics": {1: "Claw Claw", 2: "Claw Claw", 3: "Bite", 4: "Wing", 5: "Wing", 6: "Fire Breath"}
    },
    "shrieking_wight": {
        "name": "The Shrieking Wight",
        "hd": "7",
        "ac": 15,
        "attacks": ["Cold Claw", "Fearful Shriek", "Ghost Summon"],
        "special": "Cold Claw: on a hit reduces target's level by 1. Fearful Shriek: Utters ear-shattering cry. All"
                   " present must save or stand powerless next round. Ghost Summon: 1 Ghost suddenly appears next to"
                   " random target dealing d3 damage, then disappears. Weak against light and healing magic. Immune to"
                   " all non-magical weapons except for those forged in silver.",
        "description": "The mourning, furious spirit of an executed leader of an ancient rebellion. Wants nothing more"
                       " than to destroy his nemesis or finally rest in peace.",
        "tactics": {1: "Cold Claw", 2: "Cold Claw", 3: "Cold Claw", 4: "Fearful Shriek", 5: "Fearful Shriek",
                    6: "Ghost Summon"}
    }
}

# ============================================================================
# NUMBER APPEARING
# ============================================================================

# Solo PC: Tier 1 = d3, Tier 2 = d2
NUM_APPEARING_SOLO_TIER_1 = "d3"
NUM_APPEARING_SOLO_TIER_2 = "d2"
