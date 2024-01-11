import numpy as np
from character import Character, Ability, Art
from collections import defaultdict
from  lists_and_data import *
import copy

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
        abilities = GENABILITIES + ACAABILITIES + ARCABILITIES + MARABILITIES
        return characteristics, abilities, tech, form
    else:
        raise Exception(f"There is no template named {name}") 

# designed for mages, at least change prio for other characters
def get_characteristics_array(balance: str = "default", ic: int = 1):
    names = ["Int", "Per", "Str", "Sta", "Pre", "Com", "Dex", "Qik",]
    return assign_array(names,
                        CHAR_ARRAYS[balance][ic],
                        CHAR_ARRAYS[balance]["prio"],
                        int)

def shift_abilities(ab_dict: dict,
                    shift_dict: dict,
                    ) -> dict:
    additions = {}
    for ability, shift in shift_dict.items():
        if ability in ab_dict:
            val = ab_dict.pop(ability)
            for ad in shift:
                additions[ad[0]] = val*ad[1]
    return ab_dict | additions

# TODO assumes mage for now
def gen_ability_prio(primary_region: str = "default",
                     secondary_region: str = "default",
                     all_skills=False) -> tuple[dict, dict]:
    to_assign_array = [5, 2, 1, 1, 0.5, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0]
    area_prios = assign_array_prio_dict(SKILL_AREAS, to_assign_array, float, area=True)

    print(area_prios)
    # assemble master ability prio dict
    ability_prios = defaultdict(float)

    # select one supernatural ability
    if area_prios["Supernatural"] > 0:
        sup_arr = [0]*len(SUPERNATURAL)
        sup_arr[0] = 1
        sup_selection = assign_array_prio_dict(SUPERNATURAL, sup_arr, float)
        selected_sup_ability = [k for k,v in sup_selection.items() if v == 1]
        ability_prios[selected_sup_ability[0]] += area_prios.pop("Supernatural")
        # TODO if all_skills is used it gets funky with super powers in list
        # dependent on if this triggers or not

    # weigh skills by area prio
    # only add skills if prio > 0, unless overridden
    for area, weight in area_prios.items():
        # don't add skills without weight
        if not all_skills and weight == 0:
            continue
        # get sum of area to normalize with
        area_sum = 0
        for ab_name, sub_prio in SKILL_AREAS[area][0].items():
            area_sum += sub_prio
        # add skills weighted by area prio, prio in are and normed
        # by sum of prio values in area
        for ab_name, sub_prio in SKILL_AREAS[area][0].items():
            ability_prios[ab_name] += sub_prio*weight/area_sum

    # regional adjustments
    if primary_region in ["Greece", "Greek"]:
        ability_prios = shift_abilities(ability_prios, GREEK_SHIFT)
    if primary_region in ["Middle East", "Africa", "Arabia", "Arabic"]:
        ability_prios = shift_abilities(ability_prios, ARABIC_SHIFT)
    if primary_region in ["England", "British Isles"]:
        ability_prios = shift_abilities(ability_prios, ENGLISH_SHIFT)

    # TODO improve to full handling
    if secondary_region in ["Middle East", "Africa", "Arabia", "Arabic"]:
        ability_prios["Arabic"] += ability_prios.pop("Foreign Language 1")

    return ability_prios, area_prios

def add_req_to_prio(prio: dict, req: dict) -> dict:
    for key, val in req.items():
        if key not in prio:
            prio[key] = 0.00000001
    return prio

def assign_array_prio_dict(dct: dict,
                           array: list,
                           tpe: type,
                           area: bool = False,
                           req: dict = None,
                           ) -> dict:
    prio = []
    names = []
    for n, p in dct.items():
        names.append(n)
        if area:
            prio.append(p[1])
        else:
            prio.append(p)
    if req:
        for n, p in req.items():
            if n not in names:
                names.append(n)
                prio.append(0.00000001)

    # TODO handle array longer than prio
    # pad array with 0s if longer than names
    array = copy.deepcopy(array)
    if len(names) > len(array):
        extra = len(names) - len(array)
        array += [0]*extra
    if req is not None:
        return _assign_array_with_min_req(names, array, prio, tpe, req)
    return assign_array(names, array, prio, tpe)

# TODO adjust so that partial lists can be assigned too
# (more names than array elements)
def assign_array(names: list,
                 array: list,
                 prio: list,
                 tpe: type,
                 ) -> dict:
    if prio == None:
        prio = [1]*len(names)
    array = copy.deepcopy(array)
    nms = rng.choice(names,
                     len(names),
                     replace=False,
                     p=np.array(prio)/sum(prio))
    return sort_by_name_list(names,
                             {name: tpe(val) for name, val in zip(nms, array)})

def _assign_array_with_min_req(names: list,
                 array: list,
                 prio: list,
                 tpe: type,
                 req: dict,
                 ) -> dict:
    if not req:
        return assign_array(names, array, prio, tpe)
    if prio == None:
        prio = [1]*len(names)
    # sort req by value
    array = copy.deepcopy(array)
    req = list(sorted(req.items(), key=lambda x:x[1], reverse=True))
    nms = rng.choice(names,
                     len(names),
                     replace=False,
                     p=np.array(prio)/sum(prio))
    ret_dict = {}
    nms = list(nms)
    while(len(array)>0):
        if not array:
            break
        val = array.pop(0)
        if req and val < req[0][1]:
            raise Exception("Required value cannot be assigned!")
        if req and val == req[0][1]:
            ret_dict[req[0][0]] = tpe(val)
            if req[0][0] in nms:
                nms.remove(req[0][0])
            req.pop(0)
        else:
            name = nms.pop(0)
            ret_dict[name] = tpe(val)
            req_names = [k for k, v in req]
            if name in req_names:
                index = req_names.index(name)
                req.pop(index)
    return sort_by_name_list(names, ret_dict)


def select_arrays() -> tuple[list, list, list]:
    ab_setting = select_array(ABILITY_ARRAYS, ABILITY_ARRAYS_PRIO)
    te_setting = select_array(TECH_ARRAYS, TECH_ARRAYS_PRIO)
    fo_setting = select_array(FORM_ARRAYS, FORM_ARRAYS_PRIO)
    return ab_setting, te_setting, fo_setting

def select_array(array, prio_dict) -> list:
    names = list(array.keys())
    prio = []
    for name in names:
        prio.append(prio_dict[name])
    setting = rng.choice(names,
                            1,
                            replace=False,
                            p=np.array(prio)/sum(prio))
    return array[setting[0]]


# generates standard age 25, just out of gauntlet mages from mostly fixed arrays
# of stats
def gen_from_stats_array(template: str,
                         name: str,
                         char_input_year: int = 1220,
                         char_input_age: int = 25,
                         rel_prio_weight: float = 1,
                         budget: int = 30,
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

    if template == "Mage":
        characteristics = get_characteristics_array(balance="uneven", ic=2)
        # set overall priorities first

        # assign key stats and remove from array and names to do

        # set ability priorities
        prios, area_prios = gen_ability_prio(secondary_region="Africa")
        ab_array, te_array, fo_array = select_arrays()

        prios = add_req_to_prio(prios, MAGE_REQUIRED_STATS)
        abilities = assign_array_prio_dict(prios,
                                           ab_array,
                                           Ability,
                                           req = MAGE_REQUIRED_STATS)
        techniques = assign_array(te, te_array, None, Art)
        forms = assign_array(fo, fo_array, None, Art)

        # perturb prios for abilities
        # otherwise they are same when selecting as when leveling and only
        # based on fixed values in areas * area prioritization
        for key, val in prios.items():
            r = rng.random()
            if  r > 0.8:
                prios[key] = val*2
            elif r > 0.6:
                prios[key] = val*1.3
            elif r < 0.4:
                prios[key] = val*0.4
            elif r < 0.2:
                prios[key] = val*0.3
            # 0.4 < r < 0.6 remains unchanged

        magic_prio_factor = area_prios["Magic"]*4 # TODO tune
        # TODO handle removing/supressing "capped" stats
        for key, stat in techniques.items():
            if rng.random() > 0.8:
                prios[key] = 4*magic_prio_factor
            else:
                prios[key] = 0.5*magic_prio_factor
        for key, stat in forms.items():
            if rng.random() > 0.8:
                prios[key] = 3*magic_prio_factor
            else:
                prios[key] = 0.2*magic_prio_factor

    stats = abilities | techniques | forms
    return Character(name,
                        char_input_year,
                        char_input_age,
                        stats,
                        prios,
                        characteristics,
                        rng,
                        rel_prio_weight,
                        budget = budget,
                        softcapped_stats=SOFTCAPPED_STATS
                    )

def example_use():
    rng = np.random.default_rng()
    testy = gen_from_stats_array("Certamen",
                                 "Testy McCertamen",
                                 rel_prio_weight=0.1,
                                 budget = 20)
    print(testy)
    testy.set_to_year(1240)
    print(testy)
    testy.add_years(20)
    print(testy)
    testa = gen_from_stats_array("Certamen",
                                 "Testa McCertamen",
                                 rel_prio_weight=0.5,
                                 budget = 20)
    print(testa)
    testa.set_to_year(1240)
    print(testa)
    testa.add_years(20)
    print(testa)

    for i in range(10):
        print(get_characteristics_array(balance="uneven", ic=1))

    print()
    examplo = gen_from_stats_array("Mage",
                                   "Examplo de Magicus",
                                   rel_prio_weight=0.5,
                                   budget=35,
                                   )
    print(examplo)
    examplo.add_years(20)
    print(examplo)
    examplo.add_years(20)
    print(examplo)
    examplo.add_years(20)
    print(examplo)
    print(examplo.prios)

if __name__ == '__main__':
    example_use()