class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def auto_check_conflict(self):
        temperature_is_above_target = self.current_temperature > self.target_temperature
        if temperature_is_above_target:
            cooling_branch_result = self.mode == 'cool'
            if cooling_branch_result:
                return True
            self.auto_set_mode()
            return False
        heating_branch_result = self.mode == 'heat'
        if heating_branch_result:
            return True
        self.auto_set_mode()
        return False

    def auto_set_mode(self):
        temperature_comparison = self.current_temperature < self.target_temperature
        if temperature_comparison:
            self.mode = 'heat'
        else:
            self.mode = 'cool'

    def get_mode(self):
        result = self.mode
        return result

    def get_target_temperature(self):
        return self.target_temperature

    def set_mode(self, mode):
        mode_validity = mode in ('heat', 'cool')
        if mode_validity:
            self.mode = mode
        else:
            return False

    def set_target_temperature(self, temperature):
        self.target_temperature = temperature

    def simulate_operation(self):
        self.auto_set_mode()
        use_time = 0
        if self.mode == 'heat':
            while self.current_temperature < self.target_temperature:
                self.current_temperature += 1
                use_time += 1
        else:
            while self.current_temperature > self.target_temperature:
                self.current_temperature -= 1
                use_time += 1
        return use_time

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
