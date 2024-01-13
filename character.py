import numpy as np
import copy
import itertools
import json
import importlib

def dict2string(dct, sort=True, lb=False) -> str:
    if sort:
        dct = dict(sorted(dct.items()))
    s = ""
    for key, val in dct.items():
        if lb:
            s += f"{key}: {val}\n"
        else:
            s += f"{key}: {val} "
    return s

# only tracks values of the ability, assume that the name will be tracked when 
# it is stored in a stats dict
class Ability:
    def __init__(self,
                 value: int = 0,
                 xp: int = 0,
                 tot_xp: bool = False, # used when inputing only xp
                 ) -> None:
        if tot_xp:
            self._tot_xp = 0
            self.add_xp(xp)
        else:
            self.set_val(value, xp)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self):
        return self.__str__()

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> int:
        return float(self._value)

    def __json__(self):
        return self._tot_xp

    @staticmethod
    def xp2val(xp: int) -> tuple[int, int]:
        val = int(-1/2 + np.sqrt(1/4 + 2*xp/5))
        return val, xp-Ability.val2xp(val)

    @staticmethod
    def val2xp(val: int) -> int:
        return 5*(1+val)*val/2

    def add_xp(self, xp: int) -> None:
        assert xp >= 0
        self._tot_xp = self._tot_xp + xp
        val, rest = self.xp2val(self._tot_xp)
        self._value = val

    def set_val(self, value: int, xp: int = 0) -> None:
        assert value >= 0
        assert xp >= 0
        assert value*5 >= xp # otherwise value should be higher
        self._value = value
        self._tot_xp = self.val2xp(value) + xp
    
    @property
    def tot_xp(self) -> int:
        return self._tot_xp

    @tot_xp.setter
    def tot_xp(self, xp: int) -> None:
        self._tot_xp = 0
        self.add_xp(xp)

    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, val) -> None:
        self.set_val(val)
    
    def get_rest_xp(self) -> int:
        return self.tot_xp - self.val2xp(self._value)

# only tracks values of the ability, assume that the name will be tracked when 
# it is stored in a stats dict
class Art(Ability):
    def __init__(self,
                 value: int = 0,
                 xp: int = 0,
                 tot_xp: bool = False
                 ) -> None:
        super().__init__(value, xp, tot_xp)
    
    @staticmethod
    def xp2val(xp) -> tuple[int, int]:
        val = int(-1/2 + np.sqrt(1/4 + 2*xp))
        return val, xp-Art.val2xp(val)

    @staticmethod
    def val2xp(val) -> int:
        return (1+val)*val/2

    def set_val(self, value: int, xp: int = 0) -> None:
        assert value >= 0
        assert xp >= 0
        assert value >= xp # otherwise value should be higher
        self._value = value
        self._tot_xp = self.val2xp(value) + xp

class Character:
    # TODO add function support for varying budget based on age
    # TODO add parameters or function support to vary xp distribution
    # TODO determine if any of the input parameters needs to be deepcopied
    def __init__(self,
                 name: str,
                 char_input_year: int,
                 char_input_age: int,
                 stats: dict,
                 prios: dict,
                 characteristics: dict,
                 rng: np.random.Generator = None,
                 rel_prio_weight: float = 1,
                 rel_art_xp_weight: float = 1.2,
                 budget: int = 30,
                 chunk_mean: int = 5,
                 current_year: int = None,
                 softcapped_stats: dict = None,
                 groups: dict = None,
                 char_info = None, # free field for notes or so
                 ) -> None:
        assert char_input_age >= 0
        assert budget > 0
        assert chunk_mean > 0
        assert self.check_same_keys(stats, prios)
        assert isinstance(current_year, (int,type(None)))
        self.name = name
        # groups: organized like groups in setting type as key names in values
        self.groups = groups
        self.char_info = char_info
        self.char_input_year = char_input_year
        self.char_input_age = char_input_age
        self.characteristics = characteristics
        self.rng = rng
        self.rel_prio_weight = rel_prio_weight
        self.rel_art_xp_weight = rel_art_xp_weight
        self.prios = prios
        self.budget = budget
        self.chunk_mean = chunk_mean
        self.stats = stats
        self.history = {char_input_year: copy.deepcopy(stats)}
        if softcapped_stats is None:
            self.softcapped_stats = {}
        else:
            self.softcapped_stats = softcapped_stats
        if current_year is None:
            current_year = char_input_year
        self.set_to_year(current_year)

    @staticmethod
    def check_same_keys(dict1, dict2):
        return dict1.keys() == dict2.keys()

    def set_to_year(self, year: int):
        assert year >= self.char_input_year
        self._current_year = year

        if year in self.history:
            self.stats = copy.deepcopy(self.history[year])
        else:
            cyear, cstats = self.get_last_year()
            while cyear < year:
                cyear += 1
                assert cyear not in self.history
                cstats = self._step_stats(cstats)
                self.history[cyear] = cstats
            assert cyear == year
            self.stats = copy.deepcopy(cstats)

        self._current_year = year
        self._update_age()

    def add_years(self, years):
        assert years > 0
        self.set_to_year(self._current_year + years)

    def _step_stats(self, prev_stats: dict) -> dict:
        assert self.check_same_keys(prev_stats, self.prios)
        stats = copy.deepcopy(prev_stats)
        rng = self.rng
        off = int(self.chunk_mean/2) # default chunk offset range
        budget = self.budget # TODO budget could depend on age later
        # build weight measure

        temp_stats = dict(sorted(copy.deepcopy(stats).items()))
        keys = list(temp_stats.keys())
        # filter out xp weight of softcapped skills like languages
        # if cap is reached we give no weight from xp, only prio
        for key, cap in self.softcapped_stats.items():
            if key in temp_stats and temp_stats[key].value >= cap:
                temp_stats[key] = Ability(0)
        # adjust (most often increase) weight from current xp of arts
        for key, stat in temp_stats.items():
            if isinstance(stat, Art):
                temp_stats[key].tot_xp *= self.rel_art_xp_weight
        pri = [weight for key,weight in sorted(self.prios.items())]
        sts = [int(stat.tot_xp) for stat in temp_stats.values()]
        weight = self.calc_weights(np.array(sts),
                                   np.array(pri),
                                   self.rel_prio_weight)
        # start adding xp
        while budget > 0:
            # xp to add
            chunk = min(budget,
                        rng.integers(self.chunk_mean-off,
                                     self.chunk_mean+off+1))
            # select stat to add to
            # if we don't use replacement we might get stuck in infinite loop
            # lets run with replacement for now
            key = rng.choice(keys, p=weight/sum(weight))
            stats[key].add_xp(chunk)
            budget -= chunk
        return stats

    @staticmethod
    def calc_weights(sts, pri, rel_prio_weight = 1):
        sts = sts / np.linalg.norm(sts)
        pri = pri / np.linalg.norm(pri)
        # TODO possilly apply function to pri before adding
        w = np.add(sts, pri*rel_prio_weight)
        return w

    def get_last_year(self) -> tuple[int, dict]:
        year = max(self.history.keys())
        return year, copy.deepcopy(self.history[max(self.history.keys())])

    def _update_age(self) -> None:
        self.current_age = self._current_year \
                           - self.char_input_year \
                           + self.char_input_age

    def get_arts_and_abilities(self, stats: dict = None) -> tuple[dict, dict]:
        abilities = {}
        arts = {}
        if not stats:
            stats = self.stats
        # assumes no other type of Abilities to separate
        for key, val in stats.items():
            if isinstance(val, Art):
                arts[key] = val
            else:
                abilities[key] = val
        return abilities, arts
    
    @staticmethod
    def separate_tech_and_form(arts) -> tuple[dict, dict]:
        t = ["Cr","In","Mu","Pe","Re",]
        tech = {}
        form = {}
        for key, val in arts.items():
            if key in t:
                tech[key] = val
            else:
                form[key] = val
        return tech, form

    def __str__(self) -> str:
        s = f"Name: {self.name} Age: {self.current_age}\n"
        if self.char_info is not None:
            s += self.char_info
            s += "\n"
        s += f"Characteristics: {dict2string(self.characteristics, sort=False)}\n"
        abilites, arts = self.get_arts_and_abilities()
        tech, form = self.separate_tech_and_form(arts)
        s += f"Abilities: {dict2string(abilites)}\n"
        s += f"Techniques: {dict2string(tech)}\n"
        s += f"Forms: {dict2string(form)}\n"
        return s

    def to_dict(self):
        ret = {"Name": self.name, "Age": self.current_age}
        ret |= self.characteristics
        for key, val in self.stats.items():
            ret[key] = val.value
        return ret

    def __json__(self):
        # Customize serialization for the Character class
        abilities, arts = self.get_arts_and_abilities()
        history = {}
        for year, sts in self.history.items():
            ab, ar = self.get_arts_and_abilities(sts)
            history[year] = {"abilities": ab, "arts": ar}
        return {
            "name": self.name,
            "groups": self.groups,
            "char_info": self.char_info,
            "char_input_year": self.char_input_year,
            "char_input_age": self.char_input_age,
            "characteristics": self.characteristics,
            "abilities": abilities,
            "arts": arts,
            "prios": self.prios,
            # "rng": self.rng.bit_generator.state,
            "rel_prio_weight": self.rel_prio_weight,
            "rel_art_xp_weight": self.rel_art_xp_weight,
            "budget": self.budget,
            "chunk_mean": self.chunk_mean,
            "current_year": self._current_year,
            "softcapped_stats": self.softcapped_stats,
            "groups": self.groups,
            "history": history,
        }

    @classmethod
    def stats_from_json(cls, stats_data, stat_cls):
        stats = {}
        for name, xp in stats_data.items():
            stats[name] = stat_cls(xp = xp, tot_xp = True)
        return stats

    @classmethod
    def from_json(cls, serialized_data):
        # Customize deserialization for the Character class
        stats = cls.stats_from_json(serialized_data["abilities"], Ability)
        stats |= cls.stats_from_json(serialized_data["arts"], Art)

        char = cls(
            name=serialized_data["name"],
            char_input_year=serialized_data["char_input_year"],
            char_input_age=serialized_data["char_input_age"],
            stats=stats,
            prios=serialized_data["prios"],
            characteristics=serialized_data["characteristics"],
            rel_prio_weight=serialized_data["rel_prio_weight"],
            rel_art_xp_weight=serialized_data["rel_art_xp_weight"],
            budget=serialized_data["budget"],
            chunk_mean=serialized_data["chunk_mean"],
            softcapped_stats=serialized_data["softcapped_stats"],
            groups=serialized_data["groups"],
            char_info=serialized_data["char_info"],
        )

        for year, stats in serialized_data["history"].items():
            hstats = cls.stats_from_json(stats["abilities"], Ability)
            hstats |= cls.stats_from_json(stats["arts"], Art)
            char.history[int(year)] = hstats

        char._current_year = int(serialized_data["current_year"])

        return char

    # TODO add method for renaming ability (and fixing it through history)

    # TODO add method to add xp without moving year to generate initial stats

    # TODO add option to ignore/reduce some stats as weights with a mask
    # to mask out things like having 5 in native language

    # TODO add way to use function to readjust weights of existing xp
    # both to handle diff between arts and abilities and to taper of skills
    # like languages after they are mastered (lvl 4-6ish)

    # TODO consider if I need some @x.setter or @x.getter functions to 
    # return copies of variables

def calc_used_xp(array: list, tpe: type) -> int:
    sm = 0
    for val in array:
        t = tpe(val)
        sm += t.tot_xp
    return sm

def calc_used_xp_total(abilites: list,
                       tech: list,
                       form: list,
                       prnt: bool = True) -> tuple[int, int, int, int]:
    sab = calc_used_xp(abilites, Ability)
    ste = calc_used_xp(tech, Art)
    sfo = calc_used_xp(form, Art)
    tot = sab + ste + sfo
    if prnt:
        print(f"Total xp used {tot}")
        print(f"Ability xp {sab}")
        print(f"Technique xp {ste}")
        print(f"Form xp {sfo}")
        print()
    return tot, sab, ste, sfo

def pad_list_of_lists(lst: list):
    ret = np.zeros([len(lst),len(max(lst,key = lambda x: len(x)))])
    for i,j in enumerate(lst):
        ret[i][0:len(j)] = j
    return ret

# some local temporary tests
if __name__ == '__main__':
    rng = np.random.default_rng()
    # Ability and Art
    # mt = Ability(3, xp=23)
    mt = Ability(3, xp=5)
    print(f"val {mt.value}, tot {mt.tot_xp}")
    mt.add_xp(23)
    print(mt.value)
    print(mt.get_rest_xp())
    print(mt.tot_xp)
    print()
    cr = Art(8, xp=5)
    print(f"val {cr.value}, tot {cr.tot_xp}")
    cr.add_xp(23)
    print(cr.value)
    print(cr.get_rest_xp())
    print(cr.tot_xp)
    cr.tot_xp = 50
    print(cr.value)
    print(cr.get_rest_xp())
    print(cr.tot_xp)
    print()
    print(Ability.val2xp(5))
    print(Ability.xp2val(70))

    # Bjorn
    bj_abilities = [1, 2, 2, 2, 1, 1, 1, 2, 2, 4, 5, 1, 3, 1, 1, 1, 1, 3,]
    bj_tech = [0, 1, 10, 3, 1]
    bj_form = [8, 0, 0, 8, 0, 0, 0, 0, 0, 0]
    # Boni
    bo_abilities = [1, 2, 2, 3, 2, 4, 1, 4, 5, 2, 1, 1, 3,]
    bo_tech = [12, 0, 0, 0, 3,]
    bo_form = [0, 0, 12, 4, 0, 0, 0, 0, 0, 0]

    # Cria
    cr_abilities = [1, 5, 3, 3+2, 1, 4, 2, 3, 5, 1, 1]
    cr_abilities_wo = [1, 5, 3, 3, 1, 4, 2, 3, 5, 1, 1]
    cr_tech = [4, 6, 4, 4, 4]
    cr_form = [0, 0, 0, 0, 0, 0, 2, 1, 0, 10]

    # Ex Misc
    ex_abilities = [3, 1, 3, 3, 2, 4, 3, 5, 1, 2, 3]
    ex_tech = [8, 0, 4, 3, 5,]
    ex_form = [0, 0, 0, 1, 0, 0, 0, 0, 12+3, 0]
    ex_form_wo = [0, 0, 0, 1, 0, 0, 0, 0, 12, 0]

    # Flam
    fl_abilities = [2, 1, 2, 3, 2, 1, 3, 1, 4, 5, 3, 1, 2, 1, 1]
    fl_tech = [12, 0, 0, 4, 5]
    fl_form = [0, 0, 0, 0, 0, 12+3, 0, 0, 1, 0]

    # Guer
    gu_abilities = [1, 3, 1, 2, 3, 1, 4, 2, 4, 3, 5, 1, 1]
    gu_tech = [0, 12+3, 0, 2, 0,]
    gu_form = [0, 0, 0, 5, 0, 0, 6, 6, 0, 0]

    # Jerb
    je_abilities = [1, 2, 3, 1, 2, 2, 2, 5, 3, 4+2, 5, 2, 1]
    je_tech = [6, 1, 6, 1, 6,]
    je_form = [0, 0, 0, 5, 0, 0, 10, 0, 0, 0]

    # Merc
    mc_abilities = [3, 1, 1, 1, 2, 4, 3, 5, 1, 2, 3, 4,]
    mc_tech = [6+3, 4, 4, 3, 5,]
    mc_form = [0, 0, 12+3, 2, 0, 0, 0, 2, 0, 0]

    # Meri
    mi_abilities = [1, 2, 3, 2, 5, 4, 3, 5, 2, 1,]
    mi_tech = [5, 1, 5, 2, 5]
    mi_form = [0, 0, 0, 1, 0, 0, 10+3, 5, 0, 0]

    # Trem
    tr_abilities = [1, 2, 1, 2, 2, 3, 2, 2, 4, 3, 3, 5, 2, 1, 3]
    tr_tech = [5, 5, 5, 5, 5,]
    tr_form = [0, 3, 6, 0, 0, 6, 0, 1, 6, 0]

    # Tyta
    ty_abilities = [1, 2, 2, 3, 2, 2, 2, 4, 2, 3, 5, 1]
    ty_tech = [5, 5, 0, 0, 5,]
    ty_form = [0, 0, 0, 0, 0, 0, 0, 9, 0, 0,]

    # Verd
    ve_abilities = [1, 3, 2, 5+2, 4+2, 2, 4, 3, 5, 1, 1,]
    ve_tech = [7, 3, 5, 3, 5,]
    ve_form = [0, 0, 0, 0, 0, 0, 0, 0, 12+3, 0]

    template_abilities = [sorted(bj_abilities, reverse=True),
                          sorted(bo_abilities, reverse=True),
                          sorted(cr_abilities, reverse=True),
                          sorted(ex_abilities, reverse=True),
                          sorted(fl_abilities, reverse=True),
                          sorted(gu_abilities, reverse=True),
                          sorted(je_abilities, reverse=True),
                          sorted(mc_abilities, reverse=True),
                          sorted(mi_abilities, reverse=True),
                          sorted(tr_abilities, reverse=True),
                          sorted(ty_abilities, reverse=True),
                          sorted(ve_abilities, reverse=True)]
    template_tech = [sorted(bj_tech, reverse=True),
                     sorted(bo_tech, reverse=True),
                     sorted(cr_tech, reverse=True),
                     sorted(ex_tech, reverse=True),
                     sorted(fl_tech, reverse=True),
                     sorted(gu_tech, reverse=True),
                     sorted(je_tech, reverse=True),
                     sorted(mc_tech, reverse=True),
                     sorted(mi_tech, reverse=True),
                     sorted(tr_tech, reverse=True),
                     sorted(ty_tech, reverse=True),
                     sorted(ve_tech, reverse=True)]
    template_form = [sorted(bj_form, reverse=True),
                     sorted(bo_form, reverse=True),
                     sorted(cr_form, reverse=True),
                     sorted(ex_form, reverse=True),
                     sorted(fl_form, reverse=True),
                     sorted(gu_form, reverse=True),
                     sorted(je_form, reverse=True),
                     sorted(mc_form, reverse=True),
                     sorted(mi_form, reverse=True),
                     sorted(tr_form, reverse=True),
                     sorted(ty_form, reverse=True),
                     sorted(ve_form, reverse=True)]

    mean_char_xp = 0
    mean_ab_xp = 0
    mean_te_xp = 0
    mean_fo_xp = 0
    std_char_xp = 0
    std_ab_xp = 0
    std_te_xp = 0
    std_fo_xp = 0
    n = 12
    for i in range(n):
        tot, sab, ste, sfo = calc_used_xp_total(template_abilities[i],
                                           template_tech[i],
                                           template_form[i])
        mean_char_xp += tot/n
        mean_ab_xp += sab/n
        mean_te_xp += ste/n
        mean_fo_xp += sfo/n
    for i in range(12):
        tot, sab, ste, sfo = calc_used_xp_total(template_abilities[i],
                                           template_tech[i],
                                           template_form[i],
                                           prnt=False)
        std_char_xp += ((tot-mean_char_xp)**2)/n
        std_ab_xp += ((sab-mean_ab_xp)**2)/n
        std_te_xp += ((ste-mean_te_xp)**2)/n
        std_fo_xp += ((sfo-mean_fo_xp)**2)/n

    print(f"Mean char xp: {mean_char_xp} +- {np.sqrt(std_char_xp)}")
    print(f"Mean ability xp: {mean_ab_xp} +- {np.sqrt(std_ab_xp)}")
    print(f"Mean tech xp: {mean_te_xp} +- {np.sqrt(std_te_xp)}")
    print(f"Mean form xp: {mean_fo_xp} +- {np.sqrt(std_fo_xp)}")

    max_ab_length = 0
    for list in template_abilities:
        if len(list) > max_ab_length:
            max_ab_length = len(list)

    mean_ab_array = np.array([0.]*max_ab_length)
    mean_te_array = np.array([0.]*5)
    mean_fo_array = np.array([0.]*10)

    template_abilities_padded = zip(*itertools.zip_longest(*template_abilities,
                                                           fillvalue=0))

    for ab, te, fo in zip(template_abilities_padded, template_tech, template_form):
        mean_ab_array += np.array(sorted(ab, reverse=True))/12
        mean_te_array += np.array(sorted(te, reverse=True))/12
        mean_fo_array += np.array(sorted(fo, reverse=True))/12

    print(mean_ab_array)
    print(mean_te_array)
    print(mean_fo_array)

    template_abilities_arranged = np.array(pad_list_of_lists(template_abilities))
    median_ab_array = np.median(template_abilities_arranged, axis=0)
    print(median_ab_array)
    print(template_abilities_arranged)

    default_ability_array = [5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1,] # rest should be 0
    default_tech_array = [9, 6, 3, 2, 0]
    deafult_form_array = [10, 8, 1, 0, 0, 0, 0, 0, 0, 0,]
    tot, sab, ste, sfo = calc_used_xp_total(default_ability_array,
                                            default_tech_array,
                                            deafult_form_array)

    # it's not recommended to have both tech and form as even
    even_ability_array = [5, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,] # rest should be 0
    even_tech_array = [8, 5, 5, 3, 2]
    even_form_array = [8, 6, 5, 4, 3, 2, 1, 0, 0, 0,]
    tot, sab, ste, sfo = calc_used_xp_total(even_ability_array,
                                            even_tech_array,
                                            even_form_array)

    uneven_ability_array = [6, 5, 4, 3, 3, 2, 2, 1, 1, 1,] # rest should be 0
    uneven_tech_array = [10, 5, 3, 0, 0]
    uneven_form_array = [12, 4, 2, 1, 0, 0, 0, 0, 0, 0,]
    tot, sab, ste, sfo = calc_used_xp_total(uneven_ability_array,
                                            uneven_tech_array,
                                            uneven_form_array)

    extreme_ability_array = [7, 5, 4, 3, 2, 2, 1, 1,] # rest should be 0
    extreme_tech_array = [11, 3, 2, 0, 0]
    extreme_form_array = [13, 1, 0, 0, 0, 0, 0, 0, 0, 0,]
    tot, sab, ste, sfo = calc_used_xp_total(extreme_ability_array,
                                            extreme_tech_array,
                                            extreme_form_array)