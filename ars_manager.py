import numpy as np
import copy

# only tracks values of the ability, assume that the name will be tracked when 
# it is stored in a stats dict
class Ability:
    def __init__(self,
                 value: int = 0,
                 xp: int = 0,
                 tot_xp: bool = False, # used when inputing only xp
                 ) -> None:
        if tot_xp:
            self.tot_xp = 0
            self.addxp(xp)
        else:
            self.set_val(value, xp)

    @staticmethod
    def xp2val(xp: int) -> tuple[int, int]:
        val = int(-1/2 + np.sqrt(1/4 + 2*xp/5))
        return val, xp-Ability.val2xp(val)

    @staticmethod
    def val2xp(val: int) -> int:
        return 5*(1+val)*val/2

    def add_xp(self, xp: int) -> None:
        assert xp >= 0
        self.tot_xp = self.tot_xp + xp
        val, rest = self.xp2val(self.tot_xp)
        self.value = val

    def set_val(self, value: int, xp: int = 0) -> None:
        assert value >= 0
        assert xp >= 0
        assert value*5 >= xp # otherwise value should be higher
        self.value = value
        print(f"set {self.val2xp(value)} + {xp}")
        self.tot_xp = self.val2xp(value) + xp
    
    def set_xp(self, xp: int) -> None:
        self.tot_xp = 0
        self.addxp(xp)

    def get_value(self) -> int:
        return self.value
    
    def get_tot_xp(self) -> int:
        return self.tot_xp
    
    def get_rest_xp(self) -> int:
        return self.tot_xp - self.val2xp(self.value)

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
                 prio: dict,
                 characteristics: dict,
                 rng: np.random.Generator,
                 budget: int = 15,
                 chunk_mean: int = 5,
                 current_year: int = None,
                 char_info = None, # free field for notes or so
                 ) -> None:
        assert char_input_age >= 0
        assert budget > 0
        assert chunk_mean > 0
        assert self.check_same_keys(stats, prio)
        self.name = name
        self.char_info = char_info
        self.char_input_year = char_input_year
        self.char_input_age = char_input_age
        self.characteristics = characteristics
        self.rng = rng
        self.prio = prio
        self.budget = budget
        self.chunk_mean = chunk_mean
        self.stats = stats
        self.history = {char_input_year: copy.deepcopy(stats)}
        if current_year is None:
            current_year = char_input_year
        self.set_to_year(current_year)

    @staticmethod
    def check_same_keys(prio, stats):
        return prio.keys() == stats.keys()

    def set_to_year(self, year: int):
        assert year >= self.char_input_year
        self.current_year = year

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

        self.current_year = year
        self._update_age()

    def _step_stats(self, prev_stats: dict) -> dict:
        stats = copy.deepcopy(prev_stats)
        rng = self.rng
        off = int(self.chunk_mean/2) # default chunk offset range
        budget = self.budget # TODO budget could depend on age later
        # build weight measure
        temp = sorted(stats.items())
        keys, sts = zip(*temp)
        pri = [value for key,value in sorted(self.prio.items())]
        weight = self.calc_weights(np.array(sts), np.array(pri))
        # start adding xp
        while budget > 0:
            # xp to add
            chunk = min(budget,
                        rng.integers(self.chunk_mean-off, self.chunk_mean+off+1))
            # select stat to add to
            # if we don't use replacement we might get stuck in infinite loop
            # lets run with replacement for now
            key = rng.choice(keys, p=weight)
            stats[key].add_xp(chunk)
            budget -= chunk
        return stats

    @staticmethod
    def calc_weights(sts, pri):
        sts = sts / np.linalg.norm(sts)
        pri = pri / np.linalg.norm(pri)
        # TODO possilly apply function to pri before adding
        w = np.add(sts, pri)

    def get_last_year(self) -> tuple[int, dict]:
        year = max(self.history.keys())
        return year, copy.deepcopy(self.history[max(self.history.keys())])

    def _update_age(self):
        self.current_age = self.current_year \
                           - self.char_input_year \
                           + self.char_input_age

# some local temporary tests
if __name__ == '__main__':
    rng = np.random.default_rng()
    # Ability and Art
    # mt = Ability(3, xp=23)
    mt = Ability(3, xp=5)
    print(f"val {mt.get_value()}, tot {mt.get_tot_xp()}")
    mt.add_xp(23)
    print(mt.get_value())
    print(mt.get_rest_xp())
    print(mt.get_tot_xp())
    print()
    cr = Art(8, xp=5)
    print(f"val {cr.get_value()}, tot {cr.get_tot_xp()}")
    cr.add_xp(23)
    print(cr.get_value())
    print(cr.get_rest_xp())
    print(cr.get_tot_xp())
    print()
    print(Ability.val2xp(5))
    print(Ability.xp2val(70))
