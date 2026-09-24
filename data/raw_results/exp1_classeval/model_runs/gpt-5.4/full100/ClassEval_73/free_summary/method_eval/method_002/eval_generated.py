class RPGCharacter:
    def __init__(self, name, hp, attack_power, defense, level=1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.experience = 0

    def attack(self, other):
        damage = max(1, self.attack_power - other.defense)
        other.hp -= damage
        return damage

    def heal(self):
        self.hp = min(100, self.hp + 10)
        return self.hp

    def gain_exp(self, amount):
        self.experience += amount
        while self.level < 100:
            exp_to_next_level = self.level * 100
            if self.experience >= exp_to_next_level:
                self.experience -= exp_to_next_level
                self.level_up()
            else:
                break
        if self.level >= 100:
            self.experience = 0
        return self.level, self.experience

    def level_up(self):
        if self.level < 100:
            self.level += 1
            self.experience = 0
            self.hp = min(100, self.hp + 20)
            self.attack_power += 5
            self.defense += 2
        return self.level, self.hp, self.attack_power, self.defense

    def is_alive(self):
        return self.hp > 0

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
