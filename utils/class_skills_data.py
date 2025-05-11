"""
Ryuutama Character Sheet - Class Skills Data
This module contains the data for class skills
"""

# Class skills data structure
CLASS_SKILLS = {
    "Minstrel": {
        "skills": ["Well-traveled", "Knowledge of Tradition", "Music"],
        "descriptions": {
            "Well-traveled": {
                "description": "As a minstrel who makes their earning by constant travel, you've learned how to travel safely.",
                "effect": "+1 to Journey Checks (Travel/Direction/Camping Checks; always in effect)",
                "usable": "-",
                "stat_used": "-",
                "tn": "-"
            },
            "Knowledge of Tradition": {
                "description": "The people you have met on your travels have taught you their old songs and legends. You have learned a great deal about the world in this way.",
                "effect": "You can get more information about the things you see and hear.",
                "usable": "Anytime you come across something interesting",
                "stat_used": "[INT + INT]",
                "tn": "GM's discretion"
            },
            "Music": {
                "description": "You can play music that reinvigorates your companions. Once per scenario you may choose one terrain or weather type you are currently traveling through and gain it as a song. For example, if your character is currently in a rainy grassland, they might learn 'Rain Song' or 'Ballad of the Grassland,' but not 'Desert Rumba.' You may later use the song only if it matches the specific condition in which it was acquired: for example, 'Rain Song' can be used anytime it is raining, regardless of terrain. You can name your song whatever you like.",
                "effect": "Give all party members a +1 bonus to their next roll. Critical: +3 bonus. Fumble: Any PCs with Condition of 6 or less gain the [Muddled: 6] status effect.",
                "usable": "Usable when in a suitable area. Each use reduces the Minstrel's HP by 1",
                "stat_used": "[DEX + SPI]",
                "tn": "Topography"
            }
        }
    },
    "Merchant": {
        "skills": ["Well-spoken", "Animal Owner", "Trader"],
        "descriptions": {
            "Well-spoken": {
                "description": "As a merchant who earns their keep by trading, your communication skills are top notch.",
                "effect": "Negotiation Check [INT + SPI] gets +1, always in effect",
                "usable": "Any Negotiation Check",
                "stat_used": "-",
                "tn": "-"
            },
            "Animal Owner": {
                "description": "You have learned how to raise animals that will help you carry your goods. Normally, only one animal can be taken on a Journey for free (without paying their daily food and water costs). With this skill, you can keep more animals without incurring their food and water costs.",
                "effect": "You can keep 2 more animals for a total of 3 without paying for their food and water.",
                "usable": "-",
                "stat_used": "-",
                "tn": "-"
            },
            "Trader": {
                "description": "When you go shopping, you can buy items cheaply and sell items at a higher price. However, in order to do so, you must buy or sell at least four items of the same type at once. When buying, you must have enough money to buy all the items at their normal price. If you succeed on the check, the price of the items will change. If you fail a check when buying, you cannot cancel the deal: You must buy the goods at full price.",
                "effect": "You may buy items at a reduced price or sell items at an increased value.",
                "usable": "When selling/buying 4 or more of the same item",
                "stat_used": "[INT + SPI]",
                "tn": "See table (6-7: 10%, 8-9: 20%, 10-13: 40%, 14-17: 60%, 18+: 80%)"
            }
        }
    },
    "Hunter": {
        "skills": ["Animal Tracking", "Trapping", "Hunting"],
        "descriptions": {
            "Animal Tracking": {
                "description": "You can track four types of monsters (animal, phantom beast, demonstone, or phantom plant) by following their prints and spoor. You will also receive a +1 bonus to damage against a monster tracked using this skill.",
                "effect": "Find a monster's location. +1 bonus to damage against any monsters found.",
                "usable": "When finding an animal's tracks",
                "stat_used": "[STR + INT]",
                "tn": "Topography"
            },
            "Trapping": {
                "description": "You are able to harvest valuable materials, such as leather or food, from defeated monsters. The type of item you receive on a success is shown in the Monster's entry in the Dragonica.",
                "effect": "Harvest materials from a defeated Monster",
                "usable": "After defeating a monster",
                "stat_used": "[DEX + INT]",
                "tn": "Monster level x2"
            },
            "Hunting": {
                "description": "You are able to catch small wild animals for food. This skill is used just before the camp check is made, however, if you decide to go hunting, you cannot also help set up camp. The higher the result of the check, the more food you catch.",
                "effect": "Receive a number of rations equal to Check result – target number, but cannot participate in the camp check. Critical: All food is Delicious. Fumble: Afflicted by [Injury: 6] status effect",
                "usable": "Before camp check, once per day",
                "stat_used": "[DEX + INT]",
                "tn": "Topography"
            }
        }
    },
    "Healer": {
        "skills": ["Healing", "First Aid", "Herb Gathering"],
        "descriptions": {
            "Healing": {
                "description": "You heal a companion's injuries by creating a secret remedy from Healing Herbs and water. Any Healing Herb may be used, but the process takes time, so this skill is less effective if used during combat.",
                "effect": "Target character recovers HP equal to the result of [INT + SPI]. During combat, recover only the result of [INT] (only 1 die.)",
                "usable": "Spend 1 Healing Herb",
                "stat_used": "[INT + SPI] (During combat, [INT] only)",
                "tn": "None"
            },
            "First Aid": {
                "description": "You can relieve a character's status effect for one hour. This also reduces the strength of the status ailment by your current level. If this reduces the strength of the status ailment to 0 or below, the status effect is immediately cured. A character may only receive First Aid once per day, regardless of whether or not the check is successful.",
                "effect": "Relieve a character's status effect for 1 hour. Then, reduce that status effect's strength permanently by a number equal to the Healer's level.",
                "usable": "A character with a status effect who has not yet received first aid today",
                "stat_used": "[INT + SPI]",
                "tn": "Status effect's strength"
            },
            "Herb Gathering": {
                "description": "You know where to find potent Healing Herbs. Once each morning, when you succeed on this Skill Check, you can explore the wilderness to obtain a Healing Herb. The Healing Herb obtained depends on the current terrain.",
                "effect": "Find a single Healing Herb. Critical: Find 3 Healing Herbs. Fumble: Afflicted with [Poison: 6]",
                "usable": "Once each morning, before the Travel check",
                "stat_used": "[STR + INT]",
                "tn": "Topography"
            }
        }
    },
    "Farmer": {
        "skills": ["Robust", "Animal Owner", "Side-Job"],
        "descriptions": {
            "Robust": {
                "description": "Thanks to your healthy lifestyle, your body is sturdy, and you are in tune with its natural rhythm. You are naturally resistant to ill effects and can carry more items.",
                "effect": "+1 bonus to Condition Checks. +3 bonus to Carrying Capacity",
                "usable": "-",
                "stat_used": "-",
                "tn": "-"
            },
            "Animal Owner": {
                "description": "You have learned how to raise animals that will help you carry your goods. Normally, only one animal can be taken on a Journey for free (without paying their daily food and water costs). With this skill, you can keep more animals without incurring their food and water costs.",
                "effect": "You can keep 2 more animals for a total of 3 without paying for their food and water.",
                "usable": "-",
                "stat_used": "-",
                "tn": "-"
            },
            "Side-Job": {
                "description": "Since a farmer's life can be tough without extra money in the off-season, you've taken up another job on the side. When you choose the Farmer Class, choose a single Skill from any other class that requires a Skill Check. You may use that skill as if you were a member of that class. However, you aren't as practiced as a person of that class, so you will always have a -1 penalty to the check.",
                "effect": "Use a single skill from another class with a -1 penalty",
                "usable": "Depends on the skill",
                "stat_used": "Depends on the skill",
                "tn": "Depends on the skill"
            }
        }
    },
    "Artisan": {
        "skills": ["Trapping", "Crafting", "Repair"],
        "descriptions": {
            "Trapping": {
                "description": "You are able to harvest valuable materials, such as leather or food, from defeated monsters. The type of item you receive on a success is shown in the Monster's entry in the Dragonica.",
                "effect": "Take materials from a defeated Monster",
                "usable": "After defeating a monster",
                "stat_used": "[DEX + INT]",
                "tn": "Monster level x2"
            },
            "Crafting": {
                "description": "You can use this skill to make handy, cute, beautiful or delicious things. If you have time and tools, you can make things during your Journey. Each craft is different, and so are the things each character can make. When choosing the Artisan class, choose a single category from this list: Weapons, Armor, Shoes, Capes, Staves, Hats, Accessories, Food, Sundries, Camping Equipment, or Containers.",
                "effect": "Make an item from your specialization. Choose the specialization category when choosing this class.",
                "usable": "Anytime you have the time (1 day per size) and materials (1/2 the gold cost)",
                "stat_used": "[STR + DEX]",
                "tn": "See table"
            },
            "Repair": {
                "description": "You can repair damaged items, restoring their durability to full. Use the table to determine the Repair Check target number. This costs 10% of the item's value, regardless of success or failure. You may retry a failed skill check, but you must pay the cost again.",
                "effect": "Repair an item and return its durability to its original value",
                "usable": "Anytime you have the time (1 day per size) and materials (10% the gold cost)",
                "stat_used": "[STR + DEX]",
                "tn": "See table (Price: ≤100g: 6, ≤1000g: 8, ≤10,000g: 10, ≤100,000g: 14, More: 18)"
            }
        }
    },
    "Noble": {
        "skills": ["Etiquette", "Refined Education", "Weapon Grace"],
        "descriptions": {
            "Etiquette": {
                "description": "Due to your long years of tutelage and experience in noble society, you are aware of the importance of proper etiquette. When speaking to someone of rank or status, you are able to leave them with a positive impression of you when you win a contested Etiquette check.",
                "effect": "Leave a positive impression on someone of high rank or status.",
                "usable": "Conversing with someone of rank or status",
                "stat_used": "[DEX + INT]",
                "tn": "contested"
            },
            "Refined Education": {
                "description": "After years of study under a learned tutor, you have memorized facts and trivia about many aspects of the world. You know more than the average person about history, famous people and well-traveled places.",
                "effect": "Know detailed information about the things you see or hear.",
                "usable": "Seeing or hearing something.",
                "stat_used": "[INT + INT]",
                "tn": "GM's discretion"
            },
            "Weapon Grace": {
                "description": "After long years of practice and extensive training under a master-at-arms, you have learned to be graceful when wielding a certain weapon. When creating your character, choose either Blade, Polearm or Bow. You receive this weapon as a Mastered Weapon. If you already have this chosen category as a Mastered Weapon, you receive a +1 bonus to your Accuracy checks when using a weapon from that category.",
                "effect": "Choose Blade/Polearm/Bow; it becomes an additional Mastered Weapon. If chosen category is already a Mastered Weapon, gain +1 bonus to Accuracy checks.",
                "usable": "-",
                "stat_used": "-",
                "tn": "-"
            }
        }
    }
}