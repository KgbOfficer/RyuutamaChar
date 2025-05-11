"""
Ryuutama Character Sheet - Configuration
"""

import os

# Application Info
APP_NAME = "Ryuutama Character Sheet"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# File Paths
DEFAULT_SAVE_DIRECTORY = os.path.join(os.path.expanduser("~"), "RyuutamaCharacters")

# UI Settings
UI_DEFAULT_THEME = "light"  # "light" or "dark"
UI_DEFAULT_WINDOW_SIZE = "900x700"

# Die Sizes
DIE_SIZES = ["d4", "d6", "d8", "d10", "d12", "d20"]

# Terrain Types
TERRAIN_TYPES = [
    "grassland", "wasteland", "woods", "highlands", "rocky_terrain",
    "deep_forest", "swamp", "mountain", "desert", "jungle", "alpine"
]

# Weather Types
WEATHER_TYPES = [
    "rain", "strong_wind", "fog", "hot", "cold",
    "hardrain", "snow", "deep_fog", "dark", "hurricane", "blizzard"
]

# Status Effects
STATUS_EFFECTS = ["injury", "tired", "poison", "muddled", "sick", "shock"]

# Character Classes
CHARACTER_CLASSES = ["Minstrel", "Merchant", "Hunter", "Healer", "Farmer", "Artisan", "Noble"]

# Character Types
CHARACTER_TYPES = ["Attack", "Technical", "Magic"]