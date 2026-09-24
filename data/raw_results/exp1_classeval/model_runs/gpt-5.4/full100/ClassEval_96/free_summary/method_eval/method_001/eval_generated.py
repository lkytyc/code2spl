class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self):
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self):
        return (self.temperature - 32) * 5 / 9

    def query(self, weather_list, tmp_units='celsius'):
        self.weather_list = weather_list
        if self.city not in self.weather_list:
            return False

        city_data = self.weather_list[self.city]
        self.temperature = city_data.get('temperature')
        self.weather = city_data.get('weather')

        city_units = city_data.get('tmp_units', 'celsius')

        if city_units == tmp_units:
            return (self.temperature, self.weather)

        if city_units == 'celsius' and tmp_units == 'fahrenheit':
            return (self.celsius_to_fahrenheit(), self.weather)

        if city_units == 'fahrenheit' and tmp_units == 'celsius':
            return (self.fahrenheit_to_celsius(), self.weather)

        return (self.temperature, self.weather)

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
