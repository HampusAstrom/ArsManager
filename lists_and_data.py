genabilities = ["Animal Handling",
                "Area Lore 1",
                "Area Lore 2",
                "Area Lore 3",
                "Athletics",
                "Awareness",
                "Bargain",
                "Brawl",
                "Carouse",
                "Charm",
                "Chirurgy",
                "Concentration",
                "Craft 1",
                "Craft 2",
                "Craft 3",
                "Etiquette",
                "Folk Ken",
                "Guile",
                "Hunt",
                "Intrigue",
                "Leadership",
                "Legerdemain",
                "Native Language",
                "Foreign Language 1",
                "Foreign Language 2",
                "Music",
                "Order of Hermes Lore",
                "(Organization) Lore 1",
                "(Organization) Lore 2",
                "Profession (Type)",
                "Ride",
                "Stealth",
                "Survival",
                "Swim",
                "Teaching",]
acaabitilites = ["Artes Liberales",
                "Civil and Canon Law",
                "Islamic Law",
                "Common Law",
                "Latin",
                "Classic Greek",
                "Arabic",
                "(Dead Language)",
                "Medicine",
                "Philosophiae",
                "Theology",]
arcabilities = ["Code of Hermes",
                "Dominion Lore",
                "Faerie Lore",
                "Finesse",
                "Infernal Lore",
                "Magic Lore",
                "Magic Theory",
                "Parma Magica",
                "Penetration",]
marabilities = ["Bows",
                "Great Weapon",
                "Single Weapon",
                "Thrown Weapon",]
supabilities = ["Animal Ken",
                "Dowsing",
                "Enchanting Music",
                "Entrancement",
                "Magic Sensitivity",
                "Premonitions",
                "Second Sight",
                "Sense Holiness and Unholiness",
                "Shapeshifter",
                "Wilderness Sense",]

skill_areas = ["Magic",
               "Adventure",
               "Social",
               "Martial",
               "Discretion",
               "Academic",
               "Travel",
               "Crafts",
               "Performance",
               "Religion",
               "Governance",
               "Lores",
               "Medicine",
               "Supernatural",]

magic = {"Magic Theory": 20,
         "Latin": 4,
         "Parma Magica": 3,
         "Classic Greek": 0.5,
         "Artes Liberales": 3,
         "Philosophiae": 2,
         "Teaching": 0.5,
         "Order of Hermes Lore": 1,
         "House Lore": 0.2,
         "Covenant Lore": 0.1,
         "Code of Hermes": 0.5,
         "Magic Lore": 1,
         "Faerie Lore": 0.2,
         "Dominion Lore": 0.05,
         "Infernal Lore": 0.05,
         "Concentration": 1,
         "Finesse": 1,
         "Penetration": 1,
         "Awareness": 0.3,
         }

adventure = {"Awareness": 5,
             "Area Lore 1": 2,
             "Athletics": 0.5,
             "Ride": 1,
             "Animal Handling": 0.5,
             "Survival": 1,
             "Hunt": 0.2,
             "Area Lore 1": 1,
             "Area Lore 2": 1,
             "Foreign Language 1": 0.2,
             "Folk Ken": 0.2,
             "Stealth": 1,
             "Swim": 0.2,
             "Bows": 0.3,
             "Single Weapon": 0.3,
             "Chirurgy": 0.2,
             "Medicine": 0.05,
             }

social = {"Bargain": 1,
          "Carouse": 1,
          "Charm": 1,
          "Etiquette": 1,
          "Folk Ken": 2,
          "Guile": 1,
          "Intrigue": 1,
          "Leadership": 0.8,
          "Native Language": 0.3,
          "Forein Language 1": 0.3,
          "Order of Hermes Lore": 0.2, # assumes covenant member, cut if not
          "(Organization) Lore 1": 0.2,
          "Artes Liberales": 1,
          }

martial = {"Bows": 5,
           "Great Weapon": 5, 
           "Single Weapon": 5, 
           "Thrown Weapon": 2,
           "Brawl": 3,
           "Awareness": 1,
           "Athletics": 1,
           "Ride": 0.3,
           "Chirurgy": 0.3,
           "Hunt": 0.2,
           "Leadership": 0.1,
           "Stealth": 0.2,
           "Survival": 0.2,
           }

discression = {"Stealth": 10,
               "Legerdemain": 3,
               "Awareness": 5,
               "Athletics": 1,
               "Guile": 5,
               "Intrigue": 0.5,
               "Folk Ken": 1,
               "Foreign Language 1": 0.2,
               }

academic = {"Artes Liberales": 5,
            "Latin": 3,
            "Classic Greek": 1,
            "Teaching": 2,
            "Philosophiae": 3,
            "Theology": 1,
            "Civil and Canon Law": 0.3,
            "Native Language": 0.2,
            "Foreign Language 1": 0.1,
            "Foreign Language 2": 0.1,
            "(Organization) Lore 1": 0.2,
            "Profession Scribe": 0.3,
            "(Dead Language)": 0.1,
            }

travel = {"Ride": 3,
          "Animal Handling": 1,
          "Area Lore 1": 2,
          "Area Lore 2": 2,
          "Area Lore 3": 2,
          "Foreign Language 1": 1,
          "Foreign Language 2": 1,
          "Athletics": 1,
          "Awareness": 0.5,
          "Bargain": 2,
          "Hunt": 0.5,
          "Stealth": 0.2,
          "Survival": 0.8,
          "Swim": 0.2,
          "Artes Liberales": 0.8,
          "Profession Sailor": 0.4,
          "Latin": 0.5,
          "Classic Greek": 0.5,
          "Arabic": 0.5,
          }

crafts = {"Craft 1": 5,
          "Craft 2": 3,
          "Craft 3": 0.5,
          "Bargain": 2,
          "Guild Lore": 1,
          "Leadership": 0.3,
          "Philosophiae": 1, # assumes mage, cut if not
          "Finesse": 0.5, # assumes mage, cut if not
          }

performance = {"Music": 5, # might just be music or atheletics, remove one if needed
               "Athletics": 2,
               "Carouse": 0.5,
               "Concentation": 0.3,
               "Folk Ken": 0.5,
               }

religion = {"Theology": 5,
            "Civil and Canon Law": 5, # remove Canon or Islamic depening on religion
            "Church Lore": 2,
            "Latin": 1, # remove Latin or Arabic depening on religion
            "Classic Greek": 0.5,
            "Artes Liberales": 0.5,
            "Philosophiae": 0.3,
            "Dominion Lore": 0.2,
            "Infernal Lore": 0.05,
            "Music": 0.1,
            }

governance = {"Artes Liberales": 3,
              "Civil and Canon Law": 5,
              "Philosophiae": 1,
              "Latin": 0.5, # remove Latin, Greek or Arabic depening on region
              "(Organization) Lore 1": 3,
              "(Organization) Lore 2": 0.5,
              "Profession (Type)": 0.5,
              "Leadership": 0.3,
              "Bargain": 0.3,
              "Intrigue": 0.5,
              }

# most here assumes covenant member, cut if not
lores = {"Magic Lore": 2, 
         "Dominion Lore": 1,
         "Faerie Lore": 1,
         "Infernal Lore": 0.2,
         "Order of Hermes Lore": 0.3,
         "House Lore": 0.4,
         "Code of Hermes": 0.1,
         "Area Lore 1": 0.3,
         "Area Lore 2": 0.1,
         "(Dead Language)": 0.5,
         }

medicine = {"Medicine": 10,
            "Chirurgy": 5,
            "Artes Liberales": 1,
            "Philosophiae": 2,
            }

supernatural = {"Animal Ken": 1,
                "Dowsing": 1,
                "Enchanting Music": 1,
                "Entrancement": 1,
                "Magic Sensitivity": 1,
                "Premonitions": 1,
                "Second Sight": 1,
                "Sense Holiness and Unholiness": 1,
                "Shapeshifter": 1,
                "Wilderness Sense": 1,
                }

# replacement lists start with what stat to replace, then what it's replaced by
# and what factor to multipy its value with
greek_shift = {"Latin": [["Classic Greek", 1],],
               "Classic Greek": [["Latin", 1],],
               "Church Lore": [["Orthodox Church Lore", 1],],
               }

arabic_shift = {"Latin": [["Arabic", 1],],
               "Civil and Canon Law": [["Islamic Law", 1],],
               "Church Lore": [["Sunni Lore", 1],], # reprecents org lore, change if shia
               }

english_shift = {"Civil and Canon Law": [["Common Law", 1],
                                         ["Civil and Canon Law", 0.3]],
                }
