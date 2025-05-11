import tkinter as tk
from tkinter import ttk, messagebox
from models.equipment import Weapon, Shield, Armor, Item


class EquipmentTab(ttk.Frame):
    """Tab for character equipment and items"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("equipment_tab", self)

        # Setup UI
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)  # Make the items section expandable

        # Create frames for organization
        weapons_frame = ttk.LabelFrame(self, text="Weapons")
        weapons_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        armor_frame = ttk.LabelFrame(self, text="Armor & Shield")
        armor_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        items_frame = ttk.LabelFrame(self, text="Traveler's Outfit & Items")
        items_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Weapons Section
        # List to display weapons
        weapon_columns = ("name", "accuracy", "damage", "durability", "effect")
        self.weapons_tree = ttk.Treeview(weapons_frame, columns=weapon_columns, show="headings")

        # Define column headings
        self.weapons_tree.heading("name", text="Name")
        self.weapons_tree.heading("accuracy", text="Accuracy")
        self.weapons_tree.heading("damage", text="Damage")
        self.weapons_tree.heading("durability", text="Durability")
        self.weapons_tree.heading("effect", text="Effect")

        # Define column widths
        self.weapons_tree.column("name", width=120)
        self.weapons_tree.column("accuracy", width=70)
        self.weapons_tree.column("damage", width=70)
        self.weapons_tree.column("durability", width=70)
        self.weapons_tree.column("effect", width=150)

        # Add scrollbar
        weapons_scrollbar = ttk.Scrollbar(weapons_frame, orient=tk.VERTICAL, command=self.weapons_tree.yview)
        self.weapons_tree.configure(yscrollcommand=weapons_scrollbar.set)

        # Position widgets
        self.weapons_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        weapons_scrollbar.grid(row=0, column=1, padx=0, pady=5, sticky="ns")

        # Make tree expandable
        weapons_frame.columnconfigure(0, weight=1)
        weapons_frame.rowconfigure(0, weight=1)

        # Buttons for adding/removing weapons
        weapon_button_frame = ttk.Frame(weapons_frame)
        weapon_button_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(weapon_button_frame, text="Add Weapon", command=self._add_weapon).pack(side=tk.LEFT, padx=5)
        ttk.Button(weapon_button_frame, text="Edit Weapon", command=self._edit_weapon).pack(side=tk.LEFT, padx=5)
        ttk.Button(weapon_button_frame, text="Remove Weapon", command=self._remove_weapon).pack(side=tk.LEFT, padx=5)

        # Armor & Shield Section
        # Shield info
        ttk.Label(armor_frame, text="Shield:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.shield_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.shield_var, font=("Helvetica", 10, "bold")).grid(row=0, column=1,
                                                                                                  padx=5, pady=5,
                                                                                                  sticky="w")

        ttk.Label(armor_frame, text="Defense:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.shield_defense_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.shield_defense_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(armor_frame, text="Durability:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.shield_durability_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.shield_durability_var).grid(row=2, column=1, padx=5, pady=5,
                                                                             sticky="w")

        ttk.Label(armor_frame, text="Effect:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.shield_effect_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.shield_effect_var, wraplength=150).grid(row=3, column=1, padx=5,
                                                                                         pady=5, sticky="w")

        # Shield buttons
        shield_button_frame = ttk.Frame(armor_frame)
        shield_button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(shield_button_frame, text="Set Shield", command=self._set_shield).pack(side=tk.LEFT, padx=5)
        ttk.Button(shield_button_frame, text="Remove Shield", command=self._remove_shield).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(armor_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, padx=5, pady=10,
                                                              sticky="ew")

        # Armor info
        ttk.Label(armor_frame, text="Armor:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.armor_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.armor_var, font=("Helvetica", 10, "bold")).grid(row=6, column=1,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="w")

        ttk.Label(armor_frame, text="Defense Points:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.armor_defense_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.armor_defense_var).grid(row=7, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(armor_frame, text="Penalty:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.armor_penalty_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.armor_penalty_var).grid(row=8, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(armor_frame, text="Durability:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.armor_durability_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.armor_durability_var).grid(row=9, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(armor_frame, text="Effect:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.armor_effect_var = tk.StringVar()
        ttk.Label(armor_frame, textvariable=self.armor_effect_var, wraplength=150).grid(row=10, column=1, padx=5,
                                                                                        pady=5, sticky="w")

        # Armor buttons
        armor_button_frame = ttk.Frame(armor_frame)
        armor_button_frame.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(armor_button_frame, text="Set Armor", command=self._set_armor).pack(side=tk.LEFT, padx=5)
        ttk.Button(armor_button_frame, text="Remove Armor", command=self._remove_armor).pack(side=tk.LEFT, padx=5)

        # Traveler's Outfit & Items Section
        # List to display items
        item_columns = ("name", "size", "durability", "effect")
        self.items_tree = ttk.Treeview(items_frame, columns=item_columns, show="headings")

        # Define column headings
        self.items_tree.heading("name", text="Name")
        self.items_tree.heading("size", text="Size")
        self.items_tree.heading("durability", text="Durability")
        self.items_tree.heading("effect", text="Effect")

        # Define column widths
        self.items_tree.column("name", width=150)
        self.items_tree.column("size", width=50)
        self.items_tree.column("durability", width=70)
        self.items_tree.column("effect", width=300)

        # Add scrollbar
        items_scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

        # Position widgets
        self.items_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        items_scrollbar.grid(row=0, column=1, padx=0, pady=5, sticky="ns")

        # Make tree expandable
        items_frame.columnconfigure(0, weight=1)
        items_frame.rowconfigure(0, weight=1)

        # Buttons for adding/removing items
        item_button_frame = ttk.Frame(items_frame)
        item_button_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Button(item_button_frame, text="Add Item", command=self._add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(item_button_frame, text="Edit Item", command=self._edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(item_button_frame, text="Remove Item", command=self._remove_item).pack(side=tk.LEFT, padx=5)

        # Total Item Size display
        self.total_size_var = tk.StringVar(value="Total Size: 0")
        ttk.Label(item_button_frame, textvariable=self.total_size_var).pack(side=tk.RIGHT, padx=10)

    def _add_weapon(self):
        """Open dialog to add a new weapon"""
        dialog = WeaponDialog(self, "Add Weapon", None)
        weapon = dialog.result

        if weapon:
            # Add to character's weapons list
            self.app_controller.character.weapons.append(weapon)
            self._refresh_weapons_list()
            self.app_controller.mark_unsaved_changes()

    def _edit_weapon(self):
        """Open dialog to edit selected weapon"""
        selected = self.weapons_tree.selection()
        if not selected:
            messagebox.showinfo("Edit Weapon", "Please select a weapon to edit.")
            return

        # Get index of selected weapon
        index = int(selected[0])
        if 0 <= index < len(self.app_controller.character.weapons):
            weapon = self.app_controller.character.weapons[index]
            dialog = WeaponDialog(self, "Edit Weapon", weapon)

            if dialog.result:
                # Update weapon in character's list
                self.app_controller.character.weapons[index] = dialog.result
                self._refresh_weapons_list()
                self.app_controller.mark_unsaved_changes()

    def _remove_weapon(self):
        """Remove selected weapon"""
        selected = self.weapons_tree.selection()
        if not selected:
            messagebox.showinfo("Remove Weapon", "Please select a weapon to remove.")
            return

        # Get index of selected weapon
        index = int(selected[0])
        if 0 <= index < len(self.app_controller.character.weapons):
            # Remove from character's list
            self.app_controller.character.weapons.pop(index)
            self._refresh_weapons_list()
            self.app_controller.mark_unsaved_changes()

    def _set_shield(self):
        """Open dialog to set character's shield"""
        dialog = ShieldDialog(self, "Set Shield", self.app_controller.character.shield)
        shield = dialog.result

        if shield:
            # Set character's shield
            self.app_controller.character.shield = shield
            self._refresh_shield_display()
            self.app_controller.mark_unsaved_changes()

    def _remove_shield(self):
        """Remove character's shield"""
        self.app_controller.character.shield = None
        self._refresh_shield_display()
        self.app_controller.mark_unsaved_changes()

    def _set_armor(self):
        """Open dialog to set character's armor"""
        dialog = ArmorDialog(self, "Set Armor", self.app_controller.character.armor)
        armor = dialog.result

        if armor:
            # Set character's armor
            self.app_controller.character.armor = armor
            self._refresh_armor_display()
            self.app_controller.mark_unsaved_changes()

    def _remove_armor(self):
        """Remove character's armor"""
        self.app_controller.character.armor = None
        self._refresh_armor_display()
        self.app_controller.mark_unsaved_changes()

    def _add_item(self):
        """Open dialog to add a new item"""
        dialog = ItemDialog(self, "Add Item", None)
        item = dialog.result

        if item:
            # Add to character's items list
            self.app_controller.character.travelers_outfit.append(item)
            self._refresh_items_list()
            self.app_controller.mark_unsaved_changes()

    def _edit_item(self):
        """Open dialog to edit selected item"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Edit Item", "Please select an item to edit.")
            return

        # Get index of selected item
        index = int(selected[0])
        if 0 <= index < len(self.app_controller.character.travelers_outfit):
            item = self.app_controller.character.travelers_outfit[index]
            dialog = ItemDialog(self, "Edit Item", item)

            if dialog.result:
                # Update item in character's list
                self.app_controller.character.travelers_outfit[index] = dialog.result
                self._refresh_items_list()
                self.app_controller.mark_unsaved_changes()

    def _remove_item(self):
        """Remove selected item"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Remove Item", "Please select an item to remove.")
            return

        # Get index of selected item
        index = int(selected[0])
        if 0 <= index < len(self.app_controller.character.travelers_outfit):
            # Remove from character's list
            self.app_controller.character.travelers_outfit.pop(index)
            self._refresh_items_list()
            self.app_controller.mark_unsaved_changes()

    def _refresh_weapons_list(self):
        """Refresh the weapons treeview"""
        # Clear existing items
        for item in self.weapons_tree.get_children():
            self.weapons_tree.delete(item)

        # Add weapons from character
        for i, weapon in enumerate(self.app_controller.character.weapons):
            self.weapons_tree.insert("", tk.END, iid=str(i), values=(
                weapon.name,
                weapon.accuracy,
                weapon.damage,
                weapon.durability,
                weapon.effect
            ))

    def _refresh_shield_display(self):
        """Refresh the shield information display"""
        shield = self.app_controller.character.shield

        if shield:
            self.shield_var.set(shield.name)
            self.shield_defense_var.set(str(shield.defense))
            self.shield_durability_var.set(str(shield.durability))
            self.shield_effect_var.set(shield.effect)
        else:
            self.shield_var.set("None")
            self.shield_defense_var.set("")
            self.shield_durability_var.set("")
            self.shield_effect_var.set("")

    def _refresh_armor_display(self):
        """Refresh the armor information display"""
        armor = self.app_controller.character.armor

        if armor:
            self.armor_var.set(armor.name)
            self.armor_defense_var.set(str(armor.defense_points))
            self.armor_penalty_var.set(str(armor.penalty))
            self.armor_durability_var.set(str(armor.durability))
            self.armor_effect_var.set(armor.effect)
        else:
            self.armor_var.set("None")
            self.armor_defense_var.set("")
            self.armor_penalty_var.set("")
            self.armor_durability_var.set("")
            self.armor_effect_var.set("")

    def _refresh_items_list(self):
        """Refresh the items treeview"""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Add items from character
        for i, item in enumerate(self.app_controller.character.travelers_outfit):
            self.items_tree.insert("", tk.END, iid=str(i), values=(
                item.name,
                item.size,
                item.durability,
                item.effect
            ))

        # Update total size
        total_size = sum(item.size for item in self.app_controller.character.travelers_outfit)
        self.total_size_var.set(f"Total Size: {total_size}")

    def update_from_character(self, character):
        """Update UI from character model"""
        self._refresh_weapons_list()
        self._refresh_shield_display()
        self._refresh_armor_display()
        self._refresh_items_list()


class WeaponDialog(tk.Toplevel):
    """Dialog for adding/editing weapons"""

    def __init__(self, parent, title, weapon=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.result = None
        self.weapon = weapon  # Existing weapon or None for new

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Initialize fields if editing
        if self.weapon:
            self._initialize_fields()

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Accuracy field
        ttk.Label(frame, text="Accuracy:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.accuracy_var = tk.IntVar(value=0)
        ttk.Spinbox(frame, from_=-10, to=10, textvariable=self.accuracy_var, width=5).grid(row=1, column=1, padx=5,
                                                                                           pady=5, sticky="w")

        # Damage field
        ttk.Label(frame, text="Damage:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.damage_var = tk.IntVar(value=0)
        ttk.Spinbox(frame, from_=-10, to=10, textvariable=self.damage_var, width=5).grid(row=2, column=1, padx=5,
                                                                                         pady=5, sticky="w")

        # Durability field
        ttk.Label(frame, text="Durability:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.durability_var = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=1, to=20, textvariable=self.durability_var, width=5).grid(row=3, column=1, padx=5,
                                                                                           pady=5, sticky="w")

        # Effect field
        ttk.Label(frame, text="Effect:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.effect_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.effect_var, width=30).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _initialize_fields(self):
        """Initialize fields with existing weapon data"""
        self.name_var.set(self.weapon.name)
        self.accuracy_var.set(self.weapon.accuracy)
        self.damage_var.set(self.weapon.damage)
        self.durability_var.set(self.weapon.durability)
        self.effect_var.set(self.weapon.effect)

    def _on_ok(self):
        """Handle OK button click"""
        # Validate required fields
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required.")
            return

        # Create weapon object
        self.result = Weapon(
            name=self.name_var.get(),
            effect=self.effect_var.get(),
            durability=self.durability_var.get(),
            accuracy=self.accuracy_var.get(),
            damage=self.damage_var.get()
        )

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click"""
        self.destroy()


class ShieldDialog(tk.Toplevel):
    """Dialog for adding/editing shields"""

    def __init__(self, parent, title, shield=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.result = None
        self.shield = shield  # Existing shield or None for new

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Initialize fields if editing
        if self.shield:
            self._initialize_fields()

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Defense field
        ttk.Label(frame, text="Defense:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.defense_var = tk.IntVar(value=1)
        ttk.Spinbox(frame, from_=1, to=10, textvariable=self.defense_var, width=5).grid(row=1, column=1, padx=5, pady=5,
                                                                                        sticky="w")

        # Durability field
        ttk.Label(frame, text="Durability:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.durability_var = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=1, to=20, textvariable=self.durability_var, width=5).grid(row=2, column=1, padx=5,
                                                                                           pady=5, sticky="w")

        # Effect field
        ttk.Label(frame, text="Effect:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.effect_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.effect_var, width=30).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _initialize_fields(self):
        """Initialize fields with existing shield data"""
        self.name_var.set(self.shield.name)
        self.defense_var.set(self.shield.defense)
        self.durability_var.set(self.shield.durability)
        self.effect_var.set(self.shield.effect)

    def _on_ok(self):
        """Handle OK button click"""
        # Validate required fields
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required.")
            return

        # Create shield object
        self.result = Shield(
            name=self.name_var.get(),
            effect=self.effect_var.get(),
            durability=self.durability_var.get(),
            defense=self.defense_var.get()
        )

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click"""
        self.destroy()


class ArmorDialog(tk.Toplevel):
    """Dialog for adding/editing armor"""

    def __init__(self, parent, title, armor=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.result = None
        self.armor = armor  # Existing armor or None for new

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Initialize fields if editing
        if self.armor:
            self._initialize_fields()

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Defense Points field
        ttk.Label(frame, text="Defense Points:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.defense_var = tk.IntVar(value=1)
        ttk.Spinbox(frame, from_=1, to=10, textvariable=self.defense_var, width=5).grid(row=1, column=1, padx=5, pady=5,
                                                                                        sticky="w")

        # Penalty field
        ttk.Label(frame, text="Penalty:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.penalty_var = tk.IntVar(value=0)
        ttk.Spinbox(frame, from_=0, to=5, textvariable=self.penalty_var, width=5).grid(row=2, column=1, padx=5, pady=5,
                                                                                       sticky="w")

        # Durability field
        ttk.Label(frame, text="Durability:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.durability_var = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=1, to=20, textvariable=self.durability_var, width=5).grid(row=3, column=1, padx=5,
                                                                                           pady=5, sticky="w")

        # Effect field
        ttk.Label(frame, text="Effect:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.effect_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.effect_var, width=30).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _initialize_fields(self):
        """Initialize fields with existing armor data"""
        self.name_var.set(self.armor.name)
        self.defense_var.set(self.armor.defense_points)
        self.penalty_var.set(self.armor.penalty)
        self.durability_var.set(self.armor.durability)
        self.effect_var.set(self.armor.effect)

    def _on_ok(self):
        """Handle OK button click"""
        # Validate required fields
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required.")
            return

        # Create armor object
        self.result = Armor(
            name=self.name_var.get(),
            effect=self.effect_var.get(),
            durability=self.durability_var.get(),
            defense_points=self.defense_var.get(),
            penalty=self.penalty_var.get()
        )

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click"""
        self.destroy()


class ItemDialog(tk.Toplevel):
    """Dialog for adding/editing items"""

    def __init__(self, parent, title, item=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.result = None
        self.item = item  # Existing item or None for new

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Initialize fields if editing
        if self.item:
            self._initialize_fields()

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Size field
        ttk.Label(frame, text="Size:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.size_var = tk.IntVar(value=1)
        ttk.Spinbox(frame, from_=0, to=10, textvariable=self.size_var, width=5).grid(row=1, column=1, padx=5, pady=5,
                                                                                     sticky="w")

        # Durability field
        ttk.Label(frame, text="Durability:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.durability_var = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=0, to=20, textvariable=self.durability_var, width=5).grid(row=2, column=1, padx=5,
                                                                                           pady=5, sticky="w")

        # Effect field
        ttk.Label(frame, text="Effect:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.effect_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.effect_var, width=30).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side=tk.LEFT, padx=5)

    def _initialize_fields(self):
        """Initialize fields with existing item data"""
        self.name_var.set(self.item.name)
        self.size_var.set(self.item.size)
        self.durability_var.set(self.item.durability)
        self.effect_var.set(self.item.effect)

    def _on_ok(self):
        """Handle OK button click"""
        # Validate required fields
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required.")
            return

        # Create item object
        self.result = Item(
            name=self.name_var.get(),
            effect=self.effect_var.get(),
            durability=self.durability_var.get(),
            size=self.size_var.get()
        )

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click"""
        self.destroy()