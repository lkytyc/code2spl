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
