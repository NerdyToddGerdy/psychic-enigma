"""
Vendor System
Manages shop inventories for Armorer, Merchant, and Herbalist vendors in settlements.
"""

from tables import overland_tables


class VendorInventory:
    """Manages vendor inventory based on vendor type"""

    @staticmethod
    def get_armorer_inventory():
        """
        Get Armorer shop inventory (weapons and armor).

        Returns:
            dict: {
                "weapons": [list of weapon dicts],
                "armor": [list of armor dicts]
            }
        """
        weapons = []
        for weapon_name, weapon_data in overland_tables.WEAPONS.items():
            weapons.append({
                "name": weapon_name,
                "type": "weapon",
                "damage": weapon_data["damage"],
                "cost_silver": weapon_data["cost"],
                "bulky": weapon_data.get("bulky", False),
                "description": f"Deals {weapon_data['damage']} damage" +
                             (" (Bulky: takes 2 slots)" if weapon_data.get("bulky", False) else "")
            })

        armor = []
        for armor_name, armor_data in overland_tables.ARMOR.items():
            armor.append({
                "name": armor_name,
                "type": "armor",
                "ac_bonus": armor_data["AC"],
                "cost_silver": armor_data["cost"],
                "description": f"+{armor_data['AC']} Armor Class"
            })

        return {
            "weapons": sorted(weapons, key=lambda x: x["cost_silver"]),
            "armor": sorted(armor, key=lambda x: x["cost_silver"])
        }

    @staticmethod
    def get_merchant_inventory():
        """
        Get Merchant shop inventory (mundane items).

        Returns:
            list: List of item dicts with name, type, cost, description
        """
        items = []
        for item_name in overland_tables.MERCHANT_ITEMS:
            items.append({
                "name": item_name,
                "type": "mundane",
                "cost_silver": 3,  # All merchant items cost 3sp
                "description": f"Mundane item: {item_name}"
            })

        return sorted(items, key=lambda x: x["name"])

    @staticmethod
    def get_herbalist_inventory():
        """
        Get Herbalist shop inventory (potions and elixirs).

        Returns:
            list: List of potion dicts with name, type, cost, effect, description
        """
        items = []
        for item_name, item_data in overland_tables.HERBALIST.items():
            items.append({
                "name": item_name,
                "type": "consumable",
                "cost_silver": item_data["cost"],
                "effect": item_data["effect"],
                "description": item_data["effect"]
            })

        return sorted(items, key=lambda x: x["cost_silver"])

    @staticmethod
    def get_vendor_inventory(vendor_type):
        """
        Get inventory for any vendor type.

        Args:
            vendor_type (str): One of "Armorer", "Merchant", "Herbalist"

        Returns:
            dict or list: Vendor inventory

        Raises:
            ValueError: If vendor_type is not recognized
        """
        vendor_type = vendor_type.lower()

        if vendor_type == "armorer":
            return VendorInventory.get_armorer_inventory()
        elif vendor_type == "merchant":
            return VendorInventory.get_merchant_inventory()
        elif vendor_type == "herbalist":
            return VendorInventory.get_herbalist_inventory()
        else:
            raise ValueError(f"Unknown vendor type: {vendor_type}")

    @staticmethod
    def get_item_details(vendor_type, item_name):
        """
        Get details for a specific item from a vendor.

        Args:
            vendor_type (str): Vendor type
            item_name (str): Name of the item

        Returns:
            dict: Item details or None if not found
        """
        vendor_type = vendor_type.lower()
        inventory = VendorInventory.get_vendor_inventory(vendor_type)

        # Search through inventory structure
        if vendor_type == "armorer":
            # Check weapons
            for item in inventory["weapons"]:
                if item["name"] == item_name:
                    return item
            # Check armor
            for item in inventory["armor"]:
                if item["name"] == item_name:
                    return item
        else:
            # Merchant and Herbalist have flat lists
            for item in inventory:
                if item["name"] == item_name:
                    return item

        return None

    @staticmethod
    def calculate_sell_price(item_cost_silver):
        """
        Calculate the sell price for an item (100% of purchase price).

        Args:
            item_cost_silver (int): Original purchase price in silver

        Returns:
            int: Sell price in silver
        """
        return item_cost_silver
