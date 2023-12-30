import numpy as np
import copy

def dict2string(dct, sort=True) -> str:
    if sort:
        dct = dict(sorted(dct.items()))
    s = ""
    for key, val in dct.items():
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
            self.addxp(xp)
        else:
            self.set_val(value, xp)

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> int:
        return float(self._value)

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
        self.addxp(xp)

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
                 value: int,
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
        assert value >= xp # otherwise value should be higher
        super().set_val(value, xp)

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
                 rng: np.random.Generator,
                 rel_prio_weight: float = 1,
                 budget: int = 20,
                 chunk_mean: int = 5,
                 current_year: int = None,
                 char_info = None, # free field for notes or so
                 ) -> None:
        assert char_input_age >= 0
        assert budget > 0
        assert chunk_mean > 0
        assert self.check_same_keys(stats, prios)
        self.name = name
        self.char_info = char_info
        self.char_input_year = char_input_year
        self.char_input_age = char_input_age
        self.characteristics = characteristics
        self.rng = rng
        self.rel_prio_weight = rel_prio_weight
        self.prios = prios
        self.budget = budget
        self.chunk_mean = chunk_mean
        self.stats = stats
        self.history = {char_input_year: copy.deepcopy(stats)}
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

    def _step_stats(self, prev_stats: dict) -> dict:
        stats = copy.deepcopy(prev_stats)
        rng = self.rng
        off = int(self.chunk_mean/2) # default chunk offset range
        budget = self.budget # TODO budget could depend on age later
        # build weight measure
        temp = sorted(stats.items())
        keys, sts = zip(*temp)
        pri = [value for key,value in sorted(self.prios.items())]
        sts = [int(value.tot_xp) for value in sts]
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

    def get_arts_and_abilities(self) -> tuple[dict, dict]:
        abilities = {}
        arts = {}
        # assumes no other type of Abilities to separate
        for key, val in self.stats.items():
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
        # TODO clean up this nested mess
        s += f"Abilities: {dict2string(abilites)}\n"
        s += f"Techniques: {dict2string(tech)}\n"
        s += f"Forms: {dict2string(form)}\n"
        return s

    # TODO consider if I need some @x.setter or @x.getter functions to 
    # return copies of variables

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
    print()
    print(Ability.val2xp(5))
    print(Ability.xp2val(70))
