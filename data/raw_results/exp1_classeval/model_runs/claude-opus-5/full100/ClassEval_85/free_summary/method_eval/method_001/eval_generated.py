import time


class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode):
        self.current_temperature = current_temperature
        self._target_temperature = target_temperature
        self._mode = mode

    def get_target_temperature(self):
        return self._target_temperature

    def set_target_temperature(self, value):
        self._target_temperature = value

    def get_mode(self):
        return self._mode

    def set_mode(self, value):
        if value not in ('heat', 'cool'):
            return False
        self._mode = value

    def auto_set_mode(self):
        if self.current_temperature < self._target_temperature:
            self._mode = 'heat'
        else:
            self._mode = 'cool'

    def auto_check_conflict(self):
        conflict = (
            (self._mode == 'heat' and self.current_temperature > self._target_temperature) or
            (self._mode == 'cool' and self.current_temperature < self._target_temperature)
        )
        if conflict:
            return True
        self.auto_set_mode()
        return False

    def simulate_operation(self):
        self.auto_set_mode()
        steps = 0
        while self.current_temperature != self._target_temperature:
            if self._mode == 'heat':
                self.current_temperature += 1
            else:
                self.current_temperature -= 1
            steps += 1
        return steps

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
