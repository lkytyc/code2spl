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
