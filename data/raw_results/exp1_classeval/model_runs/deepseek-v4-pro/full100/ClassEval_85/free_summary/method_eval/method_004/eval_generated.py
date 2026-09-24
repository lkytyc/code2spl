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

class ThermostatTestAutoSetMode(unittest.TestCase):
    def test_auto_set_mode_1(self):
        t = Thermostat(20, 25, 'heat')
        t.auto_set_mode()
        self.assertEqual(t.get_mode(), 'heat')

    def test_auto_set_mode_2(self):
        t = Thermostat(25, 20, 'heat')
        t.auto_set_mode()
        self.assertEqual(t.get_mode(), 'cool')

    def test_auto_set_mode_3(self):
        t = Thermostat(25, 20, 'cool')
        t.auto_set_mode()
        self.assertEqual(t.get_mode(), 'cool')

    def test_auto_set_mode_4(self):
        t = Thermostat(20, 25, 'cool')
        t.auto_set_mode()
        self.assertEqual(t.get_mode(), 'heat')

    def test_auto_set_mode_5(self):
        t = Thermostat(25, 25, 'cool')
        t.auto_set_mode()
        self.assertEqual(t.get_mode(), 'cool')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
