class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def celsius_to_fahrenheit(self, temperature):
        return ((self.temperature * 9) / 5) + 32

    def fahrenheit_to_celsius(self):
        temperature_f = self.temperature
        fahrenheit_offset = temperature_f - 32
        scaled_value = fahrenheit_offset * 5
        celsius_value = scaled_value / 9
        return celsius_value

    def query(self, weather_list, tmp_units):
        self.weather_list = weather_list
        if self.city not in weather_list:
            return False
        else:
            self.temperature = self.weather_list[self.city]['temperature']
            self.weather = self.weather_list[self.city]['weather']
            if self.weather_list[self.city]['temperature units'] == tmp_units:
                return self.temperature, self.weather
            elif self.weather_list[self.city]['temperature units'] != tmp_units and tmp_units == 'celsius':
                return self.fahrenheit_to_celsius(), self.weather
            elif self.weather_list[self.city]['temperature units'] != tmp_units and tmp_units == 'fahrenheit':
                return self.celsius_to_fahrenheit(self.temperature), self.weather
            else:
                return None

    def set_city(self, city):
        self.city = city

import unittest

class WeatherSystemTestCelsiusToFahrenheit(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 27
        self.assertEqual(weatherSystem.celsius_to_fahrenheit(), 80.6)

    def test_celsius_to_fahrenheit_2(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 23
        self.assertEqual(weatherSystem.celsius_to_fahrenheit(), 73.4)

    def test_celsius_to_fahrenheit_3(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 23
        self.assertNotEqual(weatherSystem.celsius_to_fahrenheit(), 80.6)

    def test_celsius_to_fahrenheit_4(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 27
        self.assertNotEqual(weatherSystem.celsius_to_fahrenheit(), 73.4)

    def test_celsius_to_fahrenheit_5(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 27
        self.assertNotEqual(weatherSystem.celsius_to_fahrenheit(), 23)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
