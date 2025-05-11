import tkinter as tk
from tkinter import ttk
from models.conditions import TerrainEffect, WeatherEffect


class TravelTab(ttk.Frame):
    """Tab for travel rules, terrain, and weather"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("travel_tab", self)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Create frames for organization
        travel_rules_frame = ttk.LabelFrame(self, text="Traveling Rules")
        travel_rules_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        terrain_frame = ttk.LabelFrame(self, text="Terrain")
        terrain_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        weather_frame = ttk.LabelFrame(self, text="Weather")
        weather_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        effects_frame = ttk.LabelFrame(self, text="Current Effects")
        effects_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Traveling Rules Section
        # Display the three travel check types
        ttk.Label(travel_rules_frame, text="1) Movement Check [STR + DEX]").grid(row=0, column=0, padx=5, pady=5,
                                                                                 sticky="w")
        ttk.Label(travel_rules_frame, text="2) Direction Check [INT + INT]").grid(row=0, column=1, padx=5, pady=5,
                                                                                  sticky="w")
        ttk.Label(travel_rules_frame, text="3) Camp Check [DEX + INT]").grid(row=0, column=2, padx=5, pady=5,
                                                                             sticky="w")

        # Add note about equipment
        ttk.Label(travel_rules_frame, text="Equipped items count as size 0").grid(row=1, column=0, columnspan=3, padx=5,
                                                                                  pady=5, sticky="w")

        # Set column weights for travel_rules_frame
        for i in range(3):
            travel_rules_frame.columnconfigure(i, weight=1)

        # Terrain Section
        terrain_types = [
            "grassland", "wasteland", "woods", "highlands", "rocky_terrain",
            "deep_forest", "swamp", "mountain", "desert", "jungle", "alpine"
        ]

        # Create a frame for displaying terrains
        terrain_display_frame = ttk.Frame(terrain_frame)
        terrain_display_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Calculate number of rows needed (2 terrains per row)
        terrain_rows = (len(terrain_types) + 1) // 2

        # Display terrain types in rows of 2
        for i, terrain_type in enumerate(terrain_types):
            row = i // 2
            col = i % 2

            # Create a frame for each terrain
            terrain_item_frame = ttk.Frame(terrain_display_frame)
            terrain_item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            # Create a checkbutton for each terrain
            terrain_var = tk.BooleanVar(value=False)
            self.__dict__[f"terrain_{terrain_type}_var"] = terrain_var

            effect = TerrainEffect(terrain_type)

            # Format effect text
            effect_text = ""
            for stat, bonus in effect.effects.items():
                if stat == "all":
                    effect_text = f"ALL: +{bonus}" if bonus > 0 else f"ALL: {bonus}"
                else:
                    effect_text += f"{stat.upper()}: +{bonus} " if bonus > 0 else f"{stat.upper()}: {bonus} "

            terrain_cb = ttk.Checkbutton(
                terrain_item_frame,
                text=f"{terrain_type.replace('_', ' ').title()} ({effect_text})",
                variable=terrain_var,
                command=lambda t=terrain_type: self._on_terrain_change(t)
            )
            terrain_cb.pack(side=tk.LEFT)

        # Set even column weights for terrain display
        terrain_display_frame.columnconfigure(0, weight=1)
        terrain_display_frame.columnconfigure(1, weight=1)

        # Set current terrain label
        ttk.Label(terrain_frame, text="Current Terrain:").pack(anchor="w", padx=5, pady=5)
        self.current_terrain_var = tk.StringVar(value="None")
        ttk.Label(terrain_frame, textvariable=self.current_terrain_var, font=("Helvetica", 10, "bold")).pack(anchor="w",
                                                                                                             padx=5,
                                                                                                             pady=0)

        # Terrain description
        ttk.Label(terrain_frame, text="Description:").pack(anchor="w", padx=5, pady=5)
        self.terrain_description_var = tk.StringVar(value="")
        ttk.Label(terrain_frame, textvariable=self.terrain_description_var, wraplength=250).pack(anchor="w", padx=5,
                                                                                                 pady=0)

        # Weather Section
        weather_types = [
            "rain", "strong_wind", "fog", "hot", "cold",
            "hardrain", "snow", "deep_fog", "dark", "hurricane", "blizzard"
        ]

        # Create a frame for displaying weathers
        weather_display_frame = ttk.Frame(weather_frame)
        weather_display_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Calculate number of rows needed (2 weathers per row)
        weather_rows = (len(weather_types) + 1) // 2

        # Display weather types in rows of 2
        for i, weather_type in enumerate(weather_types):
            row = i // 2
            col = i % 2

            # Create a frame for each weather
            weather_item_frame = ttk.Frame(weather_display_frame)
            weather_item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            # Create a checkbutton for each weather
            weather_var = tk.BooleanVar(value=False)
            self.__dict__[f"weather_{weather_type}_var"] = weather_var

            effect = WeatherEffect(weather_type)

            # Format effect text
            effect_text = ""
            for stat, bonus in effect.effects.items():
                if stat == "all":
                    effect_text = f"ALL: {bonus}"
                else:
                    effect_text += f"{stat.upper()}: {bonus} "

            weather_cb = ttk.Checkbutton(
                weather_item_frame,
                text=f"{weather_type.replace('_', ' ').title()} ({effect_text})",
                variable=weather_var,
                command=lambda w=weather_type: self._on_weather_change(w)
            )
            weather_cb.pack(side=tk.LEFT)

        # Set even column weights for weather display
        weather_display_frame.columnconfigure(0, weight=1)
        weather_display_frame.columnconfigure(1, weight=1)

        # Set current weather label
        ttk.Label(weather_frame, text="Current Weather:").pack(anchor="w", padx=5, pady=5)
        self.current_weather_var = tk.StringVar(value="None")
        ttk.Label(weather_frame, textvariable=self.current_weather_var, font=("Helvetica", 10, "bold")).pack(anchor="w",
                                                                                                             padx=5,
                                                                                                             pady=0)

        # Weather description
        ttk.Label(weather_frame, text="Description:").pack(anchor="w", padx=5, pady=5)
        self.weather_description_var = tk.StringVar(value="")
        ttk.Label(weather_frame, textvariable=self.weather_description_var, wraplength=250).pack(anchor="w", padx=5,
                                                                                                 pady=0)

        # Current Effects Section
        effects_text = (
            "Calculate the bonus or penalty to each stat based on the current terrain and weather conditions. "
            "Use these values when making travel checks."
        )
        ttk.Label(effects_frame, text=effects_text, wraplength=600).pack(anchor="w", padx=5, pady=5)

        effects_display_frame = ttk.Frame(effects_frame)
        effects_display_frame.pack(fill=tk.X, padx=5, pady=5)

        # STR effects
        ttk.Label(effects_display_frame, text="STR Effect:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.str_effect_var = tk.StringVar(value="0")
        ttk.Label(effects_display_frame, textvariable=self.str_effect_var, font=("Helvetica", 10, "bold")).grid(row=0,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5,
                                                                                                                sticky="w")

        # DEX effects
        ttk.Label(effects_display_frame, text="DEX Effect:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.dex_effect_var = tk.StringVar(value="0")
        ttk.Label(effects_display_frame, textvariable=self.dex_effect_var, font=("Helvetica", 10, "bold")).grid(row=0,
                                                                                                                column=3,
                                                                                                                padx=5,
                                                                                                                pady=5,
                                                                                                                sticky="w")

        # INT effects
        ttk.Label(effects_display_frame, text="INT Effect:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.int_effect_var = tk.StringVar(value="0")
        ttk.Label(effects_display_frame, textvariable=self.int_effect_var, font=("Helvetica", 10, "bold")).grid(row=1,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5,
                                                                                                                sticky="w")

        # SPI effects
        ttk.Label(effects_display_frame, text="SPI Effect:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.spi_effect_var = tk.StringVar(value="0")
        ttk.Label(effects_display_frame, textvariable=self.spi_effect_var, font=("Helvetica", 10, "bold")).grid(row=1,
                                                                                                                column=3,
                                                                                                                padx=5,
                                                                                                                pady=5,
                                                                                                                sticky="w")

        # Set column weights for effects display
        for i in range(4):
            effects_display_frame.columnconfigure(i, weight=1)

        # Calculate button
        ttk.Button(effects_frame, text="Calculate Effects", command=self._calculate_effects).pack(pady=10)

    def _on_terrain_change(self, terrain_type):
        """Handle terrain selection change"""
        # Reset all other terrain checkboxes
        terrain_types = [
            "grassland", "wasteland", "woods", "highlands", "rocky_terrain",
            "deep_forest", "swamp", "mountain", "desert", "jungle", "alpine"
        ]

        # Get the current selected terrain var
        current_var = self.__dict__[f"terrain_{terrain_type}_var"]

        # If this terrain is being selected (rather than deselected)
        if current_var.get():
            # Deselect all other terrains
            for other_terrain in terrain_types:
                if other_terrain != terrain_type:
                    self.__dict__[f"terrain_{other_terrain}_var"].set(False)

            # Update the current terrain
            pretty_name = terrain_type.replace('_', ' ').title()
            self.current_terrain_var.set(pretty_name)

            # Update the description
            effect = TerrainEffect(terrain_type)
            self.terrain_description_var.set(effect.description)

            # Update the character model
            self.app_controller.character.current_terrain = terrain_type
        else:
            # If deselecting the current terrain, clear the current terrain
            self.current_terrain_var.set("None")
            self.terrain_description_var.set("")

            # Update the character model
            self.app_controller.character.current_terrain = ""

        # Calculate effects
        self._calculate_effects()

        # Mark unsaved changes
        self.app_controller.mark_unsaved_changes()

    def _on_weather_change(self, weather_type):
        """Handle weather selection change"""
        # Reset all other weather checkboxes
        weather_types = [
            "rain", "strong_wind", "fog", "hot", "cold",
            "hardrain", "snow", "deep_fog", "dark", "hurricane", "blizzard"
        ]

        # Get the current selected weather var
        current_var = self.__dict__[f"weather_{weather_type}_var"]

        # If this weather is being selected (rather than deselected)
        if current_var.get():
            # Deselect all other weathers
            for other_weather in weather_types:
                if other_weather != weather_type:
                    self.__dict__[f"weather_{other_weather}_var"].set(False)

            # Update the current weather
            pretty_name = weather_type.replace('_', ' ').title()
            self.current_weather_var.set(pretty_name)

            # Update the description
            effect = WeatherEffect(weather_type)
            self.weather_description_var.set(effect.description)

            # Update the character model
            self.app_controller.character.current_weather = weather_type
        else:
            # If deselecting the current weather, clear the current weather
            self.current_weather_var.set("None")
            self.weather_description_var.set("")

            # Update the character model
            self.app_controller.character.current_weather = ""

        # Calculate effects
        self._calculate_effects()

        # Mark unsaved changes
        self.app_controller.mark_unsaved_changes()

    def _calculate_effects(self):
        """Calculate the combined effects of terrain and weather"""
        # Initialize effects dictionary
        effects = {
            "str": 0,
            "dex": 0,
            "int": 0,
            "spi": 0
        }

        # Get current terrain and calculate its effects
        current_terrain = self.app_controller.character.current_terrain
        if current_terrain:
            terrain_effect = TerrainEffect(current_terrain)
            for stat, bonus in terrain_effect.effects.items():
                if stat == "all":
                    # Apply to all stats
                    for key in effects:
                        effects[key] += bonus
                else:
                    effects[stat] += bonus

        # Get current weather and calculate its effects
        current_weather = self.app_controller.character.current_weather
        if current_weather:
            weather_effect = WeatherEffect(current_weather)
            for stat, bonus in weather_effect.effects.items():
                if stat == "all":
                    # Apply to all stats
                    for key in effects:
                        effects[key] += bonus
                else:
                    effects[stat] += bonus

        # Update the UI
        for stat, effect in effects.items():
            if effect > 0:
                self.__dict__[f"{stat}_effect_var"].set(f"+{effect}")
            else:
                self.__dict__[f"{stat}_effect_var"].set(str(effect))

    def update_from_character(self, character):
        """Update UI from character model"""
        # Reset all checkboxes
        terrain_types = [
            "grassland", "wasteland", "woods", "highlands", "rocky_terrain",
            "deep_forest", "swamp", "mountain", "desert", "jungle", "alpine"
        ]

        weather_types = [
            "rain", "strong_wind", "fog", "hot", "cold",
            "hardrain", "snow", "deep_fog", "dark", "hurricane", "blizzard"
        ]

        # Reset all terrain checkboxes
        for terrain_type in terrain_types:
            self.__dict__[f"terrain_{terrain_type}_var"].set(False)

        # Reset all weather checkboxes
        for weather_type in weather_types:
            self.__dict__[f"weather_{weather_type}_var"].set(False)

        # Set current terrain if any
        if character.current_terrain:
            self.__dict__[f"terrain_{character.current_terrain}_var"].set(True)
            pretty_name = character.current_terrain.replace('_', ' ').title()
            self.current_terrain_var.set(pretty_name)

            # Update the description
            effect = TerrainEffect(character.current_terrain)
            self.terrain_description_var.set(effect.description)
        else:
            self.current_terrain_var.set("None")
            self.terrain_description_var.set("")

        # Set current weather if any
        if character.current_weather:
            self.__dict__[f"weather_{character.current_weather}_var"].set(True)
            pretty_name = character.current_weather.replace('_', ' ').title()
            self.current_weather_var.set(pretty_name)

            # Update the description
            effect = WeatherEffect(character.current_weather)
            self.weather_description_var.set(effect.description)
        else:
            self.current_weather_var.set("None")
            self.weather_description_var.set("")

        # Calculate effects
        self._calculate_effects()