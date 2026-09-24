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

class ThermostatTestSimulateOperation(unittest.TestCase):
    def test_simulate_operation_1(self):
        t = Thermostat(20, 25, 'heat')
        self.assertEqual(t.simulate_operation(), 5)
        self.assertEqual(t.get_mode(), 'heat')
        self.assertEqual(t.current_temperature, 25)

    def test_simulate_operation_2(self):
        t = Thermostat(25.7, 20, 'cool')
        self.assertEqual(t.simulate_operation(), 6)
        self.assertEqual(t.get_mode(), 'cool')
        self.assertEqual(t.current_temperature, 19.7)

    def test_simulate_operation_3(self):
        t = Thermostat(25, 25, 'heat')
        self.assertEqual(t.simulate_operation(), 0)
        self.assertEqual(t.get_mode(), 'cool')
        self.assertEqual(t.current_temperature, 25)

    def test_simulate_operation_4(self):
        t = Thermostat(25, 25, 'cool')
        self.assertEqual(t.simulate_operation(), 0)
        self.assertEqual(t.get_mode(), 'cool')
        self.assertEqual(t.current_temperature, 25)

    def test_simulate_operation_5(self):
        t = Thermostat(25, 25, 'test')
        self.assertEqual(t.simulate_operation(), 0)
        self.assertEqual(t.get_mode(), 'cool')
        self.assertEqual(t.current_temperature, 25)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
