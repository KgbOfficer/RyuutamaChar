import tkinter as tk
from tkinter import ttk, messagebox
from models.equipment import Weapon, Shield, Armor, Item


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


class RulebookWeaponDialog(tk.Toplevel):
    """Dialog for selecting and buying weapons from the rulebook"""

    def __init__(self, parent, title, weapons_data, available_gold):
        super().__init__(parent)
        self.title(title)
        self.minsize(700, 500)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.weapons_data = weapons_data
        self.available_gold = available_gold
        self.result = None

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Available gold display
        gold_frame = ttk.Frame(main_frame)
        gold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gold_frame, text=f"Available Gold: {self.available_gold}g", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT)

        # Create a treeview with scrollbar for weapon selection
        columns = ("name", "price", "size", "equip", "accuracy", "damage")
        self.weapons_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

        # Define headings
        self.weapons_tree.heading("name", text="Weapon")
        self.weapons_tree.heading("price", text="Price")
        self.weapons_tree.heading("size", text="Size")
        self.weapons_tree.heading("equip", text="Equip")
        self.weapons_tree.heading("accuracy", text="Accuracy")
        self.weapons_tree.heading("damage", text="Damage")

        # Define column widths
        self.weapons_tree.column("name", width=120)
        self.weapons_tree.column("price", width=80)
        self.weapons_tree.column("size", width=50)
        self.weapons_tree.column("equip", width=80)
        self.weapons_tree.column("accuracy", width=100)
        self.weapons_tree.column("damage", width=80)

        # Add scrollbar
        weapons_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.weapons_tree.yview)
        self.weapons_tree.configure(yscrollcommand=weapons_scrollbar.set)

        # Position widgets
        self.weapons_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        weapons_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load weapons data
        for weapon_name, weapon_info in self.weapons_data.items():
            self.weapons_tree.insert("", tk.END, iid=weapon_name, values=(
                weapon_name,
                f"{weapon_info['price']}g",
                weapon_info['size'],
                weapon_info['equip'],
                weapon_info['accuracy'],
                weapon_info['damage']
            ))

        # Bind selection event
        self.weapons_tree.bind("<<TreeviewSelect>>", self._on_weapon_select)

        # Description frame
        desc_frame = ttk.LabelFrame(main_frame, text="Weapon Description")
        desc_frame.pack(fill=tk.X, pady=10)

        self.description_var = tk.StringVar(value="Select a weapon to see its description")
        desc_label = ttk.Label(desc_frame, textvariable=self.description_var, wraplength=680)
        desc_label.pack(fill=tk.X, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Buy Weapon", command=lambda: self._on_select("buy")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Give Weapon", command=lambda: self._on_select("give")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _on_weapon_select(self, event):
        """Handle weapon selection in treeview"""
        selected = self.weapons_tree.selection()
        if selected:
            weapon_name = selected[0]
            weapon_info = self.weapons_data[weapon_name]
            self.description_var.set(weapon_info["description"])

    def _on_select(self, transaction_type):
        """Handle weapon selection - buy or give"""
        selected = self.weapons_tree.selection()
        if not selected:
            messagebox.showinfo("Select Weapon", "Please select a weapon from the list.")
            return

        weapon_name = selected[0]
        weapon_info = self.weapons_data[weapon_name]

        # If buying, check if they have enough gold
        if transaction_type == "buy" and self.available_gold < weapon_info["price"]:
            messagebox.showerror("Not Enough Gold",
                                 f"You need {weapon_info['price']} gold to buy this weapon, but you only have {self.available_gold} gold.")
            return

        # Create a weapon object
        from models.equipment import Weapon
        weapon = Weapon(
            name=weapon_name,
            effect=weapon_info["description"],
            durability=weapon_info["size"],  # Default durability to size
            accuracy=0,  # These will be calculated in-game based on stats
            damage=0
        )

        # Return the weapon and transaction type
        self.result = (weapon, transaction_type)
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


class RulebookItemDialog(tk.Toplevel):
    """Dialog for selecting and buying items from the rulebook"""

    def __init__(self, parent, title, items_data, available_gold):
        super().__init__(parent)
        self.title(title)
        self.minsize(800, 600)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.items_data = items_data
        self.available_gold = available_gold
        self.result = None

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Available gold display
        gold_frame = ttk.Frame(main_frame)
        gold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gold_frame, text=f"Available Gold: {self.available_gold}g", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT)

        # Create a category combobox
        category_frame = ttk.Frame(main_frame)
        category_frame.pack(fill=tk.X, pady=5)

        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(category_frame, textvariable=self.category_var,
                                              values=list(self.items_data.keys()), width=30, state="readonly")
        self.category_combobox.pack(side=tk.LEFT, padx=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self._on_category_selected)

        # Create a treeview with scrollbar for item selection
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("name", "price", "size", "bonus")
        self.items_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        # Define headings
        self.items_tree.heading("name", text="Item")
        self.items_tree.heading("price", text="Price")
        self.items_tree.heading("size", text="Size")
        self.items_tree.heading("bonus", text="Bonus/Effect")

        # Define column widths
        self.items_tree.column("name", width=150)
        self.items_tree.column("price", width=80)
        self.items_tree.column("size", width=50)
        self.items_tree.column("bonus", width=300)

        # Add scrollbar
        items_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

        # Position widgets
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.items_tree.bind("<<TreeviewSelect>>", self._on_item_select)

        # Description frame
        desc_frame = ttk.LabelFrame(main_frame, text="Item Description")
        desc_frame.pack(fill=tk.X, pady=10)

        self.description_var = tk.StringVar(value="Select a category and item to see its description")
        desc_label = ttk.Label(desc_frame, textvariable=self.description_var, wraplength=780)
        desc_label.pack(fill=tk.X, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Buy Item", command=lambda: self._on_select("buy")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Give Item", command=lambda: self._on_select("give")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _on_category_selected(self, event):
        """Handle category selection in combobox"""
        category = self.category_var.get()
        if not category:
            return

        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Load items for selected category
        for item_name, item_info in self.items_data[category].items():
            # Some items might have 'bonus' and others 'capacity' depending on the category
            bonus = item_info.get('bonus', item_info.get('capacity', '-'))

            self.items_tree.insert("", tk.END, iid=f"{category}: {item_name}", values=(
                item_name,
                f"{item_info['price']}g",
                item_info['size'],
                bonus
            ))

    def _on_item_select(self, event):
        """Handle item selection in treeview"""
        selected = self.items_tree.selection()
        if selected:
            category_and_name = selected[0]
            category, item_name = category_and_name.split(": ", 1)
            item_info = self.items_data[category][item_name]
            self.description_var.set(item_info["description"])

    def _on_select(self, transaction_type):
        """Handle item selection - buy or give"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showinfo("Select Item", "Please select an item from the list.")
            return

        category_and_name = selected[0]
        category, item_name = category_and_name.split(": ", 1)
        item_info = self.items_data[category][item_name]

        # If buying, check if they have enough gold
        if transaction_type == "buy" and self.available_gold < item_info["price"]:
            messagebox.showerror("Not Enough Gold",
                                 f"You need {item_info['price']} gold to buy this item, but you only have {self.available_gold} gold.")
            return

        # Create an item object
        from models.equipment import Item
        item = Item(
            name=item_name,
            effect=item_info["description"],
            durability=item_info.get("durability", item_info["size"]),  # Default durability to size if not specified
            size=item_info["size"]
        )

        # Add a reference to the category for display purposes
        item.category_and_name = category_and_name

        # Return the item and transaction type
        self.result = (item, transaction_type)
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


class RulebookShieldDialog(tk.Toplevel):
    """Dialog for selecting and buying shields from the rulebook"""

    def __init__(self, parent, title, shield_data, available_gold):
        super().__init__(parent)
        self.title(title)
        self.minsize(700, 400)
        self.transient(parent)  # Set to be on top of the main window
        self.grab_set()  # Make window modal

        self.shield_data = shield_data
        self.available_gold = available_gold
        self.result = None

        # Setup UI
        self._setup_ui()

        # Center on parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        # Wait for window to be closed
        self.wait_window()

    def _setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Available gold display
        gold_frame = ttk.Frame(main_frame)
        gold_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gold_frame, text=f"Available Gold: {self.available_gold}g", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT)

        # Create a treeview with scrollbar for shield selection
        columns = ("name", "price", "size", "equip", "defense", "penalty", "dodge")
        self.shields_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=5)

        # Define headings
        self.shields_tree.heading("name", text="Shield")
        self.shields_tree.heading("price", text="Price")
        self.shields_tree.heading("size", text="Size")
        self.shields_tree.heading("equip", text="Equip")
        self.shields_tree.heading("defense", text="Defense")
        self.shields_tree.heading("penalty", text="Penalty")
        self.shields_tree.heading("dodge", text="Dodge Value")

        # Define column widths
        self.shields_tree.column("name", width=120)
        self.shields_tree.column("price", width=80)
        self.shields_tree.column("size", width=50)
        self.shields_tree.column("equip", width=80)
        self.shields_tree.column("defense", width=80)
        self.shields_tree.column("penalty", width=80)
        self.shields_tree.column("dodge", width=100)

        # Add scrollbar
        shields_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.shields_tree.yview)
        self.shields_tree.configure(yscrollcommand=shields_scrollbar.set)

        # Position widgets
        self.shields_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shields_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load shield data
        for shield_name, shield_info in self.shield_data.items():
            self.shields_tree.insert("", tk.END, iid=shield_name, values=(
                shield_name,
                f"{shield_info['price']}g",
                shield_info['size'],
                shield_info['equip'],
                shield_info['defense'],
                shield_info['penalty'],
                shield_info['dodge']
            ))

        # Bind selection event
        self.shields_tree.bind("<<TreeviewSelect>>", self._on_shield_select)

        # Description frame
        desc_frame = ttk.LabelFrame(main_frame, text="Shield Description")
        desc_frame.pack(fill=tk.X, pady=10)

        self.description_var = tk.StringVar(value="Select a shield to see its description")
        desc_label = ttk.Label(desc_frame, textvariable=self.description_var, wraplength=680)
        desc_label.pack(fill=tk.X, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Buy Shield", command=lambda: self._on_select("buy")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Give Shield", command=lambda: self._on_select("give")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _on_shield_select(self, event):
        """Handle shield selection in treeview"""
        selected = self.shields_tree.selection()
        if selected:
            shield_name = selected[0]
            shield_info = self.shield_data[shield_name]
            self.description_var.set(shield_info["description"])

    def _on_select(self, transaction_type):
        """Handle shield selection - buy or give"""
        selected = self.shields_tree.selection()
        if not selected:
            messagebox.showinfo("Select Shield", "Please select a shield from the list.")
            return

        shield_name = selected[0]
        shield_info = self.shield_data[shield_name]

        # If buying, check if they have enough gold
        if transaction_type == "buy" and self.available_gold < shield_info["price"]:
            messagebox.showerror("Not Enough Gold",
                                 f"You need {shield_info['price']} gold to buy this shield, but you only have {self.available_gold} gold.")
            return

        # Create a shield object
        from models.equipment import Shield
        shield = Shield(
            name=shield_name,
            effect=shield_info["description"],
            durability=shield_info["size"],  # Default durability to size
            defense=shield_info["defense"]
        )

        # Return the shield and transaction type
        self.result = (shield, transaction_type)
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
            ttk.Spinbox(frame, from_=1, to=10, textvariable=self.defense_var, width=5).grid(row=1, column=1, padx=5,
                                                                                            pady=5,
                                                                                            sticky="w")

            # Penalty field
            ttk.Label(frame, text="Penalty:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.penalty_var = tk.IntVar(value=0)
            ttk.Spinbox(frame, from_=0, to=5, textvariable=self.penalty_var, width=5).grid(row=2, column=1, padx=5,
                                                                                           pady=5,
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

    class RulebookArmorDialog(tk.Toplevel):
        """Dialog for selecting and buying armor from the rulebook"""

        def __init__(self, parent, title, armor_data, available_gold):
            super().__init__(parent)
            self.title(title)
            self.minsize(700, 400)
            self.transient(parent)  # Set to be on top of the main window
            self.grab_set()  # Make window modal

            self.armor_data = armor_data
            self.available_gold = available_gold
            self.result = None

            # Setup UI
            self._setup_ui()

            # Center on parent
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

            # Wait for window to be closed
            self.wait_window()

        def _setup_ui(self):
            """Setup the dialog UI"""
            main_frame = ttk.Frame(self, padding=10)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Available gold display
            gold_frame = ttk.Frame(main_frame)
            gold_frame.pack(fill=tk.X, pady=5)
            ttk.Label(gold_frame, text=f"Available Gold: {self.available_gold}g", font=("Helvetica", 10, "bold")).pack(
                side=tk.LEFT)

            # Create a treeview with scrollbar for armor selection
            columns = ("name", "price", "size", "equip", "defense", "penalty")
            self.armor_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=5)

            # Define headings
            self.armor_tree.heading("name", text="Armor")
            self.armor_tree.heading("price", text="Price")
            self.armor_tree.heading("size", text="Size")
            self.armor_tree.heading("equip", text="Equip")
            self.armor_tree.heading("defense", text="Defense")
            self.armor_tree.heading("penalty", text="Penalty")

            # Define column widths
            self.armor_tree.column("name", width=120)
            self.armor_tree.column("price", width=80)
            self.armor_tree.column("size", width=50)
            self.armor_tree.column("equip", width=80)
            self.armor_tree.column("defense", width=80)
            self.armor_tree.column("penalty", width=80)

            # Add scrollbar
            armor_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.armor_tree.yview)
            self.armor_tree.configure(yscrollcommand=armor_scrollbar.set)

            # Position widgets
            self.armor_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            armor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Load armor data
            for armor_name, armor_info in self.armor_data.items():
                self.armor_tree.insert("", tk.END, iid=armor_name, values=(
                    armor_name,
                    f"{armor_info['price']}g",
                    armor_info['size'],
                    armor_info['equip'],
                    armor_info['defense'],
                    armor_info['penalty']
                ))

            # Bind selection event
            self.armor_tree.bind("<<TreeviewSelect>>", self._on_armor_select)

            # Description frame
            desc_frame = ttk.LabelFrame(main_frame, text="Armor Description")
            desc_frame.pack(fill=tk.X, pady=10)

            self.description_var = tk.StringVar(value="Select armor to see its description")
            desc_label = ttk.Label(desc_frame, textvariable=self.description_var, wraplength=680)
            desc_label.pack(fill=tk.X, padx=5, pady=5)

            # Buttons
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=10)

            ttk.Button(button_frame, text="Buy Armor", command=lambda: self._on_select("buy")).pack(side=tk.LEFT,
                                                                                                    padx=5)
            ttk.Button(button_frame, text="Give Armor", command=lambda: self._on_select("give")).pack(side=tk.LEFT,
                                                                                                      padx=5)
            ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        def _on_armor_select(self, event):
            """Handle armor selection in treeview"""
            selected = self.armor_tree.selection()
            if selected:
                armor_name = selected[0]
                armor_info = self.armor_data[armor_name]
                self.description_var.set(armor_info["description"])

        def _on_select(self, transaction_type):
            """Handle armor selection - buy or give"""
            selected = self.armor_tree.selection()
            if not selected:
                messagebox.showinfo("Select Armor", "Please select armor from the list.")
                return

            armor_name = selected[0]
            armor_info = self.armor_data[armor_name]

            # If buying, check if they have enough gold
            if transaction_type == "buy" and self.available_gold < armor_info["price"]:
                messagebox.showerror("Not Enough Gold",
                                     f"You need {armor_info['price']} gold to buy this armor, but you only have {self.available_gold} gold.")
                return

            # Create an armor object
            from models.equipment import Armor
            armor = Armor(
                name=armor_name,
                effect=armor_info["description"],
                durability=armor_info["size"],  # Default durability to size
                defense_points=armor_info["defense"],
                penalty=armor_info["penalty"]
            )

            # Return the armor and transaction type
            self.result = (armor, transaction_type)
            self.destroy()

class EquipmentTab(ttk.Frame):
    """Tab for character equipment and items"""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Register with controller
        self.app_controller.register_ui_element("equipment_tab", self)

        # Equipment data from the rulebook
        self._load_equipment_data()

        # Setup UI
        self._setup_ui()

    def _load_equipment_data(self):
        """Load equipment data from the rulebook"""
        # Weapons data (name, price, size, equip, accuracy, damage, description)
        self.weapons_data = {
            "Light Blade": {
                "price": 400, "size": 1, "equip": "1 hand",
                "accuracy": "DEX + INT +1", "damage": "INT -1",
                "description": "A blade that can be held in the hand. It can be useful outside of combat in the preparation of food, harvesting herbs, and various other situations."
            },
            "Blade": {
                "price": 700, "size": 3, "equip": "1 hand",
                "accuracy": "DEX + STR", "damage": "STR",
                "description": "A weapon with a long, flat blade. Beloved around the world, a single-edged blade is called a \"saber\" while double-edged blade is called a \"sword\"."
            },
            "Polearm": {
                "price": 350, "size": 3, "equip": "2 hands",
                "accuracy": "DEX + STR", "damage": "STR +1",
                "description": "A weapon consisting of a long pole with a sharp point fastened at the end. As it can be used to stab with the tip or bash with the handle, it has a wide breadth of usefulness. Its price also makes it easy to obtain."
            },
            "Axe": {
                "price": 500, "size": 3, "equip": "2 hands",
                "accuracy": "STR + STR -1", "damage": "STR",
                "description": "A tool used to cut down trees. Due to its weight, it is powered with brute strength, and not effective with small swings."
            },
            "Bow": {
                "price": 750, "size": 3, "equip": "2 hands",
                "accuracy": "INT + DEX -2", "damage": "DEX",
                "description": "A projectile tool used by hunters and the like. Since it can attack from afar, it is popular with nobles and soldiers. *Players don't need to keep track of arrows"
            }
        }

        # Armor data (name, price, size, equip, defense, penalty, description)
        self.armor_data = {
            "Clothes": {
                "price": 50, "size": 3, "equip": "Chest",
                "defense": 0, "penalty": 0,
                "description": "Normal clothes. Thick, tough clothing is preferred by travelers. Generally they are made from wool and thread."
            },
            "Light Armor": {
                "price": 900, "size": 3, "equip": "Chest",
                "defense": 1, "penalty": 0,
                "description": "Armor constructed from the hide of animals, with metal plates covering vital points. Only the chest is protected, but because of its light weight it is easily worn."
            },
            "Medium Armor": {
                "price": 2000, "size": 5, "equip": "Chest",
                "defense": 2, "penalty": -1,
                "description": "Armor constructed from metal plates. The arms and legs are protected in addition to the chest area, but the weight increases proportionally."
            },
            "Heavy Armor": {
                "price": 10000, "size": 5, "equip": "Chest",
                "defense": 3, "penalty": -3,
                "description": "Heavy armor constructed from metal plates that completely covers the entire body. The body's movement is restricted, so movement is hampered with the armor equipped."
            }
        }

        # Shield data (name, price, size, equip, defense, penalty, dodge, description)
        self.shield_data = {
            "Light shield": {
                "price": 400, "size": 3, "equip": "1 hand",
                "defense": 1, "penalty": 0, "dodge": 7,
                "description": "A shield that can be held in one hand. Made from wood and grass, its light weight keeps it from being a nuisance in battle."
            },
            "Heavy shield": {
                "price": 1200, "size": 3, "equip": "1 hand",
                "defense": 2, "penalty": -1, "dodge": 9,
                "description": "A shield large enough to cast half of the body in shadow. Most of them are made from metal; its heavy weight makes it hard to carry."
            }
        }

        # Items data (grouped by category)
        self.items_data = {
            "Shoes": {
                "Rain boots": {"price": 300, "size": 1, "bonus": "Rain/Hard Rain/Storm",
                               "description": "These boots have been finished with a coating that makes them resistant to water. They do a good job of keeping your feet dry."},
                "Walking shoes": {"price": 350, "size": 1, "bonus": "On a road",
                                  "description": "These shoes are made from soft leather that make it easy to walk on paved surfaces. They are very lightweight and do not impede the movement of your feet."},
                "Climbing shoes": {"price": 450, "size": 1, "bonus": "Wasteland/Rocky Terrain/Mountain/Alpine",
                                   "description": "These shoes have thick soles that allow walking across rocky terrain without hurting your feet. The soles also help to keep your feet from slipping."},
                "Snow boots": {"price": 500, "size": 1, "bonus": "Snow/Blizzard",
                               "description": "These shoes are specially finished to protect toes from frostbite."},
                "Mud boots": {"price": 500, "size": 1, "bonus": "Swamp",
                              "description": "These boots have wide soles that keep your feet from sinking into mud. They allow you to glide across the surface of the mud."},
                "Jungle boots": {"price": 600, "size": 1, "bonus": "Woods/Deep Forest/Jungle",
                                 "description": "These boots are made to help you traverse overgrown jungles. They offer complete protection for your feet and are extremely sturdy."}
            },
            "Capes": {
                "Windbreaker": {"price": 120, "size": 3, "bonus": "Strong wind",
                                "description": "A cape with a hood that covers the entire body. Weights are stitched into the cape to keep it from flapping around in the wind."},
                "Warm cape": {"price": 160, "size": 3, "bonus": "Cold",
                              "description": "A cape made from the pelt of a thickly-furred animal. It can also be used as bedding or a blanket."},
                "Raincoat": {"price": 400, "size": 3, "bonus": "Rain/Hard rain/Snow",
                             "description": "A leather cape that has been finished with a water-resistant coating. It requires constant upkeep."},
                "Camo cape": {"price": 400, "size": 3, "bonus": "Hide check +1 for chosen Terrain",
                              "description": "Choose a terrain when purchasing this item. This cape allows you to conceal your entire body by blending into the surrounding topography."},
                "Fire cape": {"price": 700, "size": 3, "bonus": "-1 fire damage",
                              "description": "A cape made from the fur of a fire-resistant monster. It is weak to water: If it gets wet, it will be ruined."},
                "Sun cape": {"price": 400, "size": 3, "bonus": "Hot",
                             "description": "A cape made from a light, very breathable material that keeps heat from reaching inside."}
            },
            "Staffs": {
                "Walking stick": {"price": 50, "size": 3, "bonus": "Level 3 or lower Terrain",
                                  "description": "A staff that is used by frail travelers. It is also useful when you have heavy bags. Its bonus only applies to weaker characters with STR of 4."},
                "Hiking staff": {"price": 100, "size": 3, "bonus": "Rocky terrain/Mountain",
                                 "description": "A staff that helps you keep your footing when climbing in high places. You can adjust the length."},
                "Snow staff": {"price": 280, "size": 3, "bonus": "Snow",
                               "description": "A staff used to dig through snow. The tip is reinforced with metal to help break through ice."}
            },
            "Hats": {
                "Cap": {"price": 120, "size": 1, "bonus": "-",
                        "description": "A normal hat. Hats and caps are believed to offer protection from evil. There are a variety of colors and shapes."},
                "Sun hat": {"price": 180, "size": 1, "bonus": "Hot",
                            "description": "A hat with a large brim to block sunlight. It is made from linen and thread for extra breathability."},
                "Woolen hat": {"price": 200, "size": 1, "bonus": "Cold",
                               "description": "A hat made from the pelt of a thickly-furred animal. It has ear covers to protect from frostbite."},
                "Sand hood": {"price": 340, "size": 1, "bonus": "Desert",
                              "description": "A hood that keeps wind and sandstorms from obscuring your vision. The material is thick and heavy but does not let direct sunlight through."}
            },
            "Accessories": {
                "Goggles": {"price": 4000, "size": 1, "bonus": "All Rain, Wind and Snow and related conditions",
                            "description": "A tool used to protect your eyes during rain, wind, snow, or other extreme weather. Since numerous techniques are required to create a single pair, the cost can be prohibitive."},
                "Accessory": {"price": 100, "size": 1, "bonus": "-",
                              "description": "Rings, earrings, bracelets, or any other decorative accessory. These can be created from metal, clam shells, seeds, or any other element that shows off the special colors of the land where it was created."}
            },
            "Containers": {
                "Waterskin": {"price": 30, "size": 1, "capacity": "-",
                              "description": "A pouch of leather that can hold a day's ration of water"},
                "Magic jar": {"price": 2000, "size": 1, "capacity": "-",
                              "description": "A magical jar that keeps cold liquids cold or hot liquids hot: +1 Travel. Check while in hot/cold weather"},
                "Travel bag": {"price": 10, "size": 1, "capacity": "3",
                               "description": "A bag held in 1 hand"},
                "Belt pouch": {"price": 30, "size": 1, "capacity": "2",
                               "description": "Only one can be equipped. Good when you want to be able to grab something quickly"},
                "Herb bottle": {"price": 100, "size": 3, "capacity": "-",
                                "description": "Magically keeps up to ten herbs fresh; once opened for the first time, the bottle is good for seven days before it no longer works."}
            },
            "Big Containers": {
                "Barrel": {"price": 10, "size": 5, "capacity": "10",
                           "description": "Holds 15 days worth of water, or holds 10 size worth of other items."},
                "Backpack": {"price": 20, "size": 3, "capacity": "5",
                             "description": "A rucksack used by many travelers"},
                "Large Backpack": {"price": 40, "size": 5, "capacity": "10",
                                   "description": "Large rucksack that holds many items"},
                "Wooden chest": {"price": 10, "size": 5, "capacity": "15",
                                 "description": "If carried by a human, they take a -1 penalty to Travel Checks"}
            },
            "Rations": {
                "Food": {"price": 5, "size": 1,
                         "description": "A single day's ration of food. Goes bad in 24 hours."},
                "Alcohol": {"price": 10, "size": 1,
                            "description": "If drunk when a character's Condition is 3 or less, gain [Muddled: 4]"},
                "Disgusting Rations": {"price": 5, "size": 1,
                                       "description": "Disgusting but edible. If eaten when character's Condition is 3 or less, lose half current MP"},
                "Rations": {"price": 10, "size": 1,
                            "description": "Portable food that can be taken on a trip"},
                "Delicious Rations": {"price": 70, "size": 1,
                                      "description": "When eaten, next day's Condition check gains a +1 bonus."},
                "Animal Feed": {"price": 5, "size": 1,
                                "description": "Needed when taking animals to the barren desert or alpine environments"}
            }
        }

    def _setup_ui(self):
        """Setup the UI elements"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)  # Make the items section expandable

        # Create frames for organization
        gold_frame = ttk.LabelFrame(self, text="Gold")
        gold_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        weapons_frame = ttk.LabelFrame(self, text="Weapons")
        weapons_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        armor_frame = ttk.LabelFrame(self, text="Armor & Shield")
        armor_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        items_frame = ttk.LabelFrame(self, text="Traveler's Outfit & Items")
        items_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Gold Section
        self.gold_var = tk.IntVar(value=1000)
        gold_entry_frame = ttk.Frame(gold_frame)
        gold_entry_frame.pack(padx=5, pady=5, fill=tk.X)

        ttk.Label(gold_entry_frame, text="Gold:").pack(side=tk.LEFT, padx=5)
        self.gold_entry = ttk.Entry(gold_entry_frame, textvariable=self.gold_var, width=10)
        self.gold_entry.pack(side=tk.LEFT, padx=5)
        self.gold_entry.bind("<KeyRelease>", self._on_gold_change)

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
        ttk.Button(weapon_button_frame, text="Buy Rulebook Weapon", command=self._buy_rulebook_weapon).pack(
            side=tk.LEFT, padx=5)

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
        ttk.Button(shield_button_frame, text="Buy Rulebook Shield", command=self._buy_rulebook_shield).pack(
            side=tk.LEFT, padx=5)

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
        ttk.Button(armor_button_frame, text="Buy Rulebook Armor", command=self._buy_rulebook_armor).pack(side=tk.LEFT,
                                                                                                         padx=5)

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
        ttk.Button(item_button_frame, text="Buy Rulebook Item", command=self._buy_rulebook_item).pack(side=tk.LEFT,
                                                                                                      padx=5)
        # Total Item Size display
        self.total_size_var = tk.StringVar(value="Total Size: 0")
        ttk.Label(item_button_frame, textvariable=self.total_size_var).pack(side=tk.RIGHT, padx=10)

    def _on_gold_change(self, event=None):
        """Handle gold amount change"""
        self._update_character_from_ui()
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

    def _update_character_from_ui(self):
        """Update character model from UI values"""
        character = self.app_controller.character

        # Make sure the character has a gold attribute
        if not hasattr(character, 'gold'):
            character.gold = self.gold_var.get()
        else:
            character.gold = self.gold_var.get()

    def update_from_character(self, character):
        """Update UI from character model"""
        # Update gold
        if hasattr(character, 'gold'):
            self.gold_var.set(character.gold)
        else:
            self.gold_var.set(1000)  # Default value
            character.gold = 1000

        self._refresh_weapons_list()
        self._refresh_shield_display()
        self._refresh_armor_display()
        self._refresh_items_list()

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

    def _buy_rulebook_weapon(self):
        """Open dialog to buy a weapon from the rulebook"""
        dialog = RulebookWeaponDialog(self, "Buy Rulebook Weapon", self.weapons_data, self.gold_var.get())
        result = dialog.result

        if not result:
            return

        weapon, transaction_type = result

        if transaction_type == "buy":
            # Check if character has enough gold
            weapon_price = self.weapons_data[weapon.name]["price"]
            if self.gold_var.get() < weapon_price:
                messagebox.showerror("Not Enough Gold",
                                     f"You need {weapon_price} gold to buy {weapon.name}, but you only have {self.gold_var.get()} gold.")
                return

            # Deduct gold
            self.gold_var.set(self.gold_var.get() - weapon_price)

        # Add to character's weapons list
        self.app_controller.character.weapons.append(weapon)
        self._refresh_weapons_list()
        self._update_character_from_ui()
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

    def _buy_rulebook_shield(self):
        """Open dialog to buy a shield from the rulebook"""
        dialog = RulebookShieldDialog(self, "Buy Rulebook Shield", self.shield_data, self.gold_var.get())
        result = dialog.result

        if not result:
            return

        shield, transaction_type = result

        if transaction_type == "buy":
            # Check if character has enough gold
            shield_price = self.shield_data[shield.name]["price"]
            if self.gold_var.get() < shield_price:
                messagebox.showerror("Not Enough Gold",
                                     f"You need {shield_price} gold to buy {shield.name}, but you only have {self.gold_var.get()} gold.")
                return

            # Deduct gold
            self.gold_var.set(self.gold_var.get() - shield_price)

        # Set character's shield
        self.app_controller.character.shield = shield
        self._refresh_shield_display()
        self._update_character_from_ui()
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

    def _buy_rulebook_armor(self):
        """Open dialog to buy armor from the rulebook"""
        dialog = RulebookArmorDialog(self, "Buy Rulebook Armor", self.armor_data, self.gold_var.get())
        result = dialog.result

        if not result:
            return

        armor, transaction_type = result

        if transaction_type == "buy":
            # Check if character has enough gold
            armor_price = self.armor_data[armor.name]["price"]
            if self.gold_var.get() < armor_price:
                messagebox.showerror("Not Enough Gold",
                                     f"You need {armor_price} gold to buy {armor.name}, but you only have {self.gold_var.get()} gold.")
                return

            # Deduct gold
            self.gold_var.set(self.gold_var.get() - armor_price)

        # Set character's armor
        self.app_controller.character.armor = armor
        self._refresh_armor_display()
        self._update_character_from_ui()
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

    def _buy_rulebook_item(self):
        """Open dialog to buy an item from the rulebook"""
        dialog = RulebookItemDialog(self, "Buy Rulebook Item", self.items_data, self.gold_var.get())
        result = dialog.result

        if not result:
            return

        item, transaction_type = result

        if transaction_type == "buy":
            # Extract price from the selected item
            category, item_name = item.category_and_name.split(": ", 1)
            item_price = self.items_data[category][item_name]["price"]

            # Check if character has enough gold
            if self.gold_var.get() < item_price:
                messagebox.showerror("Not Enough Gold",
                                     f"You need {item_price} gold to buy {item_name}, but you only have {self.gold_var.get()} gold.")
                return

            # Deduct gold
            self.gold_var.set(self.gold_var.get() - item_price)

        # Add to character's items list
        self.app_controller.character.travelers_outfit.append(item)
        self._refresh_items_list()
        self._update_character_from_ui()
        self.app_controller.mark_unsaved_changes()