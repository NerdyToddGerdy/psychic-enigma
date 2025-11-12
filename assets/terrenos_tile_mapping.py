"""
Terrenos Hex Tile Mapping
Maps game terrain types to Terrenos Roll20 hex tile images

The Terrenos folder contains 20 hex terrain tiles in Portuguese.
This file provides the mapping between internal terrain types and tile image files.
"""

# Mapping of terrain types to Terrenos tile files
TERRAIN_TILE_MAPPING = {
    # Basic terrain types
    "plains": "assets/Terrenos (Roll20)/Planície.png",
    "grassland": "assets/Terrenos (Roll20)/Campos verdejantes.png",
    "field": "assets/Terrenos (Roll20)/Campo.png",

    # Hills
    "hills": "assets/Terrenos (Roll20)/Colinas.png",
    "green_hills": "assets/Terrenos (Roll20)/Colinas Verdejantes.png",

    # Forest
    "forest": "assets/Terrenos (Roll20)/Floresta.png",
    "dense_forest": "assets/Terrenos (Roll20)/Floresta Densa.png",
    "forest_hills": "assets/Terrenos (Roll20)/Floresta-Colinas.png",

    # Desert
    "desert": "assets/Terrenos (Roll20)/Deserto.png",
    "desert_empty": "assets/Terrenos (Roll20)/Deserto - Vazio.png",
    "dunes": "assets/Terrenos (Roll20)/Dunas.png",
    "cactus": "assets/Terrenos (Roll20)/Cactos.png",

    # Mountains
    "mountain": "assets/Terrenos (Roll20)/Montanha.png",
    "mountains": "assets/Terrenos (Roll20)/Montanhas.png",

    # Water
    "sea": "assets/Terrenos (Roll20)/Mar.png",
    "deep_sea": "assets/Terrenos (Roll20)/Mar profundo.png",
    "ocean": "assets/Terrenos (Roll20)/Oceano.png",
    "deep_ocean": "assets/Terrenos (Roll20)/Oceano profundo.png",

    # Swamp
    "swamp": "assets/Terrenos (Roll20)/Pântano.png",
    "wetlands": "assets/Terrenos (Roll20)/Pantanal.png",
}

# Fallback mapping for common terrain names
TERRAIN_ALIASES = {
    "grass": "grassland",
    "plain": "plains",
    "hill": "hills",
    "woods": "forest",
    "jungle": "dense_forest",
    "sand": "desert",
    "beach": "desert_empty",
    "peak": "mountain",
    "water": "sea",
    "marsh": "swamp",
    "bog": "wetlands",
}

def get_tile_for_terrain(terrain_type: str) -> str:
    """
    Get the hex tile image path for a given terrain type.

    Args:
        terrain_type: The terrain type (e.g., "forest", "mountain")

    Returns:
        Path to the hex tile image, or default tile if not found
    """
    terrain_lower = terrain_type.lower()

    # Check direct mapping
    if terrain_lower in TERRAIN_TILE_MAPPING:
        return TERRAIN_TILE_MAPPING[terrain_lower]

    # Check aliases
    if terrain_lower in TERRAIN_ALIASES:
        aliased_terrain = TERRAIN_ALIASES[terrain_lower]
        return TERRAIN_TILE_MAPPING.get(aliased_terrain, TERRAIN_TILE_MAPPING["plains"])

    # Default to plains if terrain not found
    return TERRAIN_TILE_MAPPING["plains"]

def get_all_available_tiles():
    """
    Get a list of all available terrain tiles.

    Returns:
        List of tuples (terrain_name, file_path)
    """
    return [(terrain, path) for terrain, path in TERRAIN_TILE_MAPPING.items()]
