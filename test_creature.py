import unittest
import random
from creature import Creature


class TestCreatureActions(unittest.TestCase):
    def test_atk(self):
        random.seed(1)
        p1_dice = {"HP": ["d8"], "ATK": ["d6"], "END": ["d4"], "REC": ["d4"]}
        p2_dice = {"HP": ["d8"], "ATK": ["d4"], "END": ["d6"], "REC": ["d4"]}

        test_p1 = Creature("My_Test_Player1", p1_dice)
        test_p2 = Creature("My_Test_Plater2", p2_dice)

        test_p1.health = 10
        test_p2.health = 10

        test_p1.attack(test_p2)
