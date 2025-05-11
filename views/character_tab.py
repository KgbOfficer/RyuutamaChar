import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ensure we can import from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import class skills data
from utils.class_skills_data import CLASS_SKILLS


class CharacterTab(ttk.Frame):
    """Tab for basic character information"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("character_tab", self)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)  # Make the notes section expandable

        # Create frames for organization
        basic_frame = ttk.LabelFrame(self, text="Basic Information")
        basic_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        class_frame = ttk.LabelFrame(self, text="Class Details")
        class_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        appearance_frame = ttk.LabelFrame(self, text="Appearance & Background")
        appearance_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        notes_frame = ttk.LabelFrame(self, text="Notes")
        notes_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Basic information section
        # Row 0: Character Name, Player Name
        ttk.Label(basic_frame, text="Character Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(basic_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.name_entry.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(basic_frame, text="Player Name:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.player_name_var = tk.StringVar()
        self.player_name_entry = ttk.Entry(basic_frame, textvariable=self.player_name_var)
        self.player_name_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.player_name_entry.bind("<KeyRelease>", self._on_field_change)

        # Row 1: Level, EXP, Gender, Age
        ttk.Label(basic_frame, text="Level:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.level_var = tk.IntVar(value=1)
        self.level_spinbox = ttk.Spinbox(basic_frame, from_=1, to=20, textvariable=self.level_var, width=5)
        self.level_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.level_spinbox.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(basic_frame, text="Experience:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.exp_var = tk.IntVar()
        self.exp_spinbox = ttk.Spinbox(basic_frame, from_=0, to=9999, textvariable=self.exp_var, width=5)
        self.exp_spinbox.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.exp_spinbox.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(basic_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.gender_var = tk.StringVar()
        self.gender_entry = ttk.Entry(basic_frame, textvariable=self.gender_var, width=15)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.gender_entry.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(basic_frame, text="Age:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.age_var = tk.StringVar()
        self.age_entry = ttk.Entry(basic_frame, textvariable=self.age_var, width=15)
        self.age_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.age_entry.bind("<KeyRelease>", self._on_field_change)

        # Row 3: Class, Type
        ttk.Label(basic_frame, text="Class:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        # Predefined Ryuutama classes
        self.class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(basic_frame, textvariable=self.class_var, width=15)
        self.class_combobox['values'] = ("Minstrel", "Merchant", "Hunter", "Healer", "Farmer", "Artisan", "Noble")
        self.class_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.class_combobox.bind("<<ComboboxSelected>>", self._on_class_change)
        self.class_combobox.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(basic_frame, text="Type:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        # Predefined Ryuutama types
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(basic_frame, textvariable=self.type_var, width=15)
        self.type_combobox['values'] = ("Attack", "Technical", "Magic")
        self.type_combobox.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.type_combobox.bind("<<ComboboxSelected>>", self._on_type_change)
        self.type_combobox.bind("<KeyRelease>", self._on_field_change)

        # Setup column weights for basic_frame
        for i in range(4):
            basic_frame.columnconfigure(i, weight=1)

        # Class details section
        # Row 0: Class Skills, Stats Used
        ttk.Label(class_frame, text="Class Skills:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Class skills - Use a Text widget for better visibility and resizing
        skills_frame = ttk.Frame(class_frame)
        skills_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        skills_frame.columnconfigure(0, weight=1)  # Make the text widget expand

        # For data binding
        self.class_skill_var = tk.StringVar()

        # Text widget for skills
        self.class_skill_text = tk.Text(skills_frame, wrap=tk.WORD, height=2, width=30)
        self.class_skill_text.grid(row=0, column=0, sticky="ew")
        self.class_skill_text.bind("<KeyRelease>", self._on_skill_text_change)
        self.class_skill_text.bind("<Button-1>", self._show_skill_details)

        ttk.Label(class_frame, text="Stats Used:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.stats_used_var = tk.StringVar()
        self.stats_used_entry = ttk.Entry(class_frame, textvariable=self.stats_used_var)
        self.stats_used_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.stats_used_entry.bind("<KeyRelease>", self._on_field_change)

        # Row 1: Effect
        ttk.Label(class_frame, text="Effect:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.effect_var = tk.StringVar()
        self.effect_entry = ttk.Entry(class_frame, textvariable=self.effect_var)
        self.effect_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        self.effect_entry.bind("<KeyRelease>", self._on_field_change)

        # Row 2: Mastered Weapon, Specialized Terrain
        ttk.Label(class_frame, text="Mastered Weapon:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.mastered_weapon_var = tk.StringVar()
        self.mastered_weapon_entry = ttk.Entry(class_frame, textvariable=self.mastered_weapon_var)
        self.mastered_weapon_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.mastered_weapon_entry.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(class_frame, text="Specialized Terrain:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.specialized_terrain_var = tk.StringVar()
        self.specialized_terrain_combobox = ttk.Combobox(class_frame, textvariable=self.specialized_terrain_var)
        terrain_types = ["Grassland", "Wasteland", "Woods", "Highlands", "Rocky Terrain",
                         "Deep Forest", "Swamp", "Mountain", "Desert", "Jungle", "Alpine"]
        self.specialized_terrain_combobox['values'] = terrain_types
        self.specialized_terrain_combobox.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        self.specialized_terrain_combobox.bind("<<ComboboxSelected>>", self._on_field_change)
        self.specialized_terrain_combobox.bind("<KeyRelease>", self._on_field_change)

        # Row 3: Personal Item
        ttk.Label(class_frame, text="Personal Item:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.personal_item_var = tk.StringVar()
        self.personal_item_entry = ttk.Entry(class_frame, textvariable=self.personal_item_var)
        self.personal_item_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        self.personal_item_entry.bind("<KeyRelease>", self._on_field_change)

        # Setup column weights for class_frame
        for i in range(4):
            class_frame.columnconfigure(i, weight=1)

        # Appearance & Background section
        # Row 0: Character Image, Appearance
        ttk.Label(appearance_frame, text="Character Image:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Create a frame for the image and buttons
        image_frame = ttk.Frame(appearance_frame)
        image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Image path storage
        self.image_path_var = tk.StringVar()

        # Create a frame to display the image
        self.image_display_frame = ttk.LabelFrame(image_frame, text="Preview", width=100, height=100)
        self.image_display_frame.pack(side=tk.LEFT, padx=5, pady=5)
        self.image_display_frame.pack_propagate(False)  # Prevent frame from shrinking

        # Label to display the image
        self.image_label = ttk.Label(self.image_display_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Default "no image" display
        self.current_image = None
        self.image_label.configure(text="No Image")

        # Buttons for image management
        image_button_frame = ttk.Frame(image_frame)
        image_button_frame.pack(side=tk.LEFT, padx=5)

        ttk.Button(image_button_frame, text="Browse...", command=self._browse_image).pack(anchor="w", pady=2)
        ttk.Button(image_button_frame, text="Clear", command=self._clear_image).pack(anchor="w", pady=2)

        ttk.Label(appearance_frame, text="Appearance:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.appearance_var = tk.StringVar()
        self.appearance_entry = ttk.Entry(appearance_frame, textvariable=self.appearance_var)
        self.appearance_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.appearance_entry.bind("<KeyRelease>", self._on_field_change)

        # Row 1: Hometown, Reason for Travel
        ttk.Label(appearance_frame, text="Hometown:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.hometown_var = tk.StringVar()
        self.hometown_entry = ttk.Entry(appearance_frame, textvariable=self.hometown_var)
        self.hometown_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.hometown_entry.bind("<KeyRelease>", self._on_field_change)

        ttk.Label(appearance_frame, text="Reason for Travel:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.reason_for_travel_var = tk.StringVar()
        self.reason_for_travel_entry = ttk.Entry(appearance_frame, textvariable=self.reason_for_travel_var)
        self.reason_for_travel_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.reason_for_travel_entry.bind("<KeyRelease>", self._on_field_change)

        # Setup column weights for appearance_frame
        for i in range(4):
            appearance_frame.columnconfigure(i, weight=1)

        # Notes section
        self.notes_text = tk.Text(notes_frame, wrap=tk.WORD, height=10)
        self.notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_text.bind("<KeyRelease>", self._on_field_change)

        # Add scrollbar to notes
        notes_scrollbar = ttk.Scrollbar(self.notes_text, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_field_change(self, event=None):
        """Handle field changes"""
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_skill_text_change(self, event=None):
        """Handle changes to the skills text widget"""
        # Update the skills variable for model consistency
        skills_text = self.class_skill_text.get("1.0", tk.END).strip()
        self.class_skill_var.set(skills_text)
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _on_class_change(self, event=None):
        """Handle class selection change"""
        # Get the selected class
        character_class = self.class_var.get()

        # Update character model first
        self._update_character_from_ui()

        # Set class skills if class is in the data
        if character_class in CLASS_SKILLS:
            skills = CLASS_SKILLS[character_class]["skills"]

            # Update the text widget
            self.class_skill_text.delete("1.0", tk.END)
            self.class_skill_text.insert("1.0", ", ".join(skills))

            # Update the variable
            self.class_skill_var.set(", ".join(skills))

            # Show a confirmation message
            messagebox.showinfo(
                f"{character_class} Skills Added",
                f"Class skills for {character_class} have been added:\n\n• " + "\n• ".join(skills) +
                "\n\nClick on the skills field to see skill details."
            )

        # Mark changes
        self.app_controller.mark_unsaved_changes()

    def _on_type_change(self, event=None):
        """Handle character type changes and add appropriate abilities"""
        # Get the selected type
        character_type = self.type_var.get()

        # Update character model first
        self._update_character_from_ui()

        # Prepare type-specific abilities
        type_abilities = {
            "Attack": "Toughness: Max HP + 4\nPower: +1 bonus to damage rolls during combat\nWeapon Focus: Gain 1 more Mastered Weapon",
            "Technical": "Accurate: Gain an extra +1 bonus to any check when using Concentration for a total bonus of +1\nQuick: +1 bonus to initiative checks in combat\nPocket: Your Carrying Capacity is increased +3",
            "Magic": "Will: Max MP +4\nSpellbook: Acquire 2 Incantation spells per level\nSeasonal Sorcerer: Acquire Seasonal Magic"
        }

        # Add the appropriate abilities to level 1
        if character_type in type_abilities:
            # Clear existing level 1 abilities if type-related text isn't already there
            current_abilities = self.app_controller.character.abilities[1]

            # Check if we need to update
            ability_text = type_abilities[character_type]
            if ability_text not in current_abilities:
                # Set the new abilities for level 1
                self.app_controller.character.abilities[1] = ability_text

                # Get the stats tab to refresh its UI
                stats_tab = self.app_controller.ui_elements.get("stats_tab")
                if stats_tab:
                    stats_tab.update_from_character(self.app_controller.character)

                # Show a confirmation message
                messagebox.showinfo(
                    "Type Abilities Added",
                    f"Level 1 abilities for {character_type} Type have been added to your character."
                )

        # Mark changes
        self.app_controller.mark_unsaved_changes()

    def _show_skill_details(self, event=None):
        """Show details for skills when the skill entry is clicked"""
        # Get the current skills text
        skills_text = self.class_skill_text.get("1.0", tk.END).strip()
        if not skills_text:
            return

        # Get the character class
        character_class = self.class_var.get()
        if not character_class or character_class not in CLASS_SKILLS:
            return

        # Parse the skills (they could be comma-separated)
        skills_list = [s.strip() for s in skills_text.split(",")]

        # Create a popup window
        popup = tk.Toplevel(self)
        popup.title(f"{character_class} Skills")
        popup.transient(self)  # Set to be on top of the main window
        popup.grab_set()  # Make window modal

        # Set a minimum size for the popup
        popup.minsize(500, 400)

        # Center on parent
        popup.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))

        # Create a notebook for skills
        notebook = ttk.Notebook(popup)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a tab for each skill
        for skill in skills_list:
            # If the skill is in the descriptions
            if skill in CLASS_SKILLS[character_class]["descriptions"]:
                # Create frame for the skill
                skill_frame = ttk.Frame(notebook, padding=10)
                notebook.add(skill_frame, text=skill)

                # Get skill details
                skill_data = CLASS_SKILLS[character_class]["descriptions"][skill]

                # Configure rows and columns for better resizing
                skill_frame.columnconfigure(1, weight=1)
                for i in range(5):
                    skill_frame.rowconfigure(i, weight=0)

                # Add skill information
                row = 0

                # Description
                ttk.Label(skill_frame, text="Description:", font=("Helvetica", 10, "bold")).grid(
                    row=row, column=0, sticky="nw", pady=(0, 5))
                desc_label = ttk.Label(skill_frame, text=skill_data["description"], wraplength=400)
                desc_label.grid(row=row, column=1, sticky="nw", pady=(0, 5))
                row += 1

                # Effect
                ttk.Label(skill_frame, text="Skill Effect:", font=("Helvetica", 10, "bold")).grid(
                    row=row, column=0, sticky="nw", pady=(0, 5))
                effect_label = ttk.Label(skill_frame, text=skill_data["effect"], wraplength=400)
                effect_label.grid(row=row, column=1, sticky="nw", pady=(0, 5))
                row += 1

                # Usable Circumstances
                ttk.Label(skill_frame, text="Usable Circumstances:", font=("Helvetica", 10, "bold")).grid(
                    row=row, column=0, sticky="nw", pady=(0, 5))
                usable_label = ttk.Label(skill_frame, text=skill_data["usable"], wraplength=400)
                usable_label.grid(row=row, column=1, sticky="nw", pady=(0, 5))
                row += 1

                # Stat Used
                ttk.Label(skill_frame, text="Stat Used:", font=("Helvetica", 10, "bold")).grid(
                    row=row, column=0, sticky="nw", pady=(0, 5))
                stat_label = ttk.Label(skill_frame, text=skill_data["stat_used"], wraplength=400)
                stat_label.grid(row=row, column=1, sticky="nw", pady=(0, 5))
                row += 1

                # Target Number
                ttk.Label(skill_frame, text="Target Number:", font=("Helvetica", 10, "bold")).grid(
                    row=row, column=0, sticky="nw", pady=(0, 5))
                tn_label = ttk.Label(skill_frame, text=skill_data["tn"], wraplength=400)
                tn_label.grid(row=row, column=1, sticky="nw", pady=(0, 5))

        # Add an OK button
        button_frame = ttk.Frame(popup)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(button_frame, text="Close", command=popup.destroy).pack(side=tk.RIGHT)

    def _browse_image(self, event=None):
        """Open a file dialog to select an image"""
        from tkinter import filedialog
        import os
        from PIL import Image, ImageTk

        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select Character Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )

        # If a file was selected
        if file_path:
            try:
                # Open the image
                image = Image.open(file_path)

                # Resize to fit the display area (100x100)
                image.thumbnail((96, 96))

                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)

                # Update the label
                self.image_label.configure(image=photo, text="")

                # Keep a reference to prevent garbage collection
                self.current_image = photo

                # Store the image path
                self.image_path_var.set(file_path)

                # Update character model
                self._update_character_from_ui()
                self.app_controller.mark_unsaved_changes()

            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Image Error", f"Failed to load image: {e}")

    def _clear_image(self, event=None):
        """Clear the character image"""
        # Reset the image label
        self.image_label.configure(image="", text="No Image")
        self.current_image = None

        # Clear the image path
        self.image_path_var.set("")

        # Update character model
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()

    def _update_character_from_ui(self):
        """Update character model from UI values"""
        character = self.app_controller.character

        # Basic information
        character.name = self.name_var.get()
        character.player_name = self.player_name_var.get()
        character.level = self.level_var.get()
        character.exp = self.exp_var.get()
        character.gender = self.gender_var.get()
        character.age = self.age_var.get()
        character.character_class = self.class_var.get()
        character.type = self.type_var.get()

        # Class details
        character.class_skill = self.class_skill_text.get("1.0", tk.END).strip()
        character.stats_used = self.stats_used_var.get()
        character.effect = self.effect_var.get()
        character.mastered_weapon = self.mastered_weapon_var.get()
        character.specialized_terrain = self.specialized_terrain_var.get()
        character.personal_item = self.personal_item_var.get()

        # Appearance & Background
        character.image_path = self.image_path_var.get()  # Store image path instead of color
        character.appearance = self.appearance_var.get()
        character.hometown = self.hometown_var.get()
        character.reason_for_travel = self.reason_for_travel_var.get()

        # Notes
        character.notes = self.notes_text.get("1.0", tk.END).strip()

    def update_from_character(self, character):
        """Update UI from character model"""
        # Basic information
        self.name_var.set(character.name)
        self.player_name_var.set(character.player_name)
        self.level_var.set(character.level)
        self.exp_var.set(character.exp)
        self.gender_var.set(character.gender)
        self.age_var.set(character.age)
        self.class_var.set(character.character_class)
        self.type_var.set(character.type)

        # Class details
        self.class_skill_text.delete("1.0", tk.END)
        if character.class_skill:
            self.class_skill_text.insert("1.0", character.class_skill)
        self.class_skill_var.set(character.class_skill)

        self.stats_used_var.set(character.stats_used)
        self.effect_var.set(character.effect)
        self.mastered_weapon_var.set(character.mastered_weapon)
        self.specialized_terrain_var.set(character.specialized_terrain)
        self.personal_item_var.set(character.personal_item)

        # Appearance & Background
        # Load image if path exists
        if hasattr(character, 'image_path') and character.image_path:
            try:
                from PIL import Image, ImageTk
                import os

                if os.path.exists(character.image_path):
                    # Set image path variable
                    self.image_path_var.set(character.image_path)

                    # Load and display the image
                    image = Image.open(character.image_path)
                    image.thumbnail((96, 96))
                    photo = ImageTk.PhotoImage(image)

                    # Update the label
                    self.image_label.configure(image=photo, text="")

                    # Keep a reference to prevent garbage collection
                    self.current_image = photo
                else:
                    # Clear image if file doesn't exist
                    self.image_label.configure(image="", text="No Image")
                    self.current_image = None
            except Exception:
                # Clear image if loading fails
                self.image_label.configure(image="", text="No Image")
                self.current_image = None
        else:
            # Clear image if no path
            self.image_label.configure(image="", text="No Image")
            self.current_image = None

        self.appearance_var.set(character.appearance)
        self.hometown_var.set(character.hometown)
        self.reason_for_travel_var.set(character.reason_for_travel)

        # Notes
        self.notes_text.delete("1.0", tk.END)
        if character.notes:
            self.notes_text.insert("1.0", character.notes)