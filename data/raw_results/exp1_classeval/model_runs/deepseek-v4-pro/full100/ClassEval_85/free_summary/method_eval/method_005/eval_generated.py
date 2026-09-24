class Thermostat:
    def __init__(self, current_temp, target_temp, mode):
        self.current_temp = current_temp
        self.target_temp = target_temp
        self.mode = mode

    def get_target_temp(self):
        return self.target_temp

    def set_target_temp(self, temp):
        self.target_temp = temp

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        if mode in ("heat", "cool"):
            self.mode = mode
            return True
        return False

    def auto_set_mode(self):
        if self.current_temp < self.target_temp:
            self.mode = "heat"
        else:
            self.mode = "cool"

    def auto_check_conflict(self):
        if self.current_temp < self.target_temp:
            needed = "heat"
        else:
            needed = "cool"
        if self.mode != needed:
            self.mode = needed
            return True
        return False

    def simulate_operation(self):
        self.auto_set_mode()
        steps = 0
        if self.mode == "heat":
            while self.current_temp < self.target_temp:
                self.current_temp += 1
                steps += 1
        else:
            while self.current_temp > self.target_temp:
                self.current_temp -= 1
                steps += 1
        return steps

import unittest

class ThermostatTestAutoCheckConflict(unittest.TestCase):
    def test_auto_check_conflict_1(self):
        t = Thermostat(30, 25, 'cool')
        self.assertTrue(t.auto_check_conflict())

    def test_auto_check_conflict_2(self):
        t = Thermostat(30, 25, 'heat')
        self.assertFalse(t.auto_check_conflict())
        self.assertEqual(t.mode, 'cool')

    def test_auto_check_conflict_3(self):
        t = Thermostat(25, 30, 'heat')
        self.assertTrue(t.auto_check_conflict())

    def test_auto_check_conflict_4(self):
        t = Thermostat(25, 30, 'cool')
        self.assertFalse(t.auto_check_conflict())
        self.assertEqual(t.mode, 'heat')

    def test_auto_check_conflict_5(self):
        t = Thermostat(25, 25, 'cool')
        self.assertFalse(t.auto_check_conflict())
        self.assertEqual(t.mode, 'cool')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
