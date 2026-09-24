class Thermostat:
    def __init__(self, current_temperature, target_temperature, mode="heat"):
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature
        self.mode = "heat"
        self.set_mode(mode)

    def get_current_temperature(self):
        return self.current_temperature

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

    def auto_set_mode(self):
        if self.current_temperature < self.target_temperature:
            self.mode = "heat"
        else:
            self.mode = "cool"

    def auto_check_conflict(self):
        if self.mode == "cool" and self.current_temperature > self.target_temperature:
            return True
        if self.mode == "heat" and self.current_temperature <= self.target_temperature:
            return True
        self.auto_set_mode()
        return False

    def simulate_operation(self):
        self.auto_set_mode()
        time_units = 0
        while self.current_temperature != self.target_temperature:
            if self.current_temperature < self.target_temperature:
                self.current_temperature += 1
            else:
                self.current_temperature -= 1
            time_units += 1
        return time_units

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
