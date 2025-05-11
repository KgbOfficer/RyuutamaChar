import tkinter as tk
from tkinter import ttk
from models.stats import Stat


class StatsTab(ttk.Frame):
    """Tab for character stats and skills"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("stats_tab", self)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Create frames for organization
        stats_frame = ttk.LabelFrame(self, text="Character Stats")
        stats_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        derived_frame = ttk.LabelFrame(self, text="Derived Stats")
        derived_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        abilities_frame = ttk.LabelFrame(self, text="Abilities & Spells")
        abilities_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Make abilities frame expandable
        self.rowconfigure(1, weight=1)

        # Character Stats Section
        # Setup the STR stat
        ttk.Label(stats_frame, text="STR (Strength)").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        str_frame = ttk.Frame(stats_frame)
        str_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.str_die_var = tk.StringVar(value="d6")
        self.str_die_combobox = ttk.Combobox(str_frame, textvariable=self.str_die_var, width=5, state="readonly")
        self.str_die_combobox['values'] = Stat.DIE_SIZES
        self.str_die_combobox.pack(side=tk.LEFT, padx=2)
        self.str_die_combobox.bind("<<ComboboxSelected>>", lambda e: self._on_die_change("str"))

        ttk.Label(str_frame, text="Value:").pack(side=tk.LEFT, padx=2)
        self.str_value_var = tk.IntVar(value=6)
        self.str_value_spinbox = ttk.Spinbox(str_frame, from_=1, to=20, textvariable=self.str_value_var, width=3)
        self.str_value_spinbox.pack(side=tk.LEFT, padx=2)
        self.str_value_spinbox.bind("<KeyRelease>", lambda e: self._on_value_change("str"))

        ttk.Label(str_frame, text="Max:").pack(side=tk.LEFT, padx=2)
        self.str_max_var = tk.IntVar(value=6)
        self.str_max_spinbox = ttk.Spinbox(str_frame, from_=1, to=20, textvariable=self.str_max_var, width=3)
        self.str_max_spinbox.pack(side=tk.LEFT, padx=2)
        self.str_max_spinbox.bind("<KeyRelease>", lambda e: self._on_max_change("str"))

        ttk.Label(str_frame, text="Current:").pack(side=tk.LEFT, padx=2)
        self.str_current_var = tk.IntVar(value=6)
        self.str_current_spinbox = ttk.Spinbox(str_frame, from_=0, to=20, textvariable=self.str_current_var, width=3)
        self.str_current_spinbox.pack(side=tk.LEFT, padx=2)
        self.str_current_spinbox.bind("<KeyRelease>", lambda e: self._on_current_change("str"))

        # Setup the DEX stat
        ttk.Label(stats_frame, text="DEX (Dexterity)").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        dex_frame = ttk.Frame(stats_frame)
        dex_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.dex_die_var = tk.StringVar(value="d6")
        self.dex_die_combobox = ttk.Combobox(dex_frame, textvariable=self.dex_die_var, width=5, state="readonly")
        self.dex_die_combobox['values'] = Stat.DIE_SIZES
        self.dex_die_combobox.pack(side=tk.LEFT, padx=2)
        self.dex_die_combobox.bind("<<ComboboxSelected>>", lambda e: self._on_die_change("dex"))

        ttk.Label(dex_frame, text="Value:").pack(side=tk.LEFT, padx=2)
        self.dex_value_var = tk.IntVar(value=6)
        self.dex_value_spinbox = ttk.Spinbox(dex_frame, from_=1, to=20, textvariable=self.dex_value_var, width=3)
        self.dex_value_spinbox.pack(side=tk.LEFT, padx=2)
        self.dex_value_spinbox.bind("<KeyRelease>", lambda e: self._on_value_change("dex"))

        # Setup the INT stat
        ttk.Label(stats_frame, text="INT (Intelligence)").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        int_frame = ttk.Frame(stats_frame)
        int_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.int_die_var = tk.StringVar(value="d6")
        self.int_die_combobox = ttk.Combobox(int_frame, textvariable=self.int_die_var, width=5, state="readonly")
        self.int_die_combobox['values'] = Stat.DIE_SIZES
        self.int_die_combobox.pack(side=tk.LEFT, padx=2)
        self.int_die_combobox.bind("<<ComboboxSelected>>", lambda e: self._on_die_change("int"))

        ttk.Label(int_frame, text="Value:").pack(side=tk.LEFT, padx=2)
        self.int_value_var = tk.IntVar(value=6)
        self.int_value_spinbox = ttk.Spinbox(int_frame, from_=1, to=20, textvariable=self.int_value_var, width=3)
        self.int_value_spinbox.pack(side=tk.LEFT, padx=2)
        self.int_value_spinbox.bind("<KeyRelease>", lambda e: self._on_value_change("int"))

        # Setup the SPI stat
        ttk.Label(stats_frame, text="SPI (Spirit)").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        spi_frame = ttk.Frame(stats_frame)
        spi_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.spi_die_var = tk.StringVar(value="d6")
        self.spi_die_combobox = ttk.Combobox(spi_frame, textvariable=self.spi_die_var, width=5, state="readonly")
        self.spi_die_combobox['values'] = Stat.DIE_SIZES
        self.spi_die_combobox.pack(side=tk.LEFT, padx=2)
        self.spi_die_combobox.bind("<<ComboboxSelected>>", lambda e: self._on_die_change("spi"))

        ttk.Label(spi_frame, text="Value:").pack(side=tk.LEFT, padx=2)
        self.spi_value_var = tk.IntVar(value=6)
        self.spi_value_spinbox = ttk.Spinbox(spi_frame, from_=1, to=20, textvariable=self.spi_value_var, width=3)
        self.spi_value_spinbox.pack(side=tk.LEFT, padx=2)
        self.spi_value_spinbox.bind("<KeyRelease>", lambda e: self._on_value_change("spi"))

        ttk.Label(spi_frame, text="Max:").pack(side=tk.LEFT, padx=2)
        self.spi_max_var = tk.IntVar(value=6)
        self.spi_max_spinbox = ttk.Spinbox(spi_frame, from_=1, to=20, textvariable=self.spi_max_var, width=3)
        self.spi_max_spinbox.pack(side=tk.LEFT, padx=2)
        self.spi_max_spinbox.bind("<KeyRelease>", lambda e: self._on_max_change("spi"))

        ttk.Label(spi_frame, text="Current:").pack(side=tk.LEFT, padx=2)
        self.spi_current_var = tk.IntVar(value=6)
        self.spi_current_spinbox = ttk.Spinbox(spi_frame, from_=0, to=20, textvariable=self.spi_current_var, width=3)
        self.spi_current_spinbox.pack(side=tk.LEFT, padx=2)
        self.spi_current_spinbox.bind("<KeyRelease>", lambda e: self._on_current_change("spi"))

        # Stat total calculation
        ttk.Label(stats_frame, text="Total Value:").grid(row=4, column=0, padx=5, pady=10, sticky="w")
        self.total_stat_var = tk.StringVar(value="24")
        ttk.Label(stats_frame, textvariable=self.total_stat_var, font=("Helvetica", 12, "bold")).grid(row=4, column=1,
                                                                                                      padx=5, pady=10,
                                                                                                      sticky="w")

        # Add a stat bonus display (for when total is over 10)
        ttk.Label(stats_frame, text="Bonus:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.stat_bonus_var = tk.StringVar(value="If over 10, add 1 dice size to any 1 stat")
        ttk.Label(stats_frame, textvariable=self.stat_bonus_var).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Derived Stats Section
        # Initiative calculation
        ttk.Label(derived_frame, text="Initiative (DEX + INT):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.initiative_var = tk.IntVar(value=12)
        initiative_frame = ttk.Frame(derived_frame)
        initiative_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(initiative_frame, textvariable=self.initiative_var, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT,
                                                                                                           padx=2)
        ttk.Button(initiative_frame, text="Recalculate", command=self._calculate_initiative).pack(side=tk.LEFT, padx=5)

        # Fumble points
        ttk.Label(derived_frame, text="Fumble Points:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fumble_var = tk.IntVar(value=0)
        self.fumble_spinbox = ttk.Spinbox(derived_frame, from_=0, to=99, textvariable=self.fumble_var, width=3)
        self.fumble_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.fumble_spinbox.bind("<KeyRelease>", self._on_fumble_change)

        # Travel Checks section (derived from stats)
        travel_frame = ttk.LabelFrame(derived_frame, text="Travel Checks")
        travel_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Movement Check
        ttk.Label(travel_frame, text="Movement Check (STR + DEX):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.movement_check_var = tk.StringVar(value="12")
        ttk.Label(travel_frame, textvariable=self.movement_check_var, font=("Helvetica", 10, "bold")).grid(row=0,
                                                                                                           column=1,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="w")

        # Direction Check
        ttk.Label(travel_frame, text="Direction Check (INT + INT):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.direction_check_var = tk.StringVar(value="12")
        ttk.Label(travel_frame, textvariable=self.direction_check_var, font=("Helvetica", 10, "bold")).grid(row=1,
                                                                                                            column=1,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky="w")

        # Camp Check
        ttk.Label(travel_frame, text="Camp Check (DEX + INT):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.camp_check_var = tk.StringVar(value="12")
        ttk.Label(travel_frame, textvariable=self.camp_check_var, font=("Helvetica", 10, "bold")).grid(row=2, column=1,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="w")

        # Recalculate button for all travel checks
        ttk.Button(travel_frame, text="Recalculate All", command=self._calculate_travel_checks).grid(row=3, column=0,
                                                                                                     columnspan=2,
                                                                                                     padx=5, pady=5)

        # Condition Check section
        condition_frame = ttk.LabelFrame(derived_frame, text="Condition Checks")
        condition_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # STR Condition Check
        ttk.Label(condition_frame, text="STR Check:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.str_condition_var = tk.IntVar(value=0)
        self.str_condition_spinbox = ttk.Spinbox(condition_frame, from_=0, to=99, textvariable=self.str_condition_var,
                                                 width=3)
        self.str_condition_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.str_condition_spinbox.bind("<KeyRelease>", self._on_condition_change)

        # DEX Condition Check
        ttk.Label(condition_frame, text="DEX Check:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dex_condition_var = tk.IntVar(value=0)
        self.dex_condition_spinbox = ttk.Spinbox(condition_frame, from_=0, to=99, textvariable=self.dex_condition_var,
                                                 width=3)
        self.dex_condition_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.dex_condition_spinbox.bind("<KeyRelease>", self._on_condition_change)

        # INT Condition Check
        ttk.Label(condition_frame, text="INT Check:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.int_condition_var = tk.IntVar(value=0)
        self.int_condition_spinbox = ttk.Spinbox(condition_frame, from_=0, to=99, textvariable=self.int_condition_var,
                                                 width=3)
        self.int_condition_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.int_condition_spinbox.bind("<KeyRelease>", self._on_condition_change)

        # SPI Condition Check
        ttk.Label(condition_frame, text="SPI Check:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.spi_condition_var = tk.IntVar(value=0)
        self.spi_condition_spinbox = ttk.Spinbox(condition_frame, from_=0, to=99, textvariable=self.spi_condition_var,
                                                 width=3)
        self.spi_condition_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.spi_condition_spinbox.bind("<KeyRelease>", self._on_condition_change)

        # Abilities & Spells Section with Notebook
        self.abilities_notebook = ttk.Notebook(abilities_frame)
        self.abilities_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a tab for each level
        self.ability_tabs = {}
        self.ability_texts = {}

        for level in range(1, 6):
            tab = ttk.Frame(self.abilities_notebook)
            self.abilities_notebook.add(tab, text=f"Level {level}")
            self.ability_tabs[level] = tab

            # Add a text widget for abilities/spells
            text_widget = tk.Text(tab, wrap=tk.WORD, height=10)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(text_widget, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Store reference to text widget
            self.ability_texts[level] = text_widget

            # Bind key release event
            text_widget.bind("<KeyRelease>", lambda e, level=level: self._on_ability_change(level))

    def _on_die_change(self, stat_name):
        """Handle die size change for a stat"""
        die_var = getattr(self, f"{stat_name}_die_var")
        value_var = getattr(self, f"{stat_name}_value_var")

        # Update the stat value based on the new die size
        die_size = die_var.get()
        avg_value = Stat.get_average_value(die_size)
        value_var.set(round(avg_value))

        # Update character model
        self._update_character_from_ui()
        self._update_derived_stats()
        self.app_controller.mark_unsaved_changes()

    def _on_value_change(self, stat_name):
        """Handle value change for a stat"""
        # Update character model
        self._update_character_from_ui()
        self._update_derived_stats()
        self.app_controller.mark_unsaved_changes()

    def _on_max_change(self, stat_name):
        """Handle max value change for a stat"""
        value_var = getattr(self, f"{stat_name}_max_var")
        current_var = getattr(self, f"{stat_name}_current_var")

        # Ensure current value doesn't exceed max
        if current_var.get() > value_var.get():
            current_var.set(value_var.get())

        # Update character model
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_current_change(self, stat_name):
        """Handle current value change for a stat"""
        max_var = getattr(self, f"{stat_name}_max_var")
        current_var = getattr(self, f"{stat_name}_current_var")

        # Ensure current value doesn't exceed max
        if current_var.get() > max_var.get():
            current_var.set(max_var.get())

        # Update character model
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_fumble_change(self, event=None):
        """Handle fumble points change"""
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_condition_change(self, event=None):
        """Handle condition check value change"""
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_ability_change(self, level):
        """Handle ability text change for a level"""
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _calculate_initiative(self):
        """Calculate initiative from DEX and INT"""
        dex_value = self.dex_value_var.get()
        int_value = self.int_value_var.get()
        initiative = dex_value + int_value

        self.initiative_var.set(initiative)
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _calculate_travel_checks(self):
        """Calculate all travel check values from stats"""
        str_value = self.str_value_var.get()
        dex_value = self.dex_value_var.get()
        int_value = self.int_value_var.get()

        # Movement Check (STR + DEX)
        self.movement_check_var.set(str(str_value + dex_value))

        # Direction Check (INT + INT)
        self.direction_check_var.set(str(int_value + int_value))

        # Camp Check (DEX + INT)
        self.camp_check_var.set(str(dex_value + int_value))

        self._update_character_from_ui()

    def _update_total_stats(self):
        """Update the total stats display"""
        str_value = self.str_value_var.get()
        dex_value = self.dex_value_var.get()
        int_value = self.int_value_var.get()
        spi_value = self.spi_value_var.get()

        total = str_value + dex_value + int_value + spi_value
        self.total_stat_var.set(str(total))

        # Update bonus text based on total
        if total > 10:
            self.stat_bonus_var.set("Bonus: Add 1 dice size to any 1 stat")
        else:
            self.stat_bonus_var.set("No bonus (total ≤ 10)")

    def _update_derived_stats(self):
        """Update all derived stats based on current stat values"""
        self._update_total_stats()
        self._calculate_initiative()
        self._calculate_travel_checks()

    def _update_character_from_ui(self):
        """Update character model from UI values"""
        character = self.app_controller.character

        # Update stat values
        character.str["die_size"] = self.str_die_var.get()
        character.str["value"] = self.str_value_var.get()
        character.str["max"] = self.str_max_var.get()
        character.str["current"] = self.str_current_var.get()

        character.dex["die_size"] = self.dex_die_var.get()
        character.dex["value"] = self.dex_value_var.get()

        character.int["die_size"] = self.int_die_var.get()
        character.int["value"] = self.int_value_var.get()

        character.spi["die_size"] = self.spi_die_var.get()
        character.spi["value"] = self.spi_value_var.get()
        character.spi["max"] = self.spi_max_var.get()
        character.spi["current"] = self.spi_current_var.get()

        # Update derived stats
        character.initiative = self.initiative_var.get()
        character.fumble_points = self.fumble_var.get()

        # Update condition checks
        character.condition_checks = {
            "str": self.str_condition_var.get(),
            "dex": self.dex_condition_var.get(),
            "int": self.int_condition_var.get(),
            "spi": self.spi_condition_var.get()
        }

        # Update abilities for each level
        for level in range(1, 6):
            text_widget = self.ability_texts[level]
            character.abilities[level] = text_widget.get("1.0", tk.END).strip()

    def update_from_character(self, character):
        """Update UI from character model"""
        # Update stat values
        self.str_die_var.set(character.str["die_size"])
        self.str_value_var.set(character.str["value"])
        self.str_max_var.set(character.str["max"])
        self.str_current_var.set(character.str["current"])

        self.dex_die_var.set(character.dex["die_size"])
        self.dex_value_var.set(character.dex["value"])

        self.int_die_var.set(character.int["die_size"])
        self.int_value_var.set(character.int["value"])

        self.spi_die_var.set(character.spi["die_size"])
        self.spi_value_var.set(character.spi["value"])
        self.spi_max_var.set(character.spi["max"])
        self.spi_current_var.set(character.spi["current"])

        # Update derived stats
        self.initiative_var.set(character.initiative)
        self.fumble_var.set(character.fumble_points)

        # Update condition checks
        self.str_condition_var.set(character.condition_checks["str"])
        self.dex_condition_var.set(character.condition_checks["dex"])
        self.int_condition_var.set(character.condition_checks["int"])
        self.spi_condition_var.set(character.condition_checks["spi"])

        # Update abilities for each level
        for level in range(1, 6):
            text_widget = self.ability_texts[level]
            text_widget.delete("1.0", tk.END)
            if level in character.abilities and character.abilities[level]:
                text_widget.insert("1.0", character.abilities[level])

        # Update derived stats displays
        self._update_derived_stats()