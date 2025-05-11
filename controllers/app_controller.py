import os
import tkinter as tk
from tkinter import messagebox, filedialog
from models.character import Character
from controllers.file_controller import FileController


class AppController:
    """Main application controller"""

    def __init__(self, root=None):
        self.root = root
        self.character = Character()  # Current character
        self.file_controller = FileController(self)
        self.current_file_path = None  # Path to currently loaded file
        self.unsaved_changes = False  # Flag for tracking unsaved changes

        # References to UI elements that need updating
        self.ui_elements = {}

    def new_character(self):
        """Create a new blank character"""
        if self.unsaved_changes:
            if not self._confirm_discard_changes():
                return False

        self.character = Character()
        self.current_file_path = None
        self.unsaved_changes = False
        self._update_ui()
        self._update_window_title()
        return True

    def save_character(self, save_as=False):
        """Save the current character"""
        if self.current_file_path is None or save_as:
            initial_dir = self.file_controller.default_save_dir
            filename = f"{self.character.name or 'unnamed'}.json"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Ryuutama Character", "*.json"), ("All Files", "*.*")],
                initialdir=initial_dir,
                initialfile=filename
            )
            if not file_path:  # User cancelled
                return False
            self.current_file_path = file_path

        success = self.file_controller.save_character(self.character, self.current_file_path)
        if success:
            self.unsaved_changes = False
            self._update_window_title()
            messagebox.showinfo("Save Complete", "Character saved successfully.")
            return True
        else:
            messagebox.showerror("Save Error", "Failed to save character.")
            return False

    def load_character(self, file_path=None):
        """Load a character"""
        if self.unsaved_changes:
            if not self._confirm_discard_changes():
                return False

        if file_path is None:
            initial_dir = self.file_controller.default_save_dir
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("Ryuutama Character", "*.json"), ("All Files", "*.*")],
                initialdir=initial_dir
            )
            if not file_path:  # User cancelled
                return False

        loaded_character = self.file_controller.load_character(file_path)
        if loaded_character:
            self.character = loaded_character
            self.current_file_path = file_path
            self.unsaved_changes = False
            self._update_ui()
            self._update_window_title()
            return True
        else:
            messagebox.showerror("Load Error", "Failed to load character.")
            return False

    def export_to_pdf(self):
        """Export the current character to PDF"""
        # If character has no name, prompt to save first
        if not self.character.name:
            messagebox.showwarning(
                "Missing Information",
                "Please provide a character name before exporting to PDF."
            )
            return False

        initial_dir = self.file_controller.default_save_dir
        filename = f"{self.character.name}.pdf"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf"), ("All Files", "*.*")],
            initialdir=initial_dir,
            initialfile=filename
        )
        if not file_path:  # User cancelled
            return False

        success, saved_path = self.file_controller.export_to_pdf(self.character, file_path)
        if success:
            messagebox.showinfo(
                "Export Complete",
                f"Character exported to PDF successfully.\n\nSaved to: {saved_path}"
            )
            # Ask if user wants to open the PDF
            if messagebox.askyesno("Open PDF", "Would you like to open the PDF now?"):
                self._open_file(saved_path)
            return True
        else:
            messagebox.showerror("Export Error", "Failed to export character to PDF.")
            return False

    def mark_unsaved_changes(self):
        """Mark that there are unsaved changes"""
        self.unsaved_changes = True
        self._update_window_title()

    def register_ui_element(self, element_id, element_ref):
        """Register a UI element for updates"""
        self.ui_elements[element_id] = element_ref

    def _update_ui(self):
        """Update UI elements with current character data"""
        for element_id, element_ref in self.ui_elements.items():
            if hasattr(element_ref, "update_from_character"):
                element_ref.update_from_character(self.character)

    def _update_window_title(self):
        """Update the window title to show character name and save status"""
        if self.root:
            character_name = self.character.name or "Unnamed Character"
            unsaved_marker = "*" if self.unsaved_changes else ""
            title = f"Ryuutama Character Sheet - {character_name}{unsaved_marker}"
            self.root.title(title)

    def _confirm_discard_changes(self):
        """Ask user to confirm discarding unsaved changes"""
        return messagebox.askyesno(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to discard them and continue?"
        )

    def _open_file(self, file_path):
        """Open a file with the default system application"""
        import subprocess
        import sys
        import os

        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux
                subprocess.call(['xdg-open', file_path])
        except Exception as e:
            print(f"Error opening file: {e}")
            return False

        return True