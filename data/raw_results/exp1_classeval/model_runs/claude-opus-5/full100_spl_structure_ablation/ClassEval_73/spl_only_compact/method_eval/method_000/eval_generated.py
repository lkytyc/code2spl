class RPGCharacter:
    def __init__(self, name, hp, attack_power, defense, level=1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other_character):
        damage = self.attack_power - other_character.defense
        if damage < 1:
            damage = 1
        other_character.hp -= damage

    def gain_exp(self, amount):
        while amount != 0:
            if self.exp + amount >= self.level * 100:
                amount -= (self.level * 100 - self.exp)
                self.level_up()
            else:
                self.exp += amount
                amount = 0

    def heal(self):
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def is_alive(self):
        return self.hp > 0

    def level_up(self):
        if self.level < 100:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attack_power += 5
            self.defense += 5
        return (self.level, self.hp, self.attack_power, self.defense)

import unittest

class RPGCharacterTestAttack(unittest.TestCase):
    def test_attack(self):
        character1 = RPGCharacter("John", 100, 20, 10)
        character2 = RPGCharacter("Enemy", 100, 15, 5)
        character1.attack(character2)
        self.assertEqual(character2.hp, 85)

    def test_attack_2(self):
        character1 = RPGCharacter("John", 100, 20, 10)
        character2 = RPGCharacter("Enemy", 100, 15, 5)
        character2.attack(character1)
        self.assertEqual(character1.hp, 95)

    def test_attack_3(self):
        character1 = RPGCharacter("John", 100, 20, 10)
        character2 = RPGCharacter("Enemy", 100, 15, 5)
        character1.attack(character2)
        character2.attack(character1)
        self.assertEqual(character1.hp, 95)
        self.assertEqual(character2.hp, 85)

    def test_attack_4(self):
        character1 = RPGCharacter("John", 100, 20, 10)
        character2 = RPGCharacter("Enemy", 100, 15, 5)
        character1.attack(character2)
        character1.attack(character2)
        self.assertEqual(character2.hp, 70)

    def test_attack_5(self):
        character1 = RPGCharacter("John", 100, 20, 10)
        character2 = RPGCharacter("Enemy", 100, 15, 5)
        character1.attack(character2)
        character1.attack(character2)
        character1.attack(character2)
        self.assertEqual(character2.hp, 55)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
