"""
Table Roller - Shared utility for rolling on game tables
Provides functions to roll on any d6, d66, 2d6, or list-based table
"""

import random


def roll_on_table(table, table_name=None):
    """
    Roll on a table and return a random result.

    Args:
        table: The table to roll on (dict or list)
        table_name (str, optional): Name of the table for error messages

    Returns:
        The random value from the table

    Raises:
        ValueError: If table is empty or has unsupported type

    Examples:
        >>> terrain_table = {1: "Grasslands", 2: "Woods", 3: "Hills",
        ...                  4: "Mountains", 5: "Swamp", 6: "Wasteland"}
        >>> roll_on_table(terrain_table)
        "Woods"

        >>> items = ["Sword", "Shield", "Potion"]
        >>> roll_on_table(items)
        "Shield"
    """
    name_str = f" '{table_name}'" if table_name else ""

    if table is None:
        raise ValueError(f"Table{name_str} is None")

    # Handle different table types
    if isinstance(table, dict):
        # Check if it's a d6 table (keys 1-6) or a grid table (keys like 11-66)
        keys = list(table.keys())

        if not keys:
            raise ValueError(f"Table{name_str} is empty")

        # Determine what kind of dice to roll based on the keys
        if all(isinstance(k, int) and 1 <= k <= 6 for k in keys):
            # Standard d6 table
            roll = roll_d6()
        elif all(isinstance(k, int) and 11 <= k <= 66 for k in keys):
            # Grid table (d66) - roll two d6 and combine
            roll = roll_d66()
        elif all(isinstance(k, int) and 2 <= k <= 12 for k in keys):
            # 2d6 table
            roll = roll_2d6()
        elif all(isinstance(k, int) and 1 <= k <= 4 for k in keys):
            # d4 table
            roll = roll_d4()
        else:
            # Unknown table format, just pick a random key
            roll = random.choice(keys)

        return table.get(roll)

    elif isinstance(table, list):
        # List table - return a random element
        if not table:
            raise ValueError(f"Table{name_str} is empty")
        return random.choice(table)

    else:
        raise ValueError(
            f"Table{name_str} has unsupported type: {type(table)}"
        )


def roll_on_table_by_name(table_name, module):
    """
    Roll on a table by name from a given module.

    Args:
        table_name (str): The name of the table constant (e.g., "TERRAIN")
        module: The module containing the table (e.g., overland_tables)

    Returns:
        The random value from the table

    Raises:
        ValueError: If table doesn't exist in module

    Examples:
        >>> import overland_tables
        >>> roll_on_table_by_name("TERRAIN", overland_tables)
        "Hills"
    """
    if not hasattr(module, table_name):
        raise ValueError(
            f"Table '{table_name}' not found in module '{module.__name__}'"
        )

    table = getattr(module, table_name)
    return roll_on_table(table, table_name)


def roll_d4():
    """Roll a single d4 (1-4)."""
    return random.randint(1, 4)


def roll_d6():
    """Roll a single d6 (1-6)."""
    return random.randint(1, 6)


def roll_2d6():
    """Roll 2d6 and return the sum (2-12)."""
    return random.randint(1, 6) + random.randint(1, 6)


def roll_3d6():
    """Roll 3d6 and return the sum (3-18)."""
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)


def roll_d66():
    """
    Roll d66 (roll d6 twice and combine as tens and ones).
    Results range from 11-66.
    """
    return random.randint(1, 6) * 10 + random.randint(1, 6)


def roll_d20():
    """Roll a single d20 (1-20)."""
    return random.randint(1, 20)


def roll_d100():
    """Roll a single d100 (1-100)."""
    return random.randint(1, 100)


def roll_dice(num_dice, die_size):
    """
    Roll multiple dice of a given size and return the sum.

    Args:
        num_dice (int): Number of dice to roll
        die_size (int): Size of each die

    Returns:
        int: Sum of all dice rolls

    Examples:
        >>> roll_dice(3, 6)  # 3d6
        14
        >>> roll_dice(2, 10)  # 2d10
        15
    """
    return sum(random.randint(1, die_size) for _ in range(num_dice))


def get_all_table_names(module):
    """
    Return a list of all available table names from a module.

    Args:
        module: The module to inspect (e.g., overland_tables)

    Returns:
        list: All table names (constants) that are dictionaries or lists

    Examples:
        >>> import overland_tables
        >>> tables = get_all_table_names(overland_tables)
        >>> "TERRAIN" in tables
        True
    """
    tables = []
    for name in dir(module):
        if name.isupper():
            value = getattr(module, name)
            if isinstance(value, (dict, list)):
                # Exclude numeric constants
                if not (isinstance(value, int) or isinstance(value, float)):
                    tables.append(name)
    return sorted(tables)
