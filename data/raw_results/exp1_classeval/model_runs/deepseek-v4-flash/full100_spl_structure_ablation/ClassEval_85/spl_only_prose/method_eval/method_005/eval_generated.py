class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def auto_check_conflict(self):
        temperature_above_target = self.current_temperature > self.target_temperature
        if temperature_above_target:
            mode_is_cool = self.mode == 'cool'
            if mode_is_cool:
                return True
            else:
                self.auto_set_mode()
                return False
        else:
            mode_is_heat = self.mode == 'heat'
            if mode_is_heat:
                return True
            else:
                self.auto_set_mode()
                return False

    def auto_set_mode(self):
        is_below_target = self.current_temperature < self.target_temperature
        if is_below_target:
            self.mode = 'heat'
        else:
            self.mode = 'cool'

    def get_mode(self):
        return self.mode

    def get_target_temperature(self):
        return self.target_temperature

    def set_mode(self, mode):
        is_valid_mode = mode in ['heat', 'cool']
        if is_valid_mode:
            self.mode = mode
            return None
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
