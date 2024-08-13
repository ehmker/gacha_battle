import random


class Creature:
    def __init__(
        self,
        name: str,
        die_list_dict: dict,  # "ATK" : ['d4', 'd4']
    ):
        self.name = name
        self.dice = die_list_dict
        self.max_hp = None
        self.cur_hp = None
        self.is_alive = None

    def __repr__(self):
        out_string = f"## {self.name}\n### Dice:\n"
        for die_type, die_dict in self.dice.items():
            d_string = f"{die_type}: "
            for die, count in die_dict.items():
                d_string += f"{count}{die} + "
            d_string = d_string.rstrip(" +")
            out_string += d_string + "\n"
        return out_string

    # # rolls the attack die of the player and the target
    # # applies the damage roll to each entity
    # def attack(self, target) -> tuple:
    #     dmg_to_target = self.roll_dice("ATK")
    #     dmg_from_target = target._roll_dice("ATK")

    #     self._apply_dmg(dmg_from_target)
    #     target._apply_dmg(dmg_to_target)

    #     return (dmg_to_target, dmg_from_target)

    # applies the damage roll to the entity and updates is_alive attribute if necessary
    def _apply_dmg(self, dmg):
        self._last_dmg_taken = dmg
        self.cur_hp -= dmg
        if self.cur_hp <= 0:
            self.is_alive = False

    def initialize_HP(self):
        """
        Max HP of entity for a run is determined by the HP dice roll
        """
        hp_roll = self.roll_dice("HP")
        self.max_hp = hp_roll
        self.cur_hp = hp_roll
        self.is_alive = True

    # Method to roll entity's dice of the given category
    def roll_dice(self, category):
        total = 0
        for die in self.dice[category]:
            total += self._roll(die)
        return total

    def _roll(self, d):
        """
        Method to handle each dice class
        """
        match d:
            case "d4":
                return random.randint(1, 4)
            case "d6":
                return random.randint(1, 6)
            case "d8":
                return random.randint(1, 8)
            case "d10":
                return random.randint(1, 10)
            case "d12":
                return random.randint(1, 12)
            case "d20":
                return random.randint(1, 20)

    # Processes the recovery check and returns results of the roll as a tuple
    # (END_check_roll, REC_amount_roll)
    # REC_amount_roll = None if END_check is not successful
    def recover(self) -> int:
        if not self.is_alive:
            return None
        recover_amt = self.roll_dice("REC")
        if recover_amt + self.cur_hp > self.max_hp:
            self.cur_hp = self.max_hp
        else:
            self.cur_hp += recover_amt
        return recover_amt
