class StatusEffect:
    """Represents a status effect in Ryuutama"""

    EFFECTS = {
        "injury": {
            "description": "Physical damage that impairs your body",
            "type": "body",
            "check_stat": "str",
            "recovery_value": 5,  # Default recovery check value
            "effect": "-2 to all physical checks"
        },
        "tired": {
            "description": "Exhaustion from travel or combat",
            "type": "body",
            "check_stat": "str",
            "recovery_value": 6,
            "effect": "Unable to use Concentration actions"
        },
        "poison": {
            "description": "Toxins affecting your system",
            "type": "body",
            "check_stat": "str",
            "recovery_value": 7,
            "effect": "Take 1 damage at the start of each day"
        },
        "muddled": {
            "description": "Confusion affecting your thinking",
            "type": "mind",
            "check_stat": "int",
            "recovery_value": 6,
            "effect": "-2 to all mental checks"
        },
        "sick": {
            "description": "Illness affecting your body",
            "type": "body",
            "check_stat": "str",
            "recovery_value": 7,
            "effect": "Take 1 damage to MP at start of each day"
        },
        "shock": {
            "description": "Mental trauma from a shocking event",
            "type": "mind",
            "check_stat": "spi",
            "recovery_value": 7,
            "effect": "Unable to use magic"
        }
    }

    def __init__(self, effect_type):
        self.type = effect_type
        self.info = self.EFFECTS.get(effect_type, {})

    @property
    def description(self):
        return self.info.get("description", "")

    @property
    def effect_type(self):
        return self.info.get("type", "")

    @property
    def check_stat(self):
        return self.info.get("check_stat", "")

    @property
    def recovery_value(self):
        return self.info.get("recovery_value", 0)

    @property
    def effect(self):
        return self.info.get("effect", "")


class TerrainEffect:
    """Represents terrain effects in Ryuutama"""

    TERRAINS = {
        "grassland": {"description": "Open fields and gentle hills", "effects": {"dex": 1}},
        "wasteland": {"description": "Barren, difficult terrain", "effects": {"str": 1}},
        "woods": {"description": "Light forest and brush", "effects": {"int": 1}},
        "highlands": {"description": "High plateaus and hills", "effects": {"spi": 1}},
        "rocky_terrain": {"description": "Difficult, rocky ground", "effects": {"str": 1, "dex": 1}},
        "deep_forest": {"description": "Dense, thick forest", "effects": {"int": 1, "dex": 1}},
        "swamp": {"description": "Boggy, wet terrain", "effects": {"str": 1, "dex": 1}},
        "mountain": {"description": "High, steep mountains", "effects": {"str": 1, "spi": 1}},
        "desert": {"description": "Hot, dry wasteland", "effects": {"str": 1, "spi": 1}},
        "jungle": {"description": "Dense, tropical forest", "effects": {"int": 1, "str": 1}},
        "alpine": {"description": "High mountains above treeline", "effects": {"all": 1}}
    }

    def __init__(self, terrain_type):
        self.type = terrain_type
        self.info = self.TERRAINS.get(terrain_type, {})

    @property
    def description(self):
        return self.info.get("description", "")

    @property
    def effects(self):
        return self.info.get("effects", {})


class WeatherEffect:
    """Represents weather effects in Ryuutama"""

    WEATHER = {
        "rain": {"description": "Light rain", "effects": {"dex": -1}},
        "strong_wind": {"description": "High winds", "effects": {"dex": -1}},
        "fog": {"description": "Misty conditions", "effects": {"int": -1}},
        "hot": {"description": "Excessive heat", "effects": {"str": -1}},
        "cold": {"description": "Frigid conditions", "effects": {"str": -1}},
        "hardrain": {"description": "Heavy downpour", "effects": {"dex": -1, "int": -1}},
        "snow": {"description": "Light snowfall", "effects": {"dex": -1, "str": -1}},
        "deep_fog": {"description": "Thick, opaque fog", "effects": {"int": -2}},
        "dark": {"description": "Nighttime or darkness", "effects": {"int": -2}},
        "hurricane": {"description": "Severe storm", "effects": {"dex": -2, "int": -1}},
        "blizzard": {"description": "Heavy snow and wind", "effects": {"all": -1}}
    }

    def __init__(self, weather_type):
        self.type = weather_type
        self.info = self.WEATHER.get(weather_type, {})

    @property
    def description(self):
        return self.info.get("description", "")

    @property
    def effects(self):
        return self.info.get("effects", {})