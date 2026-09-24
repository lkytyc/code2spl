class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def query(self, weather_list, tmp_units='celsius'):
        self.weather_list = weather_list
        if self.city not in self.weather_list:
            return False

        self.temperature = self.weather_list[self.city]['temperature']
        self.weather = self.weather_list[self.city]['weather']
        stored_units = self.weather_list[self.city]['temperature units']

        if stored_units == tmp_units:
            return (self.temperature, self.weather)

        if tmp_units == 'celsius':
            return (self.fahrenheit_to_celsius(), self.weather)

        if tmp_units == 'fahrenheit':
            return (self.celsius_to_fahrenheit(), self.weather)

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self):
        temperature_celsius = self.temperature
        scaled_temperature = temperature_celsius * 9 / 5
        result = scaled_temperature + 32
        return result

    def fahrenheit_to_celsius(self):
        temperature_fahrenheit = self.temperature
        fahrenheit_offset = temperature_fahrenheit - 32
        celsius_value = fahrenheit_offset * 5 / 9
        return celsius_value

import unittest

class WeatherSystemTestFahrenheitToCelsius(unittest.TestCase):
    def test_fahrenheit_to_celsius(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 80.6
        self.assertEqual(weatherSystem.fahrenheit_to_celsius(), 26.999999999999996)

    def test_fahrenheit_to_celsius_2(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 73.4
        self.assertEqual(weatherSystem.fahrenheit_to_celsius(), 23.000000000000004)

    def test_fahrenheit_to_celsius_3(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 80
        self.assertNotEqual(weatherSystem.fahrenheit_to_celsius(), 23)

    def test_fahrenheit_to_celsius_4(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 73
        self.assertNotEqual(weatherSystem.fahrenheit_to_celsius(), 27)

    def test_fahrenheit_to_celsius_5(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.temperature = 80
        self.assertNotEqual(weatherSystem.fahrenheit_to_celsius(), 27)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
