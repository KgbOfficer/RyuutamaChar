# Ryuutama Character Sheet Application

A digital character sheet for the Ryuutama tabletop role-playing game. This application allows you to create, edit, save, and export character sheets for Ryuutama.

## Features

- Create and manage character information
- Track stats, equipment, and status effects
- Handle travel rules, terrain, and weather effects
- Save characters to reuse between sessions
- Export character sheets to PDF for printing

## Installation

### Requirements

- Python 3.7 or higher
- Tkinter (usually included with Python)
- ReportLab (for PDF export)
- sv-ttk (for modern theming)

### Install Dependencies

```bash
pip install reportlab sv-ttk
```

### Running the Application

```bash
# Navigate to the project directory
cd ryuutama_character_sheet

# Run the application
python main.py
```

## Usage

### Creating a New Character

1. Launch the application
2. Fill in the character information in the "Character" tab
3. Set stats in the "Stats" tab
4. Add equipment in the "Equipment" tab
5. Save your character using File → Save or Ctrl+S

### Loading a Character

1. Use File → Open Character or Ctrl+O
2. Select a previously saved character file

### Exporting to PDF

1. Use File → Export to PDF
2. Choose a location to save the PDF
3. The PDF can be printed or shared with your game group

## Tabs Overview

### Character Tab

Basic character information, class details, and background information.

### Stats Tab

Character stats (STR, DEX, INT, SPI), derived stats (initiative), and abilities/spells by level.

### Equipment Tab

Manage weapons, armor, shield, and items in the traveler's outfit.

### Travel Tab

Set terrain and weather conditions, and see their effects on your character's stats for travel checks.

### Conditions Tab

Track status effects, perform condition checks for recovery, and note any special conditions.

## File Format

Character data is stored in JSON format with the following structure:

- Basic character information
- Stats
- Equipment
- Status effects
- Terrain and weather
- Notes and additional information

## License

This application is unofficial and is not affiliated with or endorsed by the creators of Ryuutama.

Ryuutama is a tabletop role-playing game created by Atsuhiro Okada.

## Credits

Developed by: [Your Name]