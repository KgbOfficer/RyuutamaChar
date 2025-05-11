import tkinter as tk
from tkinter import ttk
import sv_ttk
import sys
import os

# Ensure we can import from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.character_tab import CharacterTab
from views.stats_tab import StatsTab
from views.equipment_tab import EquipmentTab
from views.travel_tab import TravelTab
from views.conditions_tab import ConditionsTab
from controllers.app_controller import AppController


class MainWindow:
    """Main application window with tabbed interface"""

    def __init__(self, root):
        self.root = root
        self.root.title("Ryuutama Character Sheet")
        self.root.minsize(800, 600)
        self.root.geometry("900x700")

        # Apply SV-TTK theme
        sv_ttk.set_theme("light")

        # Create app controller
        self.app_controller = AppController(self.root)

        # Setup UI
        self._setup_menu()
        self._setup_tabs()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Character", command=self.app_controller.new_character, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Character...", command=self.app_controller.load_character,
                              accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=lambda: self.app_controller.save_character(False),
                              accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=lambda: self.app_controller.save_character(True),
                              accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Export to PDF...", command=self.app_controller.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)

        menubar.add_cascade(label="File", menu=file_menu)

        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: sv_ttk.set_theme("light"))
        theme_menu.add_command(label="Dark Theme", command=lambda: sv_ttk.set_theme("dark"))

        menubar.add_cascade(label="Theme", menu=theme_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)

        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.app_controller.new_character())
        self.root.bind("<Control-o>", lambda e: self.app_controller.load_character())
        self.root.bind("<Control-s>", lambda e: self.app_controller.save_character(False))
        self.root.bind("<Control-Shift-S>", lambda e: self.app_controller.save_character(True))

    def _setup_tabs(self):
        """Create tabbed interface"""
        # Create notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.character_tab = CharacterTab(self.notebook, self.app_controller)
        self.stats_tab = StatsTab(self.notebook, self.app_controller)
        self.equipment_tab = EquipmentTab(self.notebook, self.app_controller)
        self.travel_tab = TravelTab(self.notebook, self.app_controller)
        self.conditions_tab = ConditionsTab(self.notebook, self.app_controller)

        # Add tabs to notebook
        self.notebook.add(self.character_tab, text="Character")
        self.notebook.add(self.stats_tab, text="Stats")
        self.notebook.add(self.equipment_tab, text="Equipment")
        self.notebook.add(self.travel_tab, text="Travel")
        self.notebook.add(self.conditions_tab, text="Conditions")

    def _show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Ryuutama Character Sheet")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.transient(self.root)  # Set to be on top of the main window

        # Center on screen
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f"{width}x{height}+{x}+{y}")

        # Add content
        frame = ttk.Frame(about_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="Ryuutama Character Sheet",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            frame,
            text="A digital character sheet for the Ryuutama tabletop RPG",
            wraplength=350
        ).pack(pady=(0, 20))

        ttk.Label(
            frame,
            text="Ryuutama is a tabletop role-playing game created by Atsuhiro Okada.",
            wraplength=350
        ).pack(pady=(0, 10))

        ttk.Label(
            frame,
            text="This application is unofficial and is not affiliated with or endorsed by the creators of Ryuutama.",
            wraplength=350
        ).pack(pady=(0, 20))

        ttk.Button(
            frame,
            text="Close",
            command=about_window.destroy
        ).pack()

    def _on_close(self):
        """Handle window close event"""
        if self.app_controller.unsaved_changes:
            if not self._confirm_exit():
                return

        self.root.destroy()

    def _confirm_exit(self):
        """Ask user to confirm exit with unsaved changes"""
        from tkinter import messagebox
        return messagebox.askyesno(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to exit anyway?"
        )