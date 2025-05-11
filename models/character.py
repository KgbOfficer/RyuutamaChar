class Character:
    def __init__(self):
        # Basic character info
        self.name = ""
        self.player_name = ""
        self.level = 1
        self.exp = 0
        self.gender = ""
        self.age = ""
        self.character_class = ""
        self.type = ""

        # Class details
        self.class_skill = ""
        self.stats_used = ""
        self.effect = ""
        self.mastered_weapon = ""
        self.specialized_terrain = ""
        self.personal_item = ""

        # Stats
        self.str = {"value": 6, "die_size": "d6", "max": 6, "current": 6}  # Default d6
        self.dex = {"value": 6, "die_size": "d6"}
        self.int = {"value": 6, "die_size": "d6"}
        self.spi = {"value": 6, "die_size": "d6", "max": 6, "current": 6}

        # Additional stats
        self.initiative = 0
        self.fumble_points = 0

        # Equipment
        self.weapons = []  # List of weapon objects
        self.shield = None  # Shield object
        self.armor = None  # Armor object
        self.travelers_outfit = []  # List of outfit/equipment items

        # Condition
        self.condition_checks = {
            "str": 0,
            "dex": 0,
            "int": 0,
            "spi": 0
        }

        # Status effects
        self.status_effects = {
            "injury": False,
            "tired": False,
            "poison": False,
            "muddled": False,
            "sick": False,
            "shock": False
        }

        # Terrain and weather
        self.current_terrain = ""
        self.current_weather = ""

        # Appearance and background
        self.image_path = ""  # Path to character image
        self.appearance = ""
        self.hometown = ""
        self.reason_for_travel = ""

        # Notes
        self.notes = ""

        # Spells/abilities by level
        self.abilities = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }

    def calculate_initiative(self):
        """Calculate character's initiative based on DEX and INT"""
        return self.dex["value"] + self.int["value"]

    def get_traveling_check_bonus(self, check_type):
        """
        Calculate bonus for travel checks:
        1) Movement Check [STR + DEX]
        2) Direction Check [INT + INT]
        3) Camp Check [DEX + INT]
        """
        if check_type == "movement":
            return self.str["value"] + self.dex["value"]
        elif check_type == "direction":
            return self.int["value"] + self.int["value"]
        elif check_type == "camp":
            return self.dex["value"] + self.int["value"]
        return 0

    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {
            "name": self.name,
            "player_name": self.player_name,
            "level": self.level,
            "exp": self.exp,
            "gender": self.gender,
            "age": self.age,
            "character_class": self.character_class,
            "type": self.type,
            "class_skill": self.class_skill,
            "stats_used": self.stats_used,
            "effect": self.effect,
            "mastered_weapon": self.mastered_weapon,
            "specialized_terrain": self.specialized_terrain,
            "personal_item": self.personal_item,
            "str": self.str,
            "dex": self.dex,
            "int": self.int,
            "spi": self.spi,
            "initiative": self.initiative,
            "fumble_points": self.fumble_points,
            "weapons": [w.to_dict() for w in self.weapons] if self.weapons else [],
            "shield": self.shield.to_dict() if self.shield else None,
            "armor": self.armor.to_dict() if self.armor else None,
            "travelers_outfit": [i.to_dict() for i in self.travelers_outfit] if self.travelers_outfit else [],
            "condition_checks": self.condition_checks,
            "status_effects": self.status_effects,
            "current_terrain": self.current_terrain,
            "current_weather": self.current_weather,
            "image_path": self.image_path,
            "appearance": self.appearance,
            "hometown": self.hometown,
            "reason_for_travel": self.reason_for_travel,
            "notes": self.notes,
            "abilities": self.abilities
        }

    @classmethod
    def from_dict(cls, data):
        """Create character from dictionary (for loading)"""
        character = cls()
        for key, value in data.items():
            setattr(character, key, value)

        # Recreate objects for weapons, armor, etc.
        from models.equipment import Weapon, Shield, Armor, Item

        if "weapons" in data and data["weapons"]:
            character.weapons = [Weapon.from_dict(w) for w in data["weapons"]]

        if "shield" in data and data["shield"]:
            character.shield = Shield.from_dict(data["shield"])

        if "armor" in data and data["armor"]:
            character.armor = Armor.from_dict(data["armor"])

        if "travelers_outfit" in data and data["travelers_outfit"]:
            character.travelers_outfit = [Item.from_dict(i) for i in data["travelers_outfit"]]

        return character