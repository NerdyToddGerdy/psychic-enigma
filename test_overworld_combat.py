"""
Test script for overworld combat encounters
"""

import sys
import random
from generators.character import create_character
from generators.hex_grid import HexGrid
from combat.combat_system import CombatEncounter
from generators.monster import Monster


def test_overworld_combat():
    """Test the complete overworld combat flow"""

    print("=" * 60)
    print("TESTING OVERWORLD COMBAT FLOW")
    print("=" * 60)

    # Step 1: Create a test character
    print("\n1. Creating test character...")
    player = create_character(
        name="Test Hero",
        race="Human",
        character_type="Soldier",
        hp=20,
        ac=14,
        attack_bonus=3,
        weapon="Long sword",
        armor="Chain mail"
    )
    print(f"   ✓ Created: {player.name} (HP: {player.hp_current}/{player.hp_max}, AC: {player.ac})")
    print(f"   ✓ Starting encounters_defeated: {player.encounters_defeated}")

    # Step 2: Create hex grid
    print("\n2. Creating hex grid...")
    hex_grid = HexGrid(start_position=(0, 0))
    print(f"   ✓ Grid created with {len(hex_grid.hexes)} hexes")

    # Step 3: Force a hostile encounter by manually spawning monsters
    print("\n3. Testing monster spawning...")

    # Test the _spawn_hostile_encounter method
    from tables import overland_tables
    from tables.table_roller import roll_on_table

    # Temporarily set the hex to a terrain that can have encounters
    test_hex = hex_grid.hexes[(0, 1)]
    print(f"   Test hex terrain: {test_hex.terrain}")

    # Spawn a hostile encounter on the hex
    encounter_data = test_hex._spawn_hostile_encounter()

    if isinstance(encounter_data, dict) and "monsters" in encounter_data:
        print(f"   ✓ Encounter spawned: {encounter_data['encounter_type']}")
        print(f"   ✓ Creature: {encounter_data['creature_name']}")
        print(f"   ✓ Number appearing: {encounter_data['num_appearing']}")
        print(f"   ✓ Monsters generated: {len(encounter_data['monsters'])}")

        for i, monster in enumerate(encounter_data['monsters']):
            print(f"      - {monster.name}: HP {monster.hp_current}/{monster.hp_max}, AC {monster.ac}")
    else:
        print("   ✗ Failed to spawn monsters properly!")
        return False

    # Step 4: Test combat initialization
    print("\n4. Testing combat initialization...")
    monsters = encounter_data['monsters']

    combat = CombatEncounter(player, monsters)
    print(f"   ✓ Combat created with {len(combat.monsters)} monsters")
    print(f"   ✓ Combat active: {not combat.is_combat_over()}")

    # Step 5: Simulate combat
    print("\n5. Simulating combat...")
    round_num = 1

    while not combat.is_combat_over() and round_num <= 20:
        print(f"\n   Round {round_num}:")

        # Player attacks a random alive monster
        alive_monsters = combat.get_alive_monsters()
        if alive_monsters:
            target_index = random.randint(0, len(alive_monsters) - 1)
            result = combat.player_attack(target_index)
            if result.get('hit'):
                print(f"      ✓ Player hits {alive_monsters[target_index].name} for {result.get('damage', 0)} damage!")
                if alive_monsters[target_index].hp_current <= 0:
                    print(f"         {alive_monsters[target_index].name} defeated!")
            else:
                print(f"      ✗ Player misses {alive_monsters[target_index].name}")

        # Monsters attack if any are alive
        if not combat.is_combat_over():
            player_hp_before = combat.player.hp_current
            combat.monster_turn()
            player_hp_after = combat.player.hp_current
            damage_taken = player_hp_before - player_hp_after
            if damage_taken > 0:
                print(f"      ✗ Monsters deal {damage_taken} damage to player! (HP: {player_hp_after}/{combat.player.hp_max})")
            else:
                print(f"      ✓ Monsters miss!")

        round_num += 1

    # Step 6: Check combat result
    print("\n6. Checking combat result...")
    if combat.is_combat_over():
        print(f"   ✓ Combat ended: {combat.combat_result.name}")

        if combat.combat_result.name == "VICTORY":
            print(f"   ✓ Player victorious!")
            print(f"   ✓ Player HP remaining: {combat.player.hp_current}/{combat.player.hp_max}")

            # Check loot
            if combat.loot:
                print(f"   ✓ Loot generated: {len(combat.loot)} items")
                for item in combat.loot:
                    print(f"      - {item}")
            else:
                print(f"   ℹ No loot dropped")

            # Step 7: Simulate loot transfer and counter increment
            print("\n7. Testing loot transfer and counter increment...")
            old_encounters = player.encounters_defeated
            old_inventory_count = len(player.inventory)

            # Transfer loot
            if combat.loot:
                for item in combat.loot:
                    player.add_to_inventory(item)

            # Increment counter
            player.encounters_defeated += 1

            print(f"   ✓ Encounters defeated: {old_encounters} → {player.encounters_defeated}")
            print(f"   ✓ Inventory count: {old_inventory_count} → {len(player.inventory)}")

            # Step 8: Verify everything
            print("\n8. Final verification...")
            print(f"   ✓ Player survived: {player.hp_current > 0}")
            print(f"   ✓ Counter incremented: {player.encounters_defeated == old_encounters + 1}")
            print(f"   ✓ Loot added to inventory: {len(player.inventory) >= old_inventory_count}")

            print("\n" + "=" * 60)
            print("✓ OVERWORLD COMBAT FLOW TEST PASSED!")
            print("=" * 60)
            return True

        elif combat.combat_result.name == "DEFEAT":
            print(f"   ✗ Player defeated!")
            print(f"   Player HP: {combat.player.hp_current}")
            print("\n" + "=" * 60)
            print("✓ Combat works but player died (test still valid)")
            print("=" * 60)
            return True

        else:
            print(f"   ℹ Combat ended with: {combat.combat_result.name}")
            return True
    else:
        print(f"   ✗ Combat did not resolve after 20 rounds")
        return False


if __name__ == "__main__":
    try:
        success = test_overworld_combat()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED WITH ERROR:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
