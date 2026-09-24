class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def get_target_temperature(self):
        return self.target_temperature

    def set_target_temperature(self, target_temperature):
        self.target_temperature = target_temperature

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        if mode not in ("heat", "cool"):
            return False
        self.mode = mode
        return True

    def choose_mode_automatically(self):
        if self.current_temperature < self.target_temperature:
            self.mode = "heat"
        else:
            self.mode = "cool"

    def check_conflict(self):
        if self.current_temperature > self.target_temperature:
            if self.mode == "cool":
                return True
            self.mode = "cool"
            return False
        else:
            if self.mode == "heat":
                return True
            self.mode = "heat"
            return False

    def simulate_operation(self):
        self.choose_mode_automatically()
        steps = 0

        if self.mode == "heat":
            while self.current_temperature < self.target_temperature:
                self.current_temperature += 1
                steps += 1
        else:
            while self.current_temperature > self.target_temperature:
                self.current_temperature -= 1
                steps += 1

        return steps

import unittest

class ThermostatTestSetMode(unittest.TestCase):
    def test_set_mode_1(self):
        t = Thermostat(20, 25, 'heat')
        t.set_mode('cool')
        self.assertEqual(t.get_mode(), 'cool')

    # use mode that not in ['heat', 'cool']
    def test_set_mode_2(self):
        t = Thermostat(20, 25, 'heat')
        self.assertFalse(t.set_mode('test'))

    def test_set_mode_3(self):
        t = Thermostat(20, 25, 'cool')
        t.set_mode('heat')
        self.assertEqual(t.get_mode(), 'heat')

    def test_set_mode_4(self):
        t = Thermostat(20, 25, 'test')
        t.set_mode('heat')
        self.assertEqual(t.get_mode(), 'heat')

    def test_set_mode_5(self):
        t = Thermostat(25, 25, 'cool')
        t.set_mode('heat')
        self.assertEqual(t.get_mode(), 'heat')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
