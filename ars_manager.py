import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
import json
from typing import List
from character import Character, Ability, Art
from character import dict2string as d2s
import char_generator as ch
from functools import partial

def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)
wrapped_default.default = json.JSONEncoder().default

# apply the patch
json.JSONEncoder.original_default = json.JSONEncoder.default
json.JSONEncoder.default = wrapped_default

class Setting:

    def __init__(self,
                 name: str,
                 save_name: str,
                 characters: dict = {},
                 groups: dict = {},
                 rng_state = None,
                 ) -> None:
        self.name = name
        self.save_name = save_name
        self.characters = characters # contains all setting characters
        # groups: Keys are group categories, like covenant or house, values
        # are possibly dicts themselves with a name as key for each group in
        # the category and other info about the group in that dict
        # for now we track group membership on the characters, but we should
        # make sure that all groups on characters exist here (or that we only
        # add a group to a character from this dict of options)
        self.groups = groups
        self.rng = np.random.default_rng()
        if rng_state:
            self.rng.bit_generator.state = rng_state
            for _, char in self.characters.items():
                char.rng = self.rng

    def __json__(self):
        # Customize serialization for the Character class
        return {
            "name": self.name,
            "save_name": self.save_name,
            "characters": self.characters,
            "groups": self.groups,
            "rng": self.rng.bit_generator.state,
        }

    @classmethod
    def from_json(cls, serialized_data):
        # Customize deserialization for the Setting class
        chars = {}
        for _, char in serialized_data["characters"].items():
            chars[char["name"]] = ch.Character.from_json(char)
        return cls(
            name=serialized_data["name"],
            save_name=serialized_data["save_name"],
            characters=chars,
            groups=serialized_data["groups"],
            rng_state=serialized_data["rng"],
        )

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

class SortableTable(ttk.Treeview):
    def __init__(self, parent, columns, data, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, columns=columns, *args, **kwargs)
        # self.heading("#0", text="Index")
        for col in columns:
            self.heading(col, text=col, command=lambda c=col: self.sortby(c, 0))
            self.column(col, width=100, anchor="center", stretch=True)
        self.populate_table(data)

    def sortby(self, col, descending):
        data = [(self.set(child, col), child) for child in self.get_children('')]
        data.sort(reverse=descending)
        for i, item in enumerate(data):
            self.move(item[1], '', i)
        self.heading(col, command=lambda: self.sortby(col, int(not descending)))

    def populate_table(self, data):
        self.data = data
        for i, item in enumerate(self.data):
            self.insert("", "end", values=tuple(item))

class ArsManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Ars Manager")
        self.setting = Setting(name="Default Setting",
                               save_name="default_setting")

        self.create_menu()
        self.create_table()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Setting", command=self.new_setting)
        file_menu.add_command(label="Save Setting", command=self.ask_save_setting)
        file_menu.add_command(label="Load Setting", command=self.load_setting)
        file_menu.add_command(label="New Character", command=self.create_character_popup)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def create_table(self):
        columns = ("Name", "Age", "Stats", "Characteristics")
        self.tree = SortableTable(self.root, columns, [], show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill="both")

    def save_setting(self):
        if self.setting.save_name:
                    with open(self.setting.save_name, 'w') as file:
                        # Serialize the setting using the __json__ method
                        serialized_setting = self.setting.__json__()
                        json.dump(serialized_setting, file, indent=2)

    def new_setting(self):
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.title("New Setting")

        # Label and Entry for the user to input the setting name
        label = ttk.Label(popup, text="Enter Setting Name:")
        label.pack(pady=10)

        entry = ttk.Entry(popup)
        entry.pack(pady=10)

        # Callback function to handle the "Save Setting" button
        def set_save_location():
            # Get the input setting name
            setting_name = entry.get()

            if setting_name:
                # Get save location
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json")]
                )

                # Create a new Setting instance
                new_setting = Setting(name=setting_name, save_name=file_path)

                # Update the current setting
                self.setting = new_setting

                self.save_setting()

                # Close the popup
                popup.destroy()

                # Update the table with the new setting
                self.update_table()

        # Save Setting button
        save_button = ttk.Button(popup,
                                 text="Select save location",
                                 command=set_save_location)
        save_button.pack(pady=10, padx=10)

        # Run the Tkinter main loop for the popup window
        popup.mainloop()

    def ask_save_setting(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        self.setting.save_name = file_path

        self.save_setting()

    def load_setting(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, 'r') as file:
                # Deserialize the setting using the custom from_json method
                serialized_setting = json.load(file)
                self.setting = Setting.from_json(serialized_setting)
                self.update_table()

    def update_table(self):
        # Clear the existing items in the table
        self.tree.delete(*self.tree.get_children())

        # Populate the table with character data
        data = [
            (char.name, char.current_age, char.stats, char.characteristics)
            for char in self.setting.characters.values()
        ]
        self.tree.populate_table(data)

    def create_new_character(self,
                             name,
                             values,
                             ):
        new_char =  ch.create_mage_from_generated_values(name,
                                                    values,
                                                    rel_prio_weight=0.5,
                                                    budget=35)
        self.setting.add_character(new_char)
        self.update_table()
        # we autosave after each character has been created
        self.save_setting()

    def create_character_popup(self):
        # Create a new Toplevel window (popup) for character creation
        popup = tk.Toplevel(self.root)
        popup.title("Create New Character")

        # Label and Entry for the user to input the character name
        name_label = tk.Label(popup, text="Enter Character Name:")
        name_label.grid(column=0, row=0, sticky=tk.NW,)

        name_entry = tk.Entry(popup, width=50)
        name_entry.grid(column=1, row=0, sticky=tk.NW,)

        # Dropdown menu for character type
        # type_label = tk.Label(popup, text="Select Character Type:")
        # type_label.pack(pady=10)

        # type_options = ["Mage", "Companion", "Grog"]  # Customize based on your character types
        # type_var = tk.StringVar(value=type_options[0])

        # type_menu = tk.OptionMenu(popup, type_var, *type_options)
        # type_menu.pack(pady=10)

        # Labels to display the generated stats
        characteristics_label = tk.Label(popup,
                                         text="Characteristics:",
                                         justify=tk.LEFT)
        characteristics_label.grid(column=1, row=1, sticky=tk.NW,)

        abilities_label = tk.Label(popup,
                                   text="Abilities:",
                                   wraplength=400,
                                   height=14,
                                   justify=tk.LEFT)
        abilities_label.grid(column=1, row=2, sticky=tk.NW,)

        techniques_label = tk.Label(popup,
                                    text="Techniques:",
                                    justify=tk.LEFT)
        techniques_label.grid(column=1, row=3, sticky=tk.NW,)

        forms_label = tk.Label(popup,
                               text="Forms:",
                               justify=tk.LEFT)
        forms_label.grid(column=1, row=4, sticky=tk.NW,)

        values = ch.gen_mage_values()
        # Update the displayed values for characteristics, abilities, etc.
        characteristics_label.config(text=f"Characteristics:\n"
                                     f"{d2s(values['characteristics'],sort=False)}")
        abilities_label.config(text=f"Abilities:\n{d2s(values['abilities'])}")
        techniques_label.config(text=f"Techniques:\n{d2s(values['techniques'])}")
        forms_label.config(text=f"Forms:\n{d2s(values['forms'])}")

        # Function to generate random character stats
        def generate_random_stats(values):
            # Customize based on your stat generation function
            values['characteristics'] = ch.get_characteristics_from_array()
            values['abilities'], values['ab_prios'], values['area_prios'] = ch.get_abilities_from_array()
            values['techniques'], values['te_prios'] = ch.get_techniques_from_array()
            values['forms'], values['fo_prios'] = ch.get_forms_from_array()

            # Update the displayed values for characteristics, abilities, etc.
            characteristics_label.config(text=f"Characteristics:\n"
                                     f"{d2s(values['characteristics'],sort=False)}")
            abilities_label.config(text=f"Abilities:\n{d2s(values['abilities'])}")
            techniques_label.config(text=f"Techniques:\n{d2s(values['techniques'])}")
            forms_label.config(text=f"Forms:\n{d2s(values['forms'])}")

        def gen_characteristics(values):
            values['characteristics'] = ch.get_characteristics_from_array()
            characteristics_label.config(text=f"Characteristics:\n"
                                     f"{d2s(values['characteristics'],sort=False)}")

        def gen_abilities(values):
            values['abilities'], values['ab_prios'], values['area_prios'] = ch.get_abilities_from_array()
            abilities_label.config(text=f"Abilities:\n{d2s(values['abilities'])}")

        def gen_techniques(values):
            values['techniques'], values['te_prios'] = ch.get_techniques_from_array()
            techniques_label.config(text=f"Techniques:\n{d2s(values['techniques'])}")

        def gen_forms(values):
            values['forms'], values['fo_prios'] = ch.get_forms_from_array()
            forms_label.config(text=f"Forms:\n{d2s(values['forms'])}")

        # Button to generate random character stats
        generate_button = ttk.Button(popup, text="Re-roll all Stats",
                                     command=partial(generate_random_stats,
                                                     values))
        generate_button.grid(column=0, row=5)

        # Buttons to regenerate each section
        gen_characteristics_b = ttk.Button(popup,
                                           text="Re-roll Characteristics",
                                           command=partial(gen_characteristics,
                                                           values))
        gen_characteristics_b.grid(column=0, row=1)

        gen_abilities_b = ttk.Button(popup,
                                     text="Re-roll Abilities",
                                     command=partial(gen_abilities,
                                                     values))
        gen_abilities_b.grid(column=0, row=2)

        gen_techniques_b = ttk.Button(popup,
                                      text="Re-roll Techniques",
                                      command=partial(gen_techniques,
                                                      values))
        gen_techniques_b.grid(column=0, row=3)

        gen_forms_b = ttk.Button(popup,
                                 text="Re-roll Forms",
                                 command=partial(gen_forms,
                                                 values))
        gen_forms_b.grid(column=0, row=4)

        def save_and_close_popup(self, name, values):
            if not name or name in self.setting.characters:
                tk.messagebox.showwarning("Warning",
                                          "Please enter a unique character name.")
                return  # Don't proceed further if the name is empty
            self.create_new_character(name, values)
            # Close the popup
            popup.destroy()

        # Save Character button
        save_button = ttk.Button(popup,
                                 text="Save Character",
                                 command=lambda:
                                 save_and_close_popup(self, name_entry.get(),
                                                      values))
        save_button.grid(column=1, row=5)

        # Run the Tkinter main loop for the popup window
        popup.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ArsManager(root)
    root.mainloop()