import numpy as np
import pickle
import os

from character import Character, Ability, Art
import char_generator

class Setting:

    def __init__(self,
                 name: str,
                 save_name: str,
                 ) -> None:
        self.name = name
        self.save_name = save_name
        self.characters = {} # contains all setting characters
        # TODO add searchable ways to keep track of which groups (coventant
        # house, tribunal, mystery, etc) characters belong too. Bidirectional
        # tracking or just use search?

    def add_character(self,
                      char: Character,
                      replace: bool = False,
                      ) -> bool:
        if char in self.characters and not replace:
            print("A character with this name already exists. "
                  "Set replace to True if you want to overwrite.")
            return False
        self.characters[char.name] = char

    def get_character(self,
                      name: str,
                      ) -> Character:
        if name in self.characters:
            return self.characters[name]
        else:
            return None

def save_setting(setting: Setting,
                 replace: bool = False,
                 ) -> bool:
    try:
        path = os.path.join("./user_data/", setting.save_name)
        if os.path.isfile(path) and not replace:
            raise Exception("Setting already exists. Set replace to "
                            "True if you want to overwrite.")
        with open(path, "wb") as f:
            pickle.dump(setting, f)
            return True
    except Exception as ex:
        print("Error during pickling object:", ex)

def load_setting(filename: str) -> Setting:
    try:
        with open(os.path.join("./user_data/", filename), "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object:", ex)

def example_use():
    rng = np.random.default_rng()
    curr_sett = Setting("Testing in Tunis",
                      "testing_in_tunis.ars_setting")
    examplo = char_generator.gen_from_stats_array("Mage",
                                   "Examplo de Magicus",
                                   rel_prio_weight=0.5,
                                   budget=35,
                                   )
    curr_sett.add_character(examplo)
    save_setting(curr_sett)
    curr_sett = load_setting("testing_in_tunis.ars_setting")
    examplo2 = curr_sett.get_character("Examplo de Magicus")
    print(examplo2)

if __name__ == "__main__":
    example_use()