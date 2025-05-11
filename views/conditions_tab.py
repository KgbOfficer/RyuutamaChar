import tkinter as tk
from tkinter import ttk
from models.conditions import StatusEffect


class ConditionsTab(ttk.Frame):
    """Tab for character status effects and conditions"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("conditions_tab", self)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)

        # Create frames for organization
        status_effects_frame = ttk.LabelFrame(self, text="Status Effects")
        status_effects_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        healing_frame = ttk.LabelFrame(self, text="Healing & Recovery")
        healing_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        notes_frame = ttk.LabelFrame(self, text="Condition Notes")
        notes_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Status Effects Section
        # Add description
        ttk.Label(
            status_effects_frame,
            text="If the next day's Condition Check is higher than the status effect number, it is cured.",
            wraplength=600
        ).pack(padx=5, pady=5, anchor="w")

        # Create a frame for the status effects
        effects_frame = ttk.Frame(status_effects_frame)
        effects_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Title row
        ttk.Label(effects_frame, text="Status Effect", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5,
                                                                                            pady=5, sticky="w")
        ttk.Label(effects_frame, text="Type", font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=5, pady=5,
                                                                                   sticky="w")
        ttk.Label(effects_frame, text="Check", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5,
                                                                                    sticky="w")
        ttk.Label(effects_frame, text="Recovery Value", font=("Helvetica", 10, "bold")).grid(row=0, column=3, padx=5,
                                                                                             pady=5, sticky="w")
        ttk.Label(effects_frame, text="Active", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=5, pady=5,
                                                                                     sticky="w")

        # Create a row for each status effect
        effect_types = ["injury", "tired", "poison", "muddled", "sick", "shock"]
        self.status_vars = {}

        for i, effect_type in enumerate(effect_types):
            effect = StatusEffect(effect_type)
            row = i + 1

            # Status name
            ttk.Label(effects_frame, text=effect_type.capitalize()).grid(row=row, column=0, padx=5, pady=5, sticky="w")

            # Status type (mind/body)
            ttk.Label(effects_frame, text=effect.effect_type.capitalize()).grid(row=row, column=1, padx=5, pady=5,
                                                                                sticky="w")

            # Check stat
            ttk.Label(effects_frame, text=effect.check_stat.upper()).grid(row=row, column=2, padx=5, pady=5, sticky="w")

            # Recovery value
            ttk.Label(effects_frame, text=str(effect.recovery_value)).grid(row=row, column=3, padx=5, pady=5,
                                                                           sticky="w")

            # Active checkbox
            status_var = tk.BooleanVar(value=False)
            self.status_vars[effect_type] = status_var
            status_cb = ttk.Checkbutton(
                effects_frame,
                variable=status_var,
                command=lambda et=effect_type: self._on_status_change(et)
            )
            status_cb.grid(row=row, column=4, padx=5, pady=5, sticky="w")

            # Effect description
            ttk.Label(effects_frame, text=f"Effect: {effect.effect}", wraplength=450).grid(row=row, column=5, padx=5,
                                                                                           pady=5, sticky="w")

        # Set column weights
        effects_frame.columnconfigure(5, weight=1)

        # Healing & Recovery Section
        # Add description
        ttk.Label(
            healing_frame,
            text="To attempt recovery from a status effect, make a Condition Check using the appropriate stat. "
                 "If the result is higher than the recovery value, the status effect is cured.",
            wraplength=600
        ).pack(padx=5, pady=5, anchor="w")

        # Create a frame for the recovery checks
        recovery_frame = ttk.Frame(healing_frame)
        recovery_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        # STR Check
        ttk.Label(recovery_frame, text="STR Check:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        str_check_frame = ttk.Frame(recovery_frame)
        str_check_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.str_check_var = tk.IntVar(value=0)
        ttk.Label(str_check_frame, textvariable=self.str_check_var, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(str_check_frame, text="Roll", command=lambda: self._simulate_roll("str")).pack(side=tk.LEFT, padx=5)

        # DEX Check
        ttk.Label(recovery_frame, text="DEX Check:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        dex_check_frame = ttk.Frame(recovery_frame)
        dex_check_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.dex_check_var = tk.IntVar(value=0)
        ttk.Label(dex_check_frame, textvariable=self.dex_check_var, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(dex_check_frame, text="Roll", command=lambda: self._simulate_roll("dex")).pack(side=tk.LEFT, padx=5)

        # INT Check
        ttk.Label(recovery_frame, text="INT Check:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        int_check_frame = ttk.Frame(recovery_frame)
        int_check_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.int_check_var = tk.IntVar(value=0)
        ttk.Label(int_check_frame, textvariable=self.int_check_var, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(int_check_frame, text="Roll", command=lambda: self._simulate_roll("int")).pack(side=tk.LEFT, padx=5)

        # SPI Check
        ttk.Label(recovery_frame, text="SPI Check:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        spi_check_frame = ttk.Frame(recovery_frame)
        spi_check_frame.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.spi_check_var = tk.IntVar(value=0)
        ttk.Label(spi_check_frame, textvariable=self.spi_check_var, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(spi_check_frame, text="Roll", command=lambda: self._simulate_roll("spi")).pack(side=tk.LEFT, padx=5)

        # Set column weights for recovery_frame
        for i in range(4):
            recovery_frame.columnconfigure(i, weight=1)

        # Add roll explanation
        ttk.Label(
            healing_frame,
            text="Note: The 'Roll' buttons simulate a die roll based on your character's stats for recovery checks. "
                 "In a real game, you would roll actual dice.",
            wraplength=600,
            font=("Helvetica", 8)
        ).pack(padx=5, pady=5, anchor="w")

        # Notes Section
        self.notes_text = tk.Text(notes_frame, wrap=tk.WORD, height=6)
        self.notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_text.bind("<KeyRelease>", self._on_notes_change)

        # Add scrollbar to notes
        notes_scrollbar = ttk.Scrollbar(self.notes_text, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Make notes section expandable
        self.rowconfigure(2, weight=1)

    def _on_status_change(self, effect_type):
        """Handle status effect checkbox change"""
        # Update character's status effects
        self.app_controller.character.status_effects[effect_type] = self.status_vars[effect_type].get()
        self.app_controller.mark_unsaved_changes()

    def _on_notes_change(self, event=None):
        """Handle notes text change"""
        # In a real app, this would update some character field
        self.app_controller.mark_unsaved_changes()

    def _simulate_roll(self, stat_name):
        """Simulate a die roll for a condition check"""
        import random

        # Get character's stat value and die size
        character = self.app_controller.character
        stat_info = getattr(character, stat_name)

        # Parse die size (e.g., "d6" -> 6)
        die_size = int(stat_info["die_size"][1:])

        # Roll the die
        roll = random.randint(1, die_size)

        # Add stat value
        total = roll + stat_info["value"]

        # Update the check variable
        check_var = getattr(self, f"{stat_name}_check_var")
        check_var.set(total)

        # Save the check value to character
        character.condition_checks[stat_name] = total

        # Update status effects based on check result
        self._check_status_recovery(stat_name, total)

        # Mark changes
        self.app_controller.mark_unsaved_changes()

    def _check_status_recovery(self, stat_name, check_value):
        """Check if any status effects are cured by this check"""
        # Get all status effects that use this stat for recovery
        for effect_type, is_active in self.app_controller.character.status_effects.items():
            if not is_active:
                continue

            effect = StatusEffect(effect_type)
            if effect.check_stat == stat_name:
                # Check if the roll is higher than the recovery value
                if check_value > effect.recovery_value:
                    # Cure the status effect
                    self.status_vars[effect_type].set(False)
                    self.app_controller.character.status_effects[effect_type] = False

                    # Show a message
                    from tkinter import messagebox
                    messagebox.showinfo(
                        "Status Recovery",
                        f"The {effect_type.capitalize()} status effect has been cured!"
                    )

    def update_from_character(self, character):
        """Update UI from character model"""
        # Update status effect checkboxes
        for effect_type, is_active in character.status_effects.items():
            if effect_type in self.status_vars:
                self.status_vars[effect_type].set(is_active)

        # Update condition check values
        self.str_check_var.set(character.condition_checks["str"])
        self.dex_check_var.set(character.condition_checks["dex"])
        self.int_check_var.set(character.condition_checks["int"])
        self.spi_check_var.set(character.condition_checks["spi"])