import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
import json
from typing import List
from character import Character, Ability, Art
import char_generator as ch

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
        self.heading("#0", text="Index")
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
            self.insert("", "end", values=(i,) + tuple(item))

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
        file_menu.add_command(label="Save Setting", command=self.save_setting)
        file_menu.add_command(label="Load Setting", command=self.load_setting)
        file_menu.add_command(label="New Character", command=self.new_character)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def create_table(self):
        columns = ("Name", "Age", "Stats", "Characteristics")
        self.tree = SortableTable(self.root, columns, [], show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill="both")

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

                if file_path:
                    with open(file_path, 'w') as file:
                        # Serialize the setting using the __json__ method
                        serialized_setting = self.setting.__json__()
                        json.dump(serialized_setting, file, indent=2)

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

    def new_character(self):
        # Assuming you have a function to create a new character instance
        new_char = self.create_new_character()
        self.setting.add_character(new_char)
        self.update_table()

    def save_setting(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, 'w') as file:
                # Serialize the setting using the __json__ method
                serialized_setting = self.setting.__json__()
                json.dump(serialized_setting, file, indent=2)

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

    # TODO replace with real method/window
    def create_new_character(self):
        values = ch.gen_mage_values()
        return ch.create_mage_from_generated_values("Examplo de Magicus",
                                                    values,
                                                    rel_prio_weight=0.5,
                                                    budget=35)

if __name__ == "__main__":
    root = tk.Tk()
    app = ArsManager(root)
    root.mainloop()