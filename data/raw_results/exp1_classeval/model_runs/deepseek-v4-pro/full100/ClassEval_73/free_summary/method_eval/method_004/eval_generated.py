class RPGCharacter:
    def __init__(self, name, hp, attack_power, defense, level=1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other):
        damage = self.attack_power - other.defense
        if damage < 1:
            damage = 1
        other.hp -= damage

    def heal(self):
        self.hp += 10
        if self.hp > 100:
            self.hp = 100

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.level * 100 and self.level < 100:
            self.exp -= self.level * 100
            self.level_up()

    def level_up(self):
        if self.level < 100:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attack_power += 5
            self.defense += 5

    def is_alive(self):
        return self.hp > 0

import unittest

class RPGCharacterTestIsAlive(unittest.TestCase):
    def test_is_alive_1(self):
        character = RPGCharacter("John", 100, 20, 10)
        self.assertTrue(character.is_alive())

    def test_is_alive_2(self):
        character = RPGCharacter("John", 0, 20, 10)
        self.assertFalse(character.is_alive())

    def test_is_alive_3(self):
        character = RPGCharacter("John", -10, 20, 10)
        self.assertFalse(character.is_alive())

    def test_is_alive_4(self):
        character = RPGCharacter("John", 1, 20, 10)
        self.assertTrue(character.is_alive())

    def test_is_alive_5(self):
        character = RPGCharacter("John", 10, 20, 10)
        self.assertTrue(character.is_alive())

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
