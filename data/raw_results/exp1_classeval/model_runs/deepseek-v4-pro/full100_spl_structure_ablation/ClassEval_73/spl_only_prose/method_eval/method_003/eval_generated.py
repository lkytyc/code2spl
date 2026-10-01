class RPGCharacter:
    def __init__(self, name: str, hp: float, attack_power: float, defense: float, level: int = 1):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.level = level
        self.exp = 0

    def attack(self, other_character: 'RPGCharacter') -> None:
        damage = max(self.attack_power - other_character.defense, 1)
        other_character.hp -= damage

    def gain_exp(self, amount: int) -> None:
        while amount != 0:
            needed = self.level * 100 - self.exp
            if amount >= needed:
                amount -= needed
                self.level_up()
            else:
                self.exp += amount
                amount = 0

    def heal(self) -> float:
        self.hp += 10
        if self.hp > 100:
            self.hp = 100
        return self.hp

    def is_alive(self) -> bool:
        return self.hp > 0

    def level_up(self) -> tuple:
        can_level_up = self.level < 100
        if can_level_up:
            self.level += 1
            self.exp = 0
            self.hp += 20
            self.attack_power += 5
            self.defense += 5
        return (self.level, self.hp, self.attack_power, self.defense)

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
