#!/usr/bin/env python3
"""
Ryuutama Character Sheet Application
A digital character sheet for the Ryuutama tabletop RPG
"""

import os
import sys
import tkinter as tk

# Ensure we can import from parent directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import needed modules
from views.main_window import MainWindow


def ensure_directories():
    """Create necessary directories if they don't exist"""
    # Default save directory
    save_dir = os.path.join(os.path.expanduser("~"), "RyuutamaCharacters")
    os.makedirs(save_dir, exist_ok=True)


def main():
    """Main application entry point"""
    # Ensure directories exist
    ensure_directories()

    # Create root window
    root = tk.Tk()
    root.title("Ryuutama Character Sheet")

    # Set application icon (if available)
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "ryuutama_icon.png")
    if os.path.exists(icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
        except Exception as e:
            print(f"Failed to load application icon: {e}")

    # Create main window
    app = MainWindow(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")

    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()