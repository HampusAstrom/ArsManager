import numpy as np

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
        print(f"val {val}, rest {rest}")
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

    def __init__(self,
                 name: str,
                 char_input_year: int,
                 char_input_age: int,
                 stats: dict) -> None:
        self.name = name
        self.char_input_year = char_input_year
        self.char_input_age = char_input_age
        self.stats = stats












# some local temporary tests
if __name__ == '__main__':
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
