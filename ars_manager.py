import numpy as np
from character import Character, Ability, Art

# initiate default rng
rng = np.random.default_rng()

def get_template(name: str) -> tuple[list, list, list]:
    characteristics = ["Int", "Per", "Pre", "Com", "Str", "Sta", "Dex", "Qik",]
    if name == "Certamen":
        characteristics = ["Int", "Per", "Pre", "Sta", "Qik",]
        abilities = ["Finesse", "Penetration", "Parma Magica",]
        tech = ["Cr","In","Mu","Pe","Re",]
        form = ["An","Aq","Au","Co","He","Ig","Im","Me","Te","Vi",]
        return characteristics, abilities, tech, form
    else:
        raise Exception(f"There is no template named {name}") 

def assign_array(names: str,
                 array: list,
                 prio: list,
                 tpe: type,
                 ) -> dict:
    if prio == None:
        prio = [1]*len(names)
    nms = rng.choice(names, len(names), replace=False, p=np.array(prio)/sum(prio))
    return {name: tpe(val) for name, val in zip(nms, array)}

# generates standard age 25, just out of gauntlet mages from mostly fixed arrays
# of stats
def gen_from_stats_array(template: str,
                         name: str,
                         char_input_year: int = 1220,
                         char_input_age: int = 25,
                         ) -> Character:
    if template == "Certamen":
        ch, ab, te, fo = get_template(template)
        charray = [3, 2, 1, 0, -1]
        chprio = [5, 1, 1, 2, 1]
        # characteristics are set by fixed array
        characteristics = assign_array(ch, charray, chprio, int)
        # abilities are mostly fixed
        abilities = {"Parma Magica": Ability(1),
                        "Penetration": Ability(rng.choice([0, 1, 2],
                                                          p=np.array([1, 0.2, 0.2])/1.4)),
                        "Finesse": Ability(rng.choice([0, 1, 2],
                                                      p=np.array([1, 0.1, 0.1])/1.2))
                        }
        tharray = [8, 5, 4, 2, 0]
        foarray = [11, 9, 4, 2, 0, 0, 0, 0, 0, 0]
        # characteristics are set by fixed array per techniques and forms
        techniques = assign_array(te, tharray, None, Art)
        forms = assign_array(fo, foarray, None, Art)
        prios = {}
        for key in abilities.keys():
            prios[key] = 0.5
        prios["Parma Magica"] = 2
        for key, stat in techniques.items():
            if stat.value > 5:
                prios[key] = 4
            elif rng.random() > 0.8:
                prios[key] = 1
            else:
                prios[key] = 0.3
        for key, stat in forms.items():
            if stat.value > 5:
                prios[key] = 4
            elif rng.random() > 0.8:
                prios[key] = 1
            else:
                prios[key] = 0.1
        stats = abilities | techniques | forms
        return Character(name,
                         char_input_year,
                         char_input_age,
                         stats,
                         prios,
                         characteristics,
                         rng,
                        )

if __name__ == '__main__':
    rng = np.random.default_rng()
    testy = gen_from_stats_array("Certamen", "Testy McChar")
    print(testy)
    testa = gen_from_stats_array("Certamen", "Testa McChar")
    print(testa)


