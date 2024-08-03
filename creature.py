import random


class Creature:
    def __init__(
        self,
        name: str,
        die_list_dict: dict,  # "ATK" : ['d4', 'd4']
    ):
        self.name = name
        self.dice = die_list_dict
        self.health = None
        self.is_alive = None
        self._last_dmg_taken = None

    def __str__(self):
        return f"""### {self.name}
    :game_dice: HP: {self.health}
    ATK: {self.attack}
    DEF: {self.health}"""

    def attack(self, target):
        dmg_to_target = self._roll_dice("ATK")
        dmg_from_target = target._roll_dice("ATK")

        self._apply_dmg(dmg_from_target)
        target._apply_dmg(dmg_to_target)

    def _apply_dmg(self, dmg):
        self._last_dmg_taken = dmg
        self.health -= dmg
        if self.health <= 0:
            self.is_alive = False

    def set_HP(self):
        self.health = self._roll_dice("HP")
        self.is_alive = True
        print(f"{self.name} has {self.health} HP")

    def _roll_dice(self, category):
        total = 0
        for die in self.dice[category]:
            total += self._roll(die)
        return total

    def _roll(self, d):
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


def Generate_New_Creature():
    hp_bonus = random.randint(0, 50)
    atk_bonus = random.randint(0, 10)
    def_bonus = random.randint(0, 10)
    return Creature(hp_bonus, atk_bonus, def_bonus)
