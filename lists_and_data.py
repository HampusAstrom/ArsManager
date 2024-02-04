CHARACTERISTICS = ["Int", "Per", "Str", "Sta", "Pre", "Com", "Dex", "Qik",]

GENABILITIES = ["Animal Handling",
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
ACAABILITIES = ["Artes Liberales",
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
ARCABILITIES = ["Code of Hermes",
                "Dominion Lore",
                "Faerie Lore",
                "Finesse",
                "Infernal Lore",
                "Magic Lore",
                "Magic Theory",
                "Parma Magica",
                "Penetration",]
MARABILITIES = ["Bows",
                "Great Weapon",
                "Single Weapon",
                "Thrown Weapon",]
SUPABILITIES = ["Animal Ken",
                "Dowsing",
                "Enchanting Music",
                "Entrancement",
                "Magic Sensitivity",
                "Premonitions",
                "Second Sight",
                "Sense Holy and Unholy",
                "Shapeshifter",
                "Wilderness Sense",]

TECHNIQUES = ["Cr","In","Mu","Pe","Re",]

FORMS = ["An","Aq","Au","Co","He","Ig","Im","Me","Te","Vi",]

MAGIC = {"Magic Theory": 20,
         "Latin": 0.5,
         "Parma Magica": 5,
         "Classic Greek": 0.5,
         "Artes Liberales": 2,
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
         "Concentration": 1.5,
         "Finesse": 2,
         "Penetration": 2,
         "Awareness": 0.3,
         }

ADVENTURE = {"Awareness": 5,
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

SOCIAL = {"Bargain": 1,
          "Carouse": 1,
          "Charm": 1,
          "Etiquette": 1,
          "Folk Ken": 2,
          "Guile": 1,
          "Intrigue": 1,
          "Leadership": 0.8,
          "Native Language": 0.3,
          "Foreign Language 1": 0.3,
          "Order of Hermes Lore": 0.2, # assumes covenant member, cut if not
          "(Organization) Lore 1": 0.2,
          "Artes Liberales": 1,
          }

MARTIAL = {"Bows": 5,
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

DISCRETION = {"Stealth": 10,
               "Legerdemain": 3,
               "Awareness": 5,
               "Athletics": 1,
               "Guile": 5,
               "Intrigue": 0.5,
               "Folk Ken": 1,
               "Foreign Language 1": 0.2,
               }

ACADEMIC = {"Artes Liberales": 5,
            "Latin": 3,
            "Classic Greek": 1,
            "Teaching": 2,
            "Philosophiae": 3,
            "Theology": 0.5,
            "Civil and Canon Law": 0.3,
            "Native Language": 0.2,
            "Foreign Language 1": 0.1,
            "Foreign Language 2": 0.1,
            "(Organization) Lore 1": 0.2,
            "Profession Scribe": 0.3,
            "(Dead Language)": 0.1,
            }

TRAVEL = {"Ride": 3,
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

CRAFTS = {"Craft 1": 5,
          "Craft 2": 3,
          "Craft 3": 0.5,
          "Bargain": 2,
          "Guild Lore": 1,
          "Leadership": 0.3,
          "Philosophiae": 1, # assumes mage, cut if not
          "Finesse": 0.5, # assumes mage, cut if not
          }

PERFORMANCE = {"Music": 5, # might just be music or atheletics, remove one if needed
               "Athletics": 2,
               "Carouse": 0.5,
               "Concentration": 0.3,
               "Folk Ken": 0.5,
               }

RELIGION = {"Theology": 5,
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

GOVERNANCE = {"Artes Liberales": 3,
              "Civil and Canon Law": 5,
              "Code of Hermes": 1,
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
LORES = {"Magic Lore": 2,
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

MEDICINE = {"Medicine": 10,
            "Chirurgy": 5,
            "Artes Liberales": 1,
            "Philosophiae": 2,
            }

SUPERNATURAL = {"Animal Ken": 1,
                "Dowsing": 1,
                "Enchanting Music": 1,
                "Entrancement": 1,
                "Magic Sensitivity": 1,
                "Premonitions": 1,
                "Second Sight": 1,
                "Sense Holy and Unholy": 1,
                "Shapeshifter": 1,
                "Wilderness Sense": 1,
                }

# skill areas with respective dictionaries and default prio
SKILL_AREAS = {"Magic": (MAGIC, 20),
               "Adventure": (ADVENTURE, 2),
               "Social": (SOCIAL, 1),
               "Martial": (MARTIAL, 0.1),
               "Discretion": (DISCRETION, 0.2),
               "Academic": (ACADEMIC, 0.5),
               "Travel": (TRAVEL, 0.2),
               "Crafts": (CRAFTS, 0.2),
               "Performance": (PERFORMANCE, 0.2),
               "Religion": (RELIGION, 0.1),
               "Governance": (GOVERNANCE, 0.07),
               "Lores": (LORES, 0.3),
               "Medicine": (MEDICINE, 0.1),
               "Supernatural": (SUPERNATURAL, 0.05),
               # supernatural is special, if positive select only one skill
               }

# replacement lists start with what stat to replace, then what it's replaced by
# and what factor to multipy its value with
GREEK_SHIFT = {"Latin": [["Classic Greek", 1],],
               "Classic Greek": [["Latin", 1],],
               "Church Lore": [["Orthodox Church Lore", 1],],
               }

ARABIC_SHIFT = {"Latin": [["Arabic", 1],],
               "Civil and Canon Law": [["Islamic Law", 1],],
               "Church Lore": [["Sunni Lore", 1],], # reprecents org lore, change if shia
               }

ENGLISH_SHIFT = {"Civil and Canon Law": [["Common Law", 1],
                                         ["Civil and Canon Law", 0.3]],
                }

ABILITY_ARRAYS = {"default": [5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1,],
                  "even": [5, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,],
                  "uneven": [6, 5, 4, 3, 3, 2, 2, 1, 1, 1,],
                  "extreme": [7, 5, 4, 3, 2, 2, 1, 1,],
                  }

ABILITY_ARRAYS_PRIO = {"default": 2,
                  "even": 1,
                  "uneven": 1,
                  "extreme": 0.5,
                  }

TECH_ARRAYS = {"default": [9, 6, 3, 2, 0],
                  "even": [8, 5, 5, 3, 2],
                  "uneven": [10, 5, 3, 0, 0],
                  "extreme": [11, 3, 2, 0, 0],
                  }

TECH_ARRAYS_PRIO = {"default": 1,
                  "even": 0.5,
                  "uneven": 2,
                  "extreme": 0.5,
                  }

FORM_ARRAYS = {"default": [10, 8, 1, 0, 0, 0, 0, 0, 0, 0,],
                  "even": [8, 6, 5, 4, 3, 2, 1, 0, 0, 0,],
                  "uneven": [12, 4, 2, 1, 0, 0, 0, 0, 0, 0,],
                  "extreme": [13, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
                  }

FORM_ARRAYS_PRIO = {"default": 2,
                  "even": 0.5,
                  "uneven": 1,
                  "extreme": 0.8,
                  }

CHAR_ARRAYS = {"default": {"prio": [40, 2, 1, 5, 2, 2, 1, 2], # prio
                           0: [3, 2, 1, 1, 0, 0, -1, -2], # 0 IC/GC
                           1: [3, 2, 2, 1, 1, 0, -1, -2], # +1 IC/GC
                           2: [3, 2, 2, 1, 1, 0, -1, -1], # +2 IC/GC
                           },
               "even": {"prio": [40, 2, 1, 5, 2, 2, 1, 2], # prio
                        0: [3, 1, 1, 1, 0, 0, -1, -1], # 0 IC/GC
                        1: [3, 1, 1, 1, 1, 0, 0, 0], # +1 IC/GC
                        2: [3, 2, 1, 1, 1, 1, 0, 0], # +2 IC/GC
                        },
               "uneven": {"prio": [20, 2, 1, 5, 2, 2, 1, 2], # prio
                          0: [3, 2, 2, 0, 0, -1, -1, -2], # 0 IC/GC
                          1: [4, 2, 2, 0, 0, -1, -1, -2], # +1 IC/GC
                          2: [4, 3, 2, 0, 0, -1, -1, -2], # +2 IC/GC
                          },
               "extreme": {"prio": [20, 2, 1, 5, 2, 2, 1, 2], # prio
                           0: [3, 3, 2, 0, 0, -1, -1, -3], # 0 IC/GC
                           1: [4, 3, 2, 0, 0, -1, -1, -3], # +1 IC/GC
                           2: [5, 3, 2, 0, 0, -1, -1, -3], # +2 IC/GC
                           }
               }

CHAR_ARRAYS_PRIO = {"default": 2,
                  "even": 0.6,
                  "uneven": 1,
                  "extreme": 0.8,
                  }

IC_PRIO = {0: 1,
           1: 3,
           2: 0.5,
           }

# Softcapped stats are mostly languages that you seldom what above 5
# keys are names of softcapped abilities, value is at what skill value cap starts
# most languages are listed as generic, we need to make sure that the effect
# remains when they are replaced with real names
SOFTCAPPED_STATS = {"Latin": 5,
                    "Classic Greek": 5,
                    "Arabic": 5,
                    "Native Language": 5,
                    "Foreign Language 1": 5,
                    "Foreign Language 2": 5,
                    "(Dead Language)": 5,
                    }

MAGE_REQUIRED_STATS = {"Native Language": 5,
                       "Latin": 4,
                       "Magic Theory": 3,
                       "Artes Liberales": 1,
                       "Parma Magica": 1,
                       }

# order skill in tyoe sections and alphabetically within them
# make a copy of this in the setting where we also add specified and
# custom skills, like specific languages, lores and so
# first skills will be most visible, order important and common first (after arts)
ORD_CORE_MAGIC = ["Concentration",
                  "Finesse",
                  "Magic Theory",
                  "Parma Magica",
                  "Penetration",]

ORD_CORE_ACA = ["Artes Liberales",
                "Philosophiae",
                "Teaching",]

ORD_SOCIAL = ["Bargain",
              "Carouse",
              "Charm",
              "Etiquette",
              "Folk Ken",
              "Guile",
              "Intrigue",
              "Leadership",]

ORD_ADVENTURE = ["Animal Handling",
                 "Athletics",
                 "Awareness",
                 "Hunt",
                 "Legerdemain",
                 "Ride",
                 "Stealth",
                 "Survival",
                 "Swim",
                 ]

ORD_MARTIAL = ["Brawl",
               "Bows",
               "Great Weapon",
               "Single Weapon",
               "Thrown Weapon",]

ORD_LANG = ["(Dead Language)",
            "Arabic",
            "Classic Greek",
            "Foreign Language 1",
            "Foreign Language 2",
            "Latin",
            "Native Language",
            ]

ORD_MED = ["Chirurgy",
           "Medicine",]

ORD_ART_N_CRAFT = ["Craft 1",
                   "Craft 2",
                   "Craft 3",
                   "Music",]

ORD_LAW_N_REL = ["Civil and Canon Law",
                 "Code of Hermes",
                 "Common Law",
                 "Islamic Law",
                 'Orthodox Church Lore',
                 'Sunni Lore',
                 "Theology",]

ORD_MAGIC_LORES = ["Dominion Lore",
                   "Faerie Lore",
                   "Infernal Lore",
                   "Magic Lore",]

ORD_AREA_LORES = ["Area Lore 1",
                  "Area Lore 2",
                  "Area Lore 3",]

ORD_ORG_LORES = ["Covenant Lore",
                 "Church Lore",
                 "Guild Lore",
                 "House Lore",
                 "Order of Hermes Lore",
                 "(Organization) Lore 1",
                 "(Organization) Lore 2",]

ORD_PROF = ["Profession (Type)",
            "Profession Scribe",
            "Profession Sailor",]

ORD_SUPER = SUPABILITIES

DEFAULT_ABIL_ORDERING = {"Core Magic": ORD_CORE_MAGIC,
                         "Core Academic": ORD_CORE_ACA,
                         "Social": ORD_SOCIAL,
                         "Adventure": ORD_ADVENTURE,
                         "Martial": ORD_MARTIAL,
                         "Languages": ORD_LANG,
                         "Medicine": ORD_MED,
                         "Arts and Crafting": ORD_ART_N_CRAFT,
                         "Law and Religion": ORD_LAW_N_REL,
                         "Magic Lores": ORD_MAGIC_LORES,
                         "Area Lores": ORD_AREA_LORES,
                         "Org. Lores": ORD_ORG_LORES,
                         "Professions": ORD_PROF,
                         "Supernatural": ORD_SUPER,
                         "Other": {},
                         }

# just used to verify coherence in lists
if __name__ == '__main__':
    import copy
    all_default_abiltites = copy.deepcopy(GENABILITIES + ACAABILITIES + ARCABILITIES + MARABILITIES +SUPABILITIES)

    abilities_in_ordering = []
    for _, area in DEFAULT_ABIL_ORDERING.items():
        for abil in area:
            if abil in abilities_in_ordering:
                print(f"{abil} is added twice to ordering!")
            else:
                abilities_in_ordering.append(abil)

    abilities_in_skill_areas = []
    for _, tup in SKILL_AREAS.items():
        area = tup[0]
        for abil in area:
            if abil not in abilities_in_skill_areas:
                abilities_in_skill_areas.append(abil)
    for _, val in GREEK_SHIFT.items():
        for tup in val:
            abil = tup[0]
            if abil not in abilities_in_skill_areas:
                    abilities_in_skill_areas.append(abil)
    for _, val in ARABIC_SHIFT.items():
        for tup in val:
            abil = tup[0]
            if abil not in abilities_in_skill_areas:
                    abilities_in_skill_areas.append(abil)
    for _, val in ENGLISH_SHIFT.items():
        for tup in val:
            abil = tup[0]
            if abil not in abilities_in_skill_areas:
                    abilities_in_skill_areas.append(abil)

    diff_def_v_order = list(set(all_default_abiltites).difference(abilities_in_ordering))
    diff_order_v_def = list(set(abilities_in_ordering).difference(all_default_abiltites))
    if diff_def_v_order:
        print(f"{diff_def_v_order} are in default abilities but not ordering")
    if diff_order_v_def:
        print(f"{diff_order_v_def} are in ordering but not default abilities")

    diff_area_v_order = list(set(abilities_in_skill_areas).difference(abilities_in_ordering))
    diff_order_v_area = list(set(abilities_in_ordering).difference(abilities_in_skill_areas))
    if diff_area_v_order:
        print(f"{diff_area_v_order} are in skill areas but not ordering")
    if diff_order_v_area:
        print(f"{diff_order_v_area} are in ordering but not skill areas")

    # these tests currently expects the following output:
    # ['Sunni Lore', 'Church Lore', 'Profession Scribe', 'Profession Sailor',
    # 'Orthodox Church Lore', 'Guild Lore', 'House Lore', 'Covenant Lore']
    # are in ordering but not default abilities
