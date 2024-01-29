import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
import json
from typing import List
from character import Character, Ability, Art
from character import dict2string as d2s
import char_generator as cg
from functools import partial
import copy
import lists_and_data
import csv

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
                 rng = None,
                 current_year: int = 1220,
                 ) -> None:
        self.version = 0.1 # used to track how json save looks like and handle updates
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
        self.current_year = current_year
        self.ability_ordering = copy.deepcopy(lists_and_data.DEFAULT_ABIL_ORDERING)
        if rng is None:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng
        for _, char in self.characters.items():
            char.rng = self.rng

    def __json__(self):
        # Customize serialization for the Character class
        return {
            "version": self.version,
            "name": self.name,
            "save_name": self.save_name,
            "characters": self.characters,
            "groups": self.groups,
            "rng": self.rng.bit_generator.state,
            "current_year": self.current_year
        }

    @classmethod
    def from_json(cls, serialized_data):
        # if needed use serialized_data["version"] to do recovery behaviour
        chars = {}
        for _, char in serialized_data["characters"].items():
            chars[char["name"]] = Character.from_json(char)
        rng = np.random.default_rng()
        rng.bit_generator.state = serialized_data["rng"]
        return cls(
            name=serialized_data["name"],
            save_name=serialized_data["save_name"],
            characters=chars,
            groups=serialized_data["groups"],
            rng=rng,
            current_year=serialized_data["current_year"]
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

    def add_years(self, years: int):
        self.current_year += years
        for char in self.characters.values():
            char.set_to_year(self.current_year)

    def set_year(self, year: int):
        self.current_year = year
        for char in self.characters.values():
            char.set_to_year(year)

    def characters2csv_headers(self) -> list:
        headers = [str(self.current_year), "Age"]
        headers += lists_and_data.CHARACTERISTICS
        headers += lists_and_data.TECHNIQUES
        headers += lists_and_data.FORMS
        for _, area in self.ability_ordering.items():
            headers += area
        headers += list(self.groups.keys())
        return headers

class SortableTable(ttk.Treeview):
    def __init__(self, parent, columns, characters, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, columns=columns, *args, **kwargs)
        # self.heading("#0", text="Index")
        for col in columns:
            self.heading(col, text=col, command=lambda c=col: self.sortby(c, 0))
            self.column(col, width=100, anchor="center", stretch=True)
        self.format_and_populate(characters)

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

    def format_and_populate(self, characters: dict):
        data = []
        for char in characters.values():
            entry, _ = char.name2charfield(self["columns"])
            data.append(entry)
        self.populate_table(data)

class CharInfoFrame(tk.Frame):
    def __init__(self, master, manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.manager = manager
        # Labels to display the generated stats
        self.characteristics_var = tk.StringVar()
        self.characteristics_label = ttk.Label(self,
                                            textvariable=self.characteristics_var,
                                            justify=tk.LEFT,
                                            style='Monospaced.TLabel',)

        self.abilities1_var = tk.StringVar()
        self.abilities1_label = ttk.Label(self,
                                    textvariable=self.abilities1_var,
                                    wraplength=400,
                                    justify=tk.LEFT,
                                    style='Monospaced.TLabel',)
        self.abilities2_var = tk.StringVar()
        self.abilities2_label = ttk.Label(self,
                                    textvariable=self.abilities2_var,
                                    wraplength=400,
                                    justify=tk.LEFT,
                                    style='Monospaced.TLabel',)
        self.abilities3_var = tk.StringVar()
        self.abilities3_label = ttk.Label(self,
                                    textvariable=self.abilities3_var,
                                    wraplength=400,
                                    justify=tk.LEFT,
                                    style='Monospaced.TLabel',)

        self.techniques_var = tk.StringVar()
        self.techniques_label = ttk.Label(self,
                                    textvariable=self.techniques_var,
                                    justify=tk.LEFT,
                                    style='Monospaced.TLabel',)

        self.forms_var = tk.StringVar()
        self.forms_label = ttk.Label(self,
                                textvariable=self.forms_var,
                                justify=tk.LEFT,
                                style='Monospaced.TLabel',)

        self.grid_rowconfigure(1, minsize=550)
        self.characteristics_label.grid(column=0,
                                    row=0,
                                    sticky="nw",
                                    columnspan=3,
                                    padx=10,
                                    pady=10,)
        self.abilities1_label.grid(column=0,
                                row=1,
                                sticky="nw",
                                padx=10,
                                pady=10,)
        self.abilities2_label.grid(column=1,
                                row=1,
                                sticky="nw",
                                padx=10,
                                pady=10,)
        self.abilities3_label.grid(column=2,
                                row=1,
                                sticky="nw",
                                padx=10,
                                pady=10,)
        self.techniques_label.grid(column=0,
                                row=2,
                                sticky="nw",
                                columnspan=3,
                                padx=10,
                                pady=10,)
        self.forms_label.grid(column=0,
                            row=3,
                            sticky="nw",
                            columnspan=3,
                            padx=10)

    def update_all(self, values):
        # Update the displayed values for characteristics, abilities, etc.
        self.characteristics_var.set(f"--Characteristics--\n"
                                f"{d2s(values['characteristics'],sort=False)}")
        self.techniques_var.set(f"--Techniques--\n{d2s(values['techniques'])}")
        self.forms_var.set(f"--Forms--\n{d2s(values['forms'])}")
        self.update_ability_display(values)
        # lcharacteristics_var.set(f"--Characteristics--\n{d2s(ccvals['new_char'].characteristics,sort=False)}")
        # ltechniques_var.set(f"--Techniques--\n{d2s(tech)}")
        # lforms_var.set(f"--Forms--\n{d2s(form)}")

    def update_ability_display(self, values):
        def compose_ability_part(areas: list, abil_vis) -> str:
            part = ""
            for area in areas:
                part = add_if_any_val(part, abil_vis, area)
            return part

        def add_if_any_val(part: str,
                        abil_vis: dict,
                        key: str) -> str:
            if len(abil_vis[key]["Dict list"]) > 0:
                part += f"-{key}-\n"
                part += f'{abil_vis[key]["String"]}\n'
            return part

        abil_vis = cg.abil_order_split(values["abilities"],
                                        self.manager.setting.ability_ordering)
        part1 = compose_ability_part(["Core Magic",
                                        "Core Academic",
                                        "Social",
                                        "Martial"],
                                        abil_vis)
        self.abilities1_var.set(f"--Abilities--\n{part1}")
        part2 = compose_ability_part(["Adventure",
                                        "Languages",
                                        "Medicine",
                                        "Arts and Crafting"],
                                        abil_vis)
        self.abilities2_var.set(part2)
        part3 = compose_ability_part(["Magic Lores",
                                        "Area Lores",
                                        "Org. Lores",
                                        "Professions",
                                        "Law and Religion",
                                        "Supernatural"],
                                        abil_vis)
        self.abilities3_var.set(part3)

class ArsManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x500')
        self.root.title("Ars Manager")
        self.setting = None # load of create setting before anything else

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.create_file_menu()
        self.create_setting_menu()
        self.enable_setting_menus(initiated=False)
        self.create_table()

    def create_setting_menu(self):
        setting_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Setting",
                                 menu=setting_menu,
                                 underline=0)
        setting_menu.bind("<Alt-s>", lambda e:setting_menu.invoke(0))
        setting_menu.add_command(label="Set Year",
                                 command=self.set_year_popup,
                                 underline=0)
        setting_menu.bind("<Alt-s>", lambda e:self.set_year_popup)
        setting_menu.add_command(label="Add Years",
                                 command=self.add_years_popup,
                                 underline=0)
        setting_menu.bind("<Alt-a>", lambda e:self.add_years_popup)

    def create_file_menu(self):
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu, underline=0)
        self.file_menu = file_menu
        file_menu.bind("<Alt-f>", lambda e:file_menu.invoke(0))
        file_menu.add_command(label="New Setting",
                              command=self.new_setting,
                              underline=0)
        file_menu.bind("<Alt-n>", lambda e:self.new_setting)
        file_menu.add_command(label="Save Setting",
                              command=self.ask_save_setting,
                               underline=0)
        file_menu.bind("<Alt-s>", lambda e:self.ask_save_setting)
        file_menu.add_command(label="Export Characters",
                              command=self.export_characters,
                               underline=0)
        file_menu.bind("<Alt-e>", lambda e:self.export_characters)
        file_menu.add_command(label="Load Setting",
                              command=self.load_setting,
                               underline=0)
        file_menu.bind("<Alt-l>", lambda e:self.load_setting)
        file_menu.add_command(label="New Character",
                              command=self.create_character_popup,
                               underline=4)
        file_menu.bind("<Alt-c>", lambda e:self.create_character_popup)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def enable_setting_menus(self, initiated: bool=True):
        if initiated:
            state=tk.NORMAL
        else:
            state=tk.DISABLED
        file_menu = self.file_menu
        file_menu.entryconfigure("Save Setting", state=state)
        file_menu.entryconfigure("Export Characters", state=state)
        file_menu.entryconfigure("New Character", state=state)
        self.menubar.entryconfigure("Setting", state=state)

    def create_table(self):
        columns = ("Name",
                   "Age",
                   "House",
                   "Covenant",
                   "Tribunal",
                   "Techniques",
                   "Forms",
                   "Characteristics",
                   "Abilities"
                   )
        self.tree = SortableTable(self.root, columns, {}, show="headings")

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
        popup.geometry('250x150')
        popup.title("New Setting")

        # Label and Entry for the user to input the setting name
        label = ttk.Label(popup, text="Enter Setting Name:")
        label.pack(pady=10)

        entry = ttk.Entry(popup)
        entry.pack(pady=10)
        entry.focus()

        # Callback function to handle the "Save Setting" button
        def set_save_location(event = None):
            # Get the input setting name
            setting_name = entry.get()

            if setting_name:
                # Get save location
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json")]
                )

                # default groups
                groups = {"Covenant": {},
                          "House": {"Bjornaer": None,
                                    "Bonisagus": None,
                                    "Criamon": None,
                                    "Ex Miscellanea": None,
                                    "Flambeau": None,
                                    "Guernicus": None,
                                    "Jerbiton": None,
                                    "Mercere": None,
                                    "Merinita": None,
                                    "Tremere": None,
                                    "Tytalus": None,
                                    "Verditius": None,},
                          "Tribunal": {"Greater Alps": None,
                                       "Hibernia": None,
                                       "Iberia": None,
                                       "Levant": None,
                                       "Loch Leglean": None,
                                       "Normandy": None,
                                       "Novgorod": None,
                                       "Provence": None,
                                       "Rhine": None,
                                       "Rome": None,
                                       "Stonehenge": None,
                                       "Thebe": None,
                                       "Transylvania": None,}}

                # Create a new Setting instance
                new_setting = Setting(name=setting_name,
                                      save_name=file_path,
                                      groups=groups)

                # Update the current setting
                self.setting = new_setting
                self.save_setting()

                # Close the popup
                popup.destroy()

                # Update the table with the new setting
                self.update_table()

                # open up options
                self.enable_setting_menus()

        # Save Setting button
        save_button = ttk.Button(popup,
                                 text="Select save location",
                                 command=set_save_location)
        save_button.pack(pady=10, padx=10)
        popup.bind('<Return>', set_save_location)

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
                self.enable_setting_menus()

    def update_table(self):
        # Clear the existing items in the table
        self.tree.delete(*self.tree.get_children())

        # Populate the table with character data
        self.tree.format_and_populate(self.setting.characters)

    def export_characters(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Export location")
        if file_path:
            with open(file_path, "w", newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                headers = self.setting.characters2csv_headers()
                csvwriter.writerow(headers)
                # first field should be name, we just hijacked it for current year
                headers[0] = "Name"
                dictwriter = csv.DictWriter(csvfile, fieldnames=headers)
                chars = dict(sorted(self.setting.characters.items()))
                for char in chars.values():
                    dictwriter.writerow(char.to_dict())

    def set_year_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Set year")

        earliest = -np.inf
        for char in self.setting.characters.values():
            if char.char_input_year > earliest:
                earliest = char.char_input_year

        label_text = f"Current year is {self.setting.current_year}.\n"
        label_text += f"The earliest year you can select is {earliest}.\n"
        label_text += "What year do you want to set it to?"
        year_label = tk.Label(popup,
                              text=label_text)
        year_label.grid(column=0, row=0, sticky=tk.NW, padx=10, pady=10)

        set_years_entry = tk.Entry(popup, width=20)
        set_years_entry.grid(column=1,
                             row=0,
                             sticky=tk.NW,
                             padx=10,
                             pady=10)
        set_years_entry.focus()

        def set_year(year: str):
            year = int(year)
            if year < earliest:
                return
            self.setting.set_year(year)
            self.update_table()
            self.save_setting()
            popup.destroy()

        add_b = ttk.Button(popup,text="Set year",
                           command=lambda:
                           set_year(set_years_entry.get()))
        add_b.grid(column=0, row=1, padx=10, pady=10, sticky=tk.NW, columnspan=2)
        popup.bind('<Return>', lambda e:set_year(set_years_entry.get()))

    def add_years_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add years")

        label_text = f"Current year is {self.setting.current_year}.\n"
        label_text += "How many years to you want to add?"
        year_label = tk.Label(popup,
                              text=label_text)
        year_label.grid(column=0, row=0, sticky=tk.NW, padx=10, pady=10)

        add_years_entry = tk.Entry(popup, width=20)
        add_years_entry.grid(column=1,
                             row=0,
                             sticky=tk.NW,
                             padx=10,
                             pady=10)
        add_years_entry.focus()

        def add_years(years: str):
            years = int(years)
            if years < 1:
                return
            self.setting.add_years(years)
            self.update_table()
            self.save_setting()
            popup.destroy()

        add_b = ttk.Button(popup,text="Add years",
                           command=lambda:
                           add_years(add_years_entry.get()))
        add_b.grid(column=0, row=1, padx=10, pady=10, sticky=tk.NW, columnspan=2)
        popup.bind('<Return>', lambda e:add_years(add_years_entry.get()))

        # Run the Tkinter main loop for the popup window
        popup.mainloop()

    def create_character_popup(self):
        ccvals = {}
        ccvals["values"] = cg.gen_mage_values()
        age_entry_var = tk.IntVar(value=25)
        ccvals["age_var"] = age_entry_var
        def gen_and_age_char(name: str = "temp_to_be_replaced",):
            values = ccvals["values"]
            age = age_entry_var.get()
            if age < 25:
                tk.messagebox.showwarning("Warning",
                                          "Character cannot be younger than gauntlet age at 25!")
                return  # Don't proceed further if the name is empty
            gauntlet_year = self.setting.current_year - age + 25
            char =  cg.create_mage_from_gen_vals(name,
                                                 values,
                                                 char_input_year=gauntlet_year,
                                                 current_year = self.setting.current_year,)
                                                 #rel_prio_weight=1,
                                                 #budget=30)
            ccvals["new_char"] = char

        def update_all():
            values = ccvals["values"]
            base_stats_frame.update_all(values)
            gen_and_age_char()
            abilities, arts = ccvals["new_char"].get_arts_and_abilities()
            tech, form = ccvals["new_char"].separate_tech_and_form(arts)
            aged_values = {"characteristics": ccvals['new_char'].characteristics,
                           "abilities": abilities,
                           "techniques": tech,
                           "forms": form}
            aged_stats_frame.update_all(aged_values)

        # Create a new Toplevel window (popup) for character creation
        popup = tk.Toplevel(self.root)
        popup.title("Create New Character")

        popup.grid_rowconfigure(4, minsize=570)
        #popup.grid_rowconfigure(4, weight=1)
        #popup.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Monospaced.TLabel', font='Courier 10') # Courier

        # Label and Entry for the user to input the character name
        name_label = ttk.Label(popup, text="Enter Character Name:")
        name_label.grid(column=0, row=0, sticky=tk.NW, padx=10, pady=10)

        name_entry = ttk.Entry(popup, width=30)
        name_entry.grid(column=1,
                        row=0,
                        sticky=tk.NW,
                        columnspan=3,
                        padx=10,
                        pady=10)
        name_entry.focus()

        groups_label = ttk.Label(popup, text="Which groups are the character in?")
        groups_label.grid(column=0, row=1, rowspan=2, sticky=tk.NW, padx=10, pady=10)

        house_label = ttk.Label(popup, text="House")
        house_label.grid(column=1, row=1, sticky=tk.NW, padx=10)
        covenant_label = ttk.Label(popup, text="Covenant")
        covenant_label.grid(column=2, row=1, sticky=tk.NW, padx=10)
        tribunal_label = ttk.Label(popup, text="Tribunal")
        tribunal_label.grid(column=3, row=1, sticky=tk.NW, padx=10)

        house = tk.StringVar()
        house_box = ttk.Combobox(popup, width = 27, textvariable = house)
        house_box['values'] = list(sorted(self.setting.groups["House"]))
        house_box.grid(column=1, row=2, sticky=tk.NW, padx=10)
        covenant = tk.StringVar()
        covenant_box = ttk.Combobox(popup, width = 27, textvariable = covenant)
        covenant_box['values'] = list(sorted(self.setting.groups["Covenant"]))
        covenant_box.grid(column=2, row=2, sticky=tk.NW, padx=10)
        tribunal = tk.StringVar()
        tribunal_box = ttk.Combobox(popup, width = 27, textvariable = tribunal)
        tribunal_box['values'] = list(sorted(self.setting.groups["Tribunal"]))
        tribunal_box.grid(column=3, row=2, sticky=tk.NW, padx=10)

        base_stats_frame = CharInfoFrame(popup, self)
        base_stats_frame.grid(column=1, row=3, columnspan=3, rowspan=4, sticky=tk.NW,)

        # display char after leveling
        vseparator = ttk.Separator(popup, orient="vertical")
        vseparator.grid(column=4, row=0, rowspan=7, sticky='ns')

        older_label = ttk.Label(popup, text="Here are the stats the character"
                                            "will have at the current year")
        older_label.grid(column=5, row=0, rowspan=3, sticky=tk.NW, padx=10, pady=10)

        age_txt = f"Current setting year is {self.setting.current_year}.\n"
        age_txt += f"How old should the character be this year?\n"
        age_txt += f"Minimum age is 25, when they pass their gauntlet."
        age_label = ttk.Label(popup, text=age_txt)
        age_label.grid(column=5, row=2, sticky=tk.NW, padx=10, pady=10)

        age_entry = ttk.Entry(popup, width=30, text=age_entry_var)
        age_entry.grid(column=6,
                        row=2,
                        sticky=tk.W,
                        columnspan=3,
                        padx=10,
                        pady=10)
        age_entry_b = ttk.Button(popup,
                                 text="Set Current Age and (Re)run Aging",
                                 command=lambda:update_all(),
                                 underline=13)
        age_entry_b.grid(column=7, row=2, padx=10, pady=10)
        popup.bind('<Alt-g>', lambda e:update_all())

        aged_stats_frame = CharInfoFrame(popup, self)
        aged_stats_frame.grid(column=5, row=3, columnspan=3, rowspan=4, sticky=tk.NW,)

        # Update the displayed values for characteristics, abilities, etc.
        update_all()

        # Function to generate random character stats
        def generate_random_stats():
            values = ccvals["values"]
            # Customize based on your stat generation function
            values['characteristics'] = cg.get_characteristics_from_array()
            values['abilities'], values['ab_prios'], values['area_prios'] = cg.get_abilities_from_array()
            values['techniques'], values['te_prios'] = cg.get_techniques_from_array()
            values['forms'], values['fo_prios'] = cg.get_forms_from_array()
            update_all()

        def gen_characteristics():
            values = ccvals["values"]
            values['characteristics'] = cg.get_characteristics_from_array()
            update_all()

        def gen_abilities():
            values = ccvals["values"]
            values['abilities'], values['ab_prios'], values['area_prios'] = cg.get_abilities_from_array()
            update_all()

        def gen_techniques():
            values = ccvals["values"]
            values['techniques'], values['te_prios'] = cg.get_techniques_from_array()
            update_all()

        def gen_forms():
            values = ccvals["values"]
            values['forms'], values['fo_prios'] = cg.get_forms_from_array()
            update_all()

        # Buttons to regenerate each section
        gen_characteristics_b = ttk.Button(popup,
                                           text="Re-roll Characteristics",
                                           command=gen_characteristics,
                                           underline=8)
        gen_characteristics_b.grid(column=0, row=3, padx=10, pady=10)
        popup.bind('<Alt-c>', lambda e:gen_characteristics)

        gen_abilities_b = ttk.Button(popup,
                                     text="Re-roll Abilities",
                                     command=gen_abilities,
                                     underline=8)
        gen_abilities_b.grid(column=0, row=4, padx=10, pady=10)
        popup.bind('<Alt-a>', lambda e:gen_abilities)

        gen_techniques_b = ttk.Button(popup,
                                      text="Re-roll Techniques",
                                      command=gen_techniques,
                                      underline=8)
        gen_techniques_b.grid(column=0, row=5, padx=10, pady=10)
        popup.bind('<Alt-t>', lambda e:gen_techniques)

        gen_forms_b = ttk.Button(popup,
                                 text="Re-roll Forms",
                                 command=gen_forms,
                                 underline=8)
        gen_forms_b.grid(column=0, row=6, padx=10, pady=10)
        popup.bind('<Alt-f>', lambda e:gen_forms)

        def save_and_close_popup(self, name):
            if not name or name in self.setting.characters:
                tk.messagebox.showwarning("Warning",
                                          "Please enter a unique character name.")
                return  # Don't proceed further if the name is empty
            if age_entry_var.get() != ccvals["new_char"].current_age:
                update_all()
            groups = {"House": house.get(),
                      "Covenant": covenant.get(),
                      "Tribunal": tribunal.get()}
            # add groups to setting if not already there
            for category, group in groups.items():
                if category not in self.setting.groups:
                    self.setting.groups[category] = {group: None}
                if group not in self.setting.groups[category]:
                    self.setting.groups[category][group] = None
            ccvals["new_char"].name = name
            ccvals["new_char"].groups = groups
            self.setting.add_character(ccvals["new_char"])
            self.update_table()
            # we autosave after each character has been created
            self.save_setting()
                # Close the popup
            popup.destroy()

        # Button to generate random character stats
        generate_button = ttk.Button(popup, text="Re-roll all Stats",
                                     command=generate_random_stats,
                                     underline=0)
        generate_button.grid(column=2, row=7, padx=10, pady=10)
        popup.bind('<Alt-r>', lambda e:generate_random_stats())

        # Save Character button
        save_button = ttk.Button(popup,
                                 text="Save Character",
                                 command=lambda:
                                 save_and_close_popup(self, name_entry.get()),
                                 underline=0)
        save_button.grid(column=4, row=7, padx=10, pady=10)
        popup.bind('<Alt-s>', lambda e:save_and_close_popup(self,
                                                               name_entry.get()))

        # Run the Tkinter main loop for the popup window
        popup.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ArsManager(root)
    root.mainloop()