from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import os


class PDFExporter:
    """Utility for exporting character data to PDF format"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Create a character sheet style
        self.styles.add(ParagraphStyle(
            name='CharacterTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            alignment=1,  # Center alignment
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            spaceBefore=8,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='SmallText',
            fontName='Helvetica',
            fontSize=8
        ))

    def _create_basic_info_table(self, character):
        """Create a table with basic character information"""
        # Basic information section
        basic_info = [
            [
                Paragraph("<b>Character Name:</b>", self.styles['Normal']),
                Paragraph(character.name, self.styles['Normal']),
                Paragraph("<b>Player Name:</b>", self.styles['Normal']),
                Paragraph(character.player_name, self.styles['Normal'])
            ],
            [
                Paragraph("<b>Level:</b>", self.styles['Normal']),
                Paragraph(str(character.level), self.styles['Normal']),
                Paragraph("<b>Experience:</b>", self.styles['Normal']),
                Paragraph(str(character.exp), self.styles['Normal'])
            ],
            [
                Paragraph("<b>Class:</b>", self.styles['Normal']),
                Paragraph(character.character_class, self.styles['Normal']),
                Paragraph("<b>Type:</b>", self.styles['Normal']),
                Paragraph(character.type, self.styles['Normal'])
            ],
            [
                Paragraph("<b>Gender:</b>", self.styles['Normal']),
                Paragraph(character.gender, self.styles['Normal']),
                Paragraph("<b>Age:</b>", self.styles['Normal']),
                Paragraph(str(character.age), self.styles['Normal'])
            ]
        ]

        info_table = Table(basic_info, colWidths=[1.0 * inch, 1.2 * inch, 1.0 * inch, 1.1 * inch])
        info_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return info_table

    def export_character(self, character, file_path):
        """Export character to PDF file"""
        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                leftMargin=0.5 * inch,
                rightMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch
            )

            # Build the PDF content
            elements = []

            # Add title
            elements.append(Paragraph(f"Ryuutama Character Sheet - {character.name}", self.styles['CharacterTitle']))
            elements.append(Spacer(1, 0.1 * inch))

            # Create a table for character image and basic info side by side
            if hasattr(character, 'image_path') and character.image_path and os.path.exists(character.image_path):
                try:
                    # Add character image if available
                    img = Image(character.image_path, width=1.5 * inch, height=1.5 * inch)

                    # Create a table with image and basic info
                    data = [[img, self._create_basic_info_table(character)]]
                    image_table = Table(data, colWidths=[1.7 * inch, 4.3 * inch])
                    image_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (0, 0), 'TOP'),
                        ('VALIGN', (1, 0), (1, 0), 'TOP'),
                    ]))
                    elements.append(image_table)
                except:
                    # If image loading fails, just add basic info
                    elements.append(self._create_basic_info_table(character))
            else:
                # No image, just add basic info
                elements.append(self._create_basic_info_table(character))

            elements.append(Spacer(1, 0.2 * inch))

            # Class details
            elements.append(Paragraph("Class Details", self.styles['SectionTitle']))

            class_details = [
                [
                    Paragraph("<b>Class Skills:</b>", self.styles['Normal']),
                    Paragraph(character.class_skill, self.styles['Normal']),
                    Paragraph("<b>Stats Used:</b>", self.styles['Normal']),
                    Paragraph(character.stats_used, self.styles['Normal'])
                ],
                [
                    Paragraph("<b>Effect:</b>", self.styles['Normal']),
                    Paragraph(character.effect, self.styles['Normal']),
                    Paragraph("<b>Mastered Weapon:</b>", self.styles['Normal']),
                    Paragraph(character.mastered_weapon, self.styles['Normal'])
                ],
                [
                    Paragraph("<b>Specialized Terrain:</b>", self.styles['Normal']),
                    Paragraph(character.specialized_terrain, self.styles['Normal']),
                    Paragraph("<b>Personal Item:</b>", self.styles['Normal']),
                    Paragraph(character.personal_item, self.styles['Normal'])
                ]
            ]

            class_table = Table(class_details, colWidths=[1.2 * inch, 1.8 * inch, 1.2 * inch, 1.8 * inch])
            class_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(class_table)
            elements.append(Spacer(1, 0.2 * inch))

            # Stats section
            elements.append(Paragraph("Character Stats", self.styles['SectionTitle']))

            # Create a table for the character stats
            stats_data = [
                [
                    Paragraph("<b>STR</b>", self.styles['Normal']),
                    Paragraph(f"{character.str['value']} ({character.str['die_size']})", self.styles['Normal']),
                    Paragraph("<b>DEX</b>", self.styles['Normal']),
                    Paragraph(f"{character.dex['value']} ({character.dex['die_size']})", self.styles['Normal']),
                ],
                [
                    Paragraph("<b>INT</b>", self.styles['Normal']),
                    Paragraph(f"{character.int['value']} ({character.int['die_size']})", self.styles['Normal']),
                    Paragraph("<b>SPI</b>", self.styles['Normal']),
                    Paragraph(f"{character.spi['value']} ({character.spi['die_size']})", self.styles['Normal']),
                ],
                [
                    Paragraph("<b>Initiative</b>", self.styles['Normal']),
                    Paragraph(str(character.initiative), self.styles['Normal']),
                    Paragraph("<b>Fumble Points</b>", self.styles['Normal']),
                    Paragraph(str(character.fumble_points), self.styles['Normal']),
                ],
            ]

            stats_table = Table(stats_data, colWidths=[1 * inch, 1.5 * inch, 1 * inch, 1.5 * inch])
            stats_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.2 * inch))

            # Equipment section
            elements.append(Paragraph("Equipment", self.styles['SectionTitle']))

            # Weapons table
            if character.weapons:
                elements.append(Paragraph("Weapons", self.styles['Normal']))
                weapons_header = [
                    Paragraph("<b>Name</b>", self.styles['SmallText']),
                    Paragraph("<b>Accuracy</b>", self.styles['SmallText']),
                    Paragraph("<b>Damage</b>", self.styles['SmallText']),
                    Paragraph("<b>Durability</b>", self.styles['SmallText']),
                    Paragraph("<b>Effect</b>", self.styles['SmallText'])
                ]
                weapons_data = [weapons_header]

                for weapon in character.weapons:
                    weapons_data.append([
                        Paragraph(weapon.name, self.styles['SmallText']),
                        Paragraph(str(weapon.accuracy), self.styles['SmallText']),
                        Paragraph(str(weapon.damage), self.styles['SmallText']),
                        Paragraph(str(weapon.durability), self.styles['SmallText']),
                        Paragraph(weapon.effect, self.styles['SmallText'])
                    ])

                weapons_table = Table(weapons_data,
                                      colWidths=[1.2 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 2.4 * inch])
                weapons_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(weapons_table)
                elements.append(Spacer(1, 0.1 * inch))

            # Shield and Armor
            shield_armor_data = []

            if character.shield:
                shield_armor_data.append([
                    Paragraph("<b>Shield</b>", self.styles['SmallText']),
                    Paragraph(character.shield.name, self.styles['SmallText']),
                    Paragraph(f"Defense: {character.shield.defense}", self.styles['SmallText']),
                    Paragraph(f"Durability: {character.shield.durability}", self.styles['SmallText']),
                    Paragraph(character.shield.effect, self.styles['SmallText'])
                ])

            if character.armor:
                shield_armor_data.append([
                    Paragraph("<b>Armor</b>", self.styles['SmallText']),
                    Paragraph(character.armor.name, self.styles['SmallText']),
                    Paragraph(f"Defense: {character.armor.defense_points}", self.styles['SmallText']),
                    Paragraph(f"Penalty: {character.armor.penalty}", self.styles['SmallText']),
                    Paragraph(character.armor.effect, self.styles['SmallText'])
                ])

            if shield_armor_data:
                shield_armor_table = Table(shield_armor_data,
                                           colWidths=[0.8 * inch, 1.2 * inch, 1 * inch, 1 * inch, 2 * inch])
                shield_armor_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(shield_armor_table)
                elements.append(Spacer(1, 0.1 * inch))

            # Traveler's Outfit
            if character.travelers_outfit:
                elements.append(Paragraph("Traveler's Outfit", self.styles['Normal']))
                outfit_header = [
                    Paragraph("<b>Name</b>", self.styles['SmallText']),
                    Paragraph("<b>Size</b>", self.styles['SmallText']),
                    Paragraph("<b>Durability</b>", self.styles['SmallText']),
                    Paragraph("<b>Effect</b>", self.styles['SmallText'])
                ]
                outfit_data = [outfit_header]

                for item in character.travelers_outfit:
                    outfit_data.append([
                        Paragraph(item.name, self.styles['SmallText']),
                        Paragraph(str(item.size), self.styles['SmallText']),
                        Paragraph(str(item.durability), self.styles['SmallText']),
                        Paragraph(item.effect, self.styles['SmallText'])
                    ])

                outfit_table = Table(outfit_data, colWidths=[1.5 * inch, 0.8 * inch, 0.8 * inch, 2.9 * inch])
                outfit_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(outfit_table)
                elements.append(Spacer(1, 0.2 * inch))

            # Status Effects
            elements.append(Paragraph("Status Effects", self.styles['SectionTitle']))

            status_data = [
                [
                    Paragraph("<b>Effect</b>", self.styles['SmallText']),
                    Paragraph("<b>Active</b>", self.styles['SmallText']),
                    Paragraph("<b>Type</b>", self.styles['SmallText']),
                    Paragraph("<b>Recovery Stat</b>", self.styles['SmallText']),
                    Paragraph("<b>Effect</b>", self.styles['SmallText'])
                ]
            ]

            from models.conditions import StatusEffect

            for effect_name, is_active in character.status_effects.items():
                effect = StatusEffect(effect_name)
                status_data.append([
                    Paragraph(effect_name.capitalize(), self.styles['SmallText']),
                    Paragraph("Yes" if is_active else "No", self.styles['SmallText']),
                    Paragraph(effect.effect_type.capitalize(), self.styles['SmallText']),
                    Paragraph(effect.check_stat.upper(), self.styles['SmallText']),
                    Paragraph(effect.effect, self.styles['SmallText'])
                ])

            status_table = Table(status_data, colWidths=[1 * inch, 0.8 * inch, 0.8 * inch, 1.2 * inch, 2.2 * inch])
            status_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(status_table)
            elements.append(Spacer(1, 0.2 * inch))

            # Background and Notes
            elements.append(Paragraph("Background & Notes", self.styles['SectionTitle']))

            background_data = [
                [
                    Paragraph("<b>Hometown:</b>", self.styles['Normal']),
                    Paragraph(character.hometown, self.styles['Normal'])
                ],
                [
                    Paragraph("<b>Reason for Travel:</b>", self.styles['Normal']),
                    Paragraph(character.reason_for_travel, self.styles['Normal'])
                ],
                [
                    Paragraph("<b>Appearance:</b>", self.styles['Normal']),
                    Paragraph(character.appearance, self.styles['Normal'])
                ],
                [
                    Paragraph("<b>Notes:</b>", self.styles['Normal']),
                    Paragraph(character.notes, self.styles['Normal'])
                ]
            ]

            background_table = Table(background_data, colWidths=[1.5 * inch, 4.5 * inch])
            background_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(background_table)

            # Add abilities/spells if available
            if any(character.abilities.values()):
                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph("Abilities & Spells", self.styles['SectionTitle']))

                for level, abilities in character.abilities.items():
                    if abilities:
                        elements.append(Paragraph(f"Level {level}", self.styles['Normal']))
                        elements.append(Paragraph(abilities, self.styles['Normal']))
                        elements.append(Spacer(1, 0.1 * inch))

            # Build the PDF
            doc.build(elements)
            return True

        except Exception as e:
            print(f"Error exporting PDF: {e}")
            return False