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

class RPGCharacterTestHeal(unittest.TestCase):
    def test_heal_1(self):
        character = RPGCharacter("John", 90, 20, 10)
        character.heal()
        self.assertEqual(character.hp, 100)

    # overflow healing 
    def test_heal_2(self):
        character = RPGCharacter("John", 97, 20, 10)
        character.heal()
        self.assertEqual(character.hp, 100)

    def test_heal_3(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.heal()
        self.assertEqual(character.hp, 100)

    def test_heal_4(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.hp = 50
        character.heal()
        self.assertEqual(character.hp, 60)

    def test_heal_5(self):
        character = RPGCharacter("John", 100, 20, 10)
        character.hp = 10
        character.heal()
        self.assertEqual(character.hp, 20)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
