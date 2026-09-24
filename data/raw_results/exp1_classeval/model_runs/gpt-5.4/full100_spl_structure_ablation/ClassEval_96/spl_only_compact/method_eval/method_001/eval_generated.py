class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

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

    def query(self, weather_list, tmp_units):
        self.weather_list = weather_list
        city_missing = self.city not in weather_list
        if city_missing:
            return False

        self.temperature = self.weather_list[self.city]['temperature']
        self.weather = self.weather_list[self.city]['weather']
        units_differ = self.weather_list[self.city]['temperature units'] != tmp_units

        if not units_differ:
            return (self.temperature, self.weather)

        if tmp_units == 'celsius':
            converted_temperature = self.fahrenheit_to_celsius()
            return (converted_temperature, self.weather)

        if tmp_units == 'fahrenheit':
            converted_temperature = self.celsius_to_fahrenheit()
            return (converted_temperature, self.weather)

    def set_city(self, city):
        self.city = city

import unittest

class WeatherSystemTestSetCity(unittest.TestCase):
    def test_set_city(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Beijing')
        self.assertEqual(weatherSystem.city, 'Beijing')

    def test_set_city_2(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertEqual(weatherSystem.city, 'Shanghai')

    def test_set_city_3(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'Beijing')

    def test_set_city_4(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'New York')

    def test_set_city_5(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'Tokyo')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
