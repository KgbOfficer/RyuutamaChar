class EquipmentBase:
    def __init__(self, name="", effect="", durability=0):
        self.name = name
        self.effect = effect
        self.durability = durability

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            "name": self.name,
            "effect": self.effect,
            "durability": self.durability
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary (for loading)"""
        item = cls()
        for key, value in data.items():
            setattr(item, key, value)
        return item


class Weapon(EquipmentBase):
    def __init__(self, name="", effect="", durability=0, accuracy=0, damage=0):
        super().__init__(name, effect, durability)
        self.accuracy = accuracy
        self.damage = damage

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "accuracy": self.accuracy,
            "damage": self.damage
        })
        return data


class Shield(EquipmentBase):
    def __init__(self, name="", effect="", durability=0, defense=0):
        super().__init__(name, effect, durability)
        self.defense = defense

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "defense": self.defense
        })
        return data


class Armor(EquipmentBase):
    def __init__(self, name="", effect="", durability=0, defense_points=0, penalty=0):
        super().__init__(name, effect, durability)
        self.defense_points = defense_points
        self.penalty = penalty

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "defense_points": self.defense_points,
            "penalty": self.penalty
        })
        return data


class Item(EquipmentBase):
    def __init__(self, name="", effect="", durability=0, size=0):
        super().__init__(name, effect, durability)
        self.size = size  # Size for inventory management

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "size": self.size
        })
        return data