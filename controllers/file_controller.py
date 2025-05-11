import json
import os
import datetime
from pathlib import Path
from models.character import Character


class FileController:
    """Controller for file operations (save, load, export)"""

    def __init__(self, app_controller=None):
        self.app_controller = app_controller
        self.default_save_dir = os.path.join(os.path.expanduser("~"), "RyuutamaCharacters")
        # Ensure save directory exists
        os.makedirs(self.default_save_dir, exist_ok=True)

    def save_character(self, character, file_path=None):
        """Save character to JSON file"""
        if file_path is None:
            # Generate default filename based on character name
            filename = f"{character.name or 'unnamed'}.json"
            file_path = os.path.join(self.default_save_dir, filename)

        # Convert character to dictionary
        character_dict = character.to_dict()

        # Save to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(character_dict, f, ensure_ascii=False, indent=2)

        return file_path

    def load_character(self, file_path):
        """Load character from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                character_dict = json.load(f)

            # Create Character object from dictionary
            character = Character.from_dict(character_dict)
            return character
        except Exception as e:
            print(f"Error loading character: {e}")
            return None

    def export_to_pdf(self, character, file_path=None):
        """Export character to PDF"""
        from utils.pdf_exporter import PDFExporter

        if file_path is None:
            # Generate default filename based on character name and date
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            filename = f"{character.name or 'unnamed'}_{date_str}.pdf"
            file_path = os.path.join(self.default_save_dir, filename)

        exporter = PDFExporter()
        result = exporter.export_character(character, file_path)

        return result, file_path

    def get_recent_characters(self, max_count=5):
        """Get list of recently saved characters"""
        character_files = []

        # List all JSON files in save directory
        for filename in os.listdir(self.default_save_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.default_save_dir, filename)
                modified_time = os.path.getmtime(file_path)
                character_files.append((file_path, modified_time))

        # Sort by modification time (newest first)
        character_files.sort(key=lambda x: x[1], reverse=True)

        # Return file paths for the most recent files
        return [file_path for file_path, _ in character_files[:max_count]]

    def get_character_preview(self, file_path):
        """Get a preview of character information from a save file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                character_dict = json.load(f)

            # Extract basic info for preview
            preview = {
                "name": character_dict.get("name", "Unnamed"),
                "level": character_dict.get("level", 1),
                "class": character_dict.get("character_class", ""),
                "type": character_dict.get("type", ""),
                "file_path": file_path,
                "last_modified": datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                ).strftime("%Y-%m-%d %H:%M")
            }

            return preview
        except Exception as e:
            print(f"Error reading character preview: {e}")
            return None