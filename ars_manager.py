import numpy as np
from character import Character, Ability, Art
from collections import defaultdict
from  lists_and_data import *

# initiate default rng
rng = np.random.default_rng()

def sort_by_name_list(names, dct):
    assert len(names) == len(dct)
    assert all(name in names for name in dct.keys())
    ret = {}
    for key in names:
        ret[key] = dct[key]
    return ret

def get_template(name: str) -> tuple[list, list, list]:
    # shared stats unless overwritten, non mages don't get the arts (tech and form)
    characteristics = ["Int", "Per", "Str", "Sta", "Pre", "Com", "Dex", "Qik",]
    tech = ["Cr","In","Mu","Pe","Re",]
    form = ["An","Aq","Au","Co","He","Ig","Im","Me","Te","Vi",]
    if name == "Certamen":
        characteristics = ["Int", "Per", "Sta", "Pre", "Qik",]
        abilities = ["Finesse", "Penetration", "Parma Magica", "Concentration"]
        return characteristics, abilities, tech, form
    elif name == "Mage":
        abilities = genabilities + acaabitilites + arcabilities + marabilities
        return characteristics, abilities, tech, form
    else:
        raise Exception(f"There is no template named {name}") 

# designed for mages, at least change prio for other characters
def get_characteristics_array(balance: str = "default", ic: int = 1):
    options = {"default": {"prio": [40, 2, 1, 5, 2, 2, 1, 2], # prio
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
    names = ["Int", "Per", "Str", "Sta", "Pre", "Com", "Dex", "Qik",]
    return assign_array(names,
                        options[balance][ic],
                        options[balance]["prio"],
                        int)

def assign_array_prio_dict(dct: dict,
                           array: list,
                           tpe: type
                           ) -> dict:
    prio = []
    names = []
    for n, p in dct.items():
        names.append(n)
        prio.append(p)
    return assign_array(names, array, prio, tpe)

def assign_array(names: list,
                 array: list,
                 prio: list,
                 tpe: type,
                 ) -> dict:
    if prio == None:
        prio = [1]*len(names)
    nms = rng.choice(names, len(names), replace=False, p=np.array(prio)/sum(prio))
    return sort_by_name_list(names, {name: tpe(val) for name, val in zip(nms, array)})

# generates standard age 25, just out of gauntlet mages from mostly fixed arrays
# of stats
def gen_from_stats_array(template: str,
                         name: str,
                         char_input_year: int = 1220,
                         char_input_age: int = 25,
                         rel_prio_weight: float = 1,
                         ) -> Character:
    ch, ab, te, fo = get_template(template)
    if template == "Certamen":
        charray = [3, 2, 1, 0, -1]
        chprio = [20, 1, 1, 2, 1]
        # characteristics are set by fixed array
        characteristics = assign_array(ch, charray, chprio, int)
        # abilities are mostly fixed
        abilities = {"Parma Magica": Ability(1),
                     "Penetration": Ability(rng.choice([0, 1, 2],
                                                       p=np.array([1, 0.2, 0.2])/1.4)),
                     "Finesse": Ability(rng.choice([0, 1, 2],
                                                   p=np.array([1, 0.1, 0.1])/1.2)),
                     "Concentration": Ability(rng.choice([0, 1, 2],
                                                         p=np.array([1, 0.1, 0.1])/1.2)),
                    }
        tharray = [10, 8, 4, 2, 0]
        foarray = [11, 7, 3, 2, 0, 0, 0, 0, 0, 0]
        # characteristics are set by fixed array per techniques and forms
        techniques = assign_array(te, tharray, None, Art)
        forms = assign_array(fo, foarray, None, Art)
        prios = {}
        for key in abilities.keys():
            prios[key] = 0.5
        prios["Parma Magica"] = 2
        for key, stat in techniques.items():
            if rng.random() > 0.8:
                prios[key] = 2
            else:
                prios[key] = 0.5
        for key, stat in forms.items():
            if rng.random() > 0.8:
                prios[key] = 1
            else:
                prios[key] = 0.2
        stats = abilities | techniques | forms
    if template == "Mage":
        characteristics = get_characteristics_array(balance="uneven", ic=2)
        # set overall priorities first

        # assign key stats and remove from array and names to do

        # set ability priorities
        prio_dict = {}
    return Character(name,
                        char_input_year,
                        char_input_age,
                        stats,
                        prios,
                        characteristics,
                        rng,
                        rel_prio_weight,
                    )

if __name__ == '__main__':
    rng = np.random.default_rng()
    testy = gen_from_stats_array("Certamen",
                                 "Testy McCertamen",
                                 rel_prio_weight=0.1)
    print(testy)
    testy.set_to_year(1240)
    print(testy)
    testy.add_years(20)
    print(testy)
    testa = gen_from_stats_array("Certamen",
                                 "Testa McCertamen",
                                 rel_prio_weight=0.5)
    print(testa)
    testa.set_to_year(1240)
    print(testa)
    testa.add_years(20)
    print(testa)

    for i in range(10):
        print(get_characteristics_array(balance="uneven", ic=2))

