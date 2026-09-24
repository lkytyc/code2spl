class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = mode

    def auto_check_conflict(self):
        if self.current_temperature > self.target_temperature:
            if self.mode == 'cool':
                return True
            self.auto_set_mode()
            return False
        else:
            if self.mode == 'heat':
                return True
            self.auto_set_mode()
            return False

    def auto_set_mode(self):
        if self.current_temperature < self.target_temperature:
            self.mode = 'heat'
        else:
            self.mode = 'cool'

    def get_mode(self):
        return self.mode

    def get_target_temperature(self):
        return self.target_temperature

    def set_mode(self, mode):
        if mode in ('heat', 'cool'):
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

class ThermostatTestSetTargetTemperature(unittest.TestCase):
    def test_set_target_temperature_1(self):
        t = Thermostat(20, 25, 'heat')
        t.set_target_temperature(30)
        self.assertEqual(t.get_target_temperature(), 30)

    def test_set_target_temperature_2(self):
        t = Thermostat(20, 25, 'cool')
        t.set_target_temperature(10)
        self.assertEqual(t.get_target_temperature(), 10)

    def test_set_target_temperature_3(self):
        t = Thermostat(20, 25, 'test')
        t.set_target_temperature(10)
        self.assertEqual(t.get_target_temperature(), 10)

    def test_set_target_temperature_4(self):
        t = Thermostat(25, 25, 'cool')
        t.set_target_temperature(10)
        self.assertEqual(t.get_target_temperature(), 10)

    def test_set_target_temperature_5(self):
        t = Thermostat(25, 25, 'heat')
        t.set_target_temperature(10)
        self.assertEqual(t.get_target_temperature(), 10)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
