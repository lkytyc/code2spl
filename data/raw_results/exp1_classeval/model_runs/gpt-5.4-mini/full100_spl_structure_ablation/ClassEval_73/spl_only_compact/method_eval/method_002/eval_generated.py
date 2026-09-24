class RPGCharacter:
    def __init__(self, name, hp, attack_power, defense, level=1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other_character):
        damage = max(self.attack_power - other_character.defense, 1)
        other_character.hp -= damage

    def gain_exp(self, amount):
        start = amount
        while amount != 0:
            threshold_check = self.exp + amount >= self.level * 100
            if threshold_check:
                amount -= self.level * 100 - self.exp
                self.level_up()
                leveled_up = True
            else:
                self.exp += amount
                amount = 0
                xp_applied_and_finished = True

    def heal(self):
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def is_alive(self):
        hp_value = self.hp
        is_alive_result = hp_value > 0
        return is_alive_result

    def level_up(self):
        level_check = self.level < 100
        if level_check:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attack_power += 5
            self.defense += 5
        return (self.level, self.hp, self.attack_power, self.defense)

import unittest

class RPGCharacterTestGainExp(unittest.TestCase):

    # exp not overflow
    def test_gain_exp_1(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.gain_exp(100)
        self.assertEqual(character.level, 2)
        self.assertEqual(character.exp, 0)

    # exp overflow
    def test_gain_exp_2(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.gain_exp(1100)
        self.assertEqual(character.level, 5)
        self.assertEqual(character.exp, 100)

    def test_gain_exp_3(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.gain_exp(200)
        self.assertEqual(character.level, 2)
        self.assertEqual(character.exp, 100)

    def test_gain_exp_4(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.gain_exp(300)
        self.assertEqual(character.level, 3)
        self.assertEqual(character.exp, 0)

    def test_gain_exp_5(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.gain_exp(400)
        self.assertEqual(character.level, 3)
        self.assertEqual(character.exp, 100)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
