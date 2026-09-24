class RPGCharacter:
    MAX_LEVEL = 100
    MAX_HP = 100
    HEAL_AMOUNT = 10
    HP_PER_LEVEL = 10
    ATTACK_PER_LEVEL = 2
    DEFENSE_PER_LEVEL = 1

    def __init__(self, name, hit_points=100, attack_power=10, defense=5):
        self.name = name
        self.hit_points = min(hit_points, self.MAX_HP)
        self.attack_power = attack_power
        self.defense = defense
        self.level = 1
        self.experience = 0

    def attack(self, other):
        damage = self.attack_power - other.defense
        if damage < 1:
            damage = 1
        other.hit_points -= damage

    def heal(self):
        self.hit_points = min(self.hit_points + self.HEAL_AMOUNT, self.MAX_HP)

    def gain_exp(self, amount):
        self.experience += amount
        while self.level < self.MAX_LEVEL and self.experience >= self._exp_to_next_level():
            self.experience -= self._exp_to_next_level()
            self.level += 1
            self.hit_points = min(self.hit_points + self.HP_PER_LEVEL, self.MAX_HP)
            self.attack_power += self.ATTACK_PER_LEVEL
            self.defense += self.DEFENSE_PER_LEVEL

    def _exp_to_next_level(self):
        return self.level * 100

    def is_alive(self):
        return self.hit_points > 0

import unittest

class RPGCharacterTestLevelUp(unittest.TestCase):
    def test_level_up_1(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.level_up()
        self.assertEqual(character.level, 2)
        self.assertEqual(character.exp, 0)
        self.assertEqual(character.hp, 120)
        self.assertEqual(character.attack_power, 25)
        self.assertEqual(character.defense, 15)

    # full level
    def test_level_up_2(self):
        character = RPGCharacter("John", 100, 20, 10, 100)
        character.level_up()
        self.assertEqual(character.level, 100)
        self.assertEqual(character.exp, 0)
        self.assertEqual(character.hp, 100)
        self.assertEqual(character.attack_power, 20)
        self.assertEqual(character.defense, 10)

    def test_level_up_3(self):
        character = RPGCharacter("John", 100, 20, 10, 2)
        character.level_up()
        self.assertEqual(character.level, 3)
        self.assertEqual(character.exp, 0)
        self.assertEqual(character.hp, 120)
        self.assertEqual(character.attack_power, 25)
        self.assertEqual(character.defense, 15)

    def test_level_up_4(self):
        character = RPGCharacter("John", 100, 20, 10, 3)
        character.level_up()
        self.assertEqual(character.level, 4)
        self.assertEqual(character.exp, 0)
        self.assertEqual(character.hp, 120)
        self.assertEqual(character.attack_power, 25)
        self.assertEqual(character.defense, 15)

    def test_level_up_5(self):
        character = RPGCharacter("John", 100, 20, 10, 4)
        character.level_up()
        self.assertEqual(character.level, 5)
        self.assertEqual(character.exp, 0)
        self.assertEqual(character.hp, 120)
        self.assertEqual(character.attack_power, 25)
        self.assertEqual(character.defense, 15)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
