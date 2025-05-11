class Stat:
    """Represents a character stat in Ryuutama"""

    DIE_SIZES = ["d4", "d6", "d8", "d10", "d12", "d20"]

    def __init__(self, name, value=6, die_size="d6", max_value=None, current_value=None):
        self.name = name
        self.value = value
        self.die_size = die_size
        # For stats that can be reduced (STR/SPI)
        self.max_value = max_value if max_value is not None else value
        self.current_value = current_value if current_value is not None else value

    def increase_die_size(self):
        """Increase the die size to the next level"""
        current_index = self.DIE_SIZES.index(self.die_size)
        if current_index < len(self.DIE_SIZES) - 1:
            self.die_size = self.DIE_SIZES[current_index + 1]
            # Update the value based on the average of the new die
            self.value = self.get_average_value(self.die_size)

    def decrease_die_size(self):
        """Decrease the die size to the previous level"""
        current_index = self.DIE_SIZES.index(self.die_size)
        if current_index > 0:
            self.die_size = self.DIE_SIZES[current_index - 1]
            # Update the value based on the average of the new die
            self.value = self.get_average_value(self.die_size)

    @staticmethod
    def get_average_value(die_size):
        """Calculate the average value for a die size"""
        die_map = {
            "d4": 2.5,
            "d6": 3.5,
            "d8": 4.5,
            "d10": 5.5,
            "d12": 6.5,
            "d20": 10.5
        }
        return die_map.get(die_size, 3.5)  # Default to d6 if unknown

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            "name": self.name,
            "value": self.value,
            "die_size": self.die_size,
            "max_value": self.max_value,
            "current_value": self.current_value
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary (for loading)"""
        return cls(
            name=data.get("name", ""),
            value=data.get("value", 6),
            die_size=data.get("die_size", "d6"),
            max_value=data.get("max_value", None),
            current_value=data.get("current_value", None)
        )