class WeatherSystem:
    def __init__(self, city):
        self.city = city
        self.temperature = None
        self.weather = None
        self.weather_list = {}

    def query(self, weather_list, tmp_units='celsius'):
        self.weather_list = weather_list

        if self.city not in weather_list:
            return False

        city_data = weather_list[self.city]
        self.temperature = city_data['temperature']
        self.weather = city_data['weather']
        stored_units = city_data['temperature units']

        if stored_units != tmp_units:
            if stored_units == 'fahrenheit' and tmp_units == 'celsius':
                converted = self.fahrenheit_to_celsius()
                return (converted, self.weather)
            elif stored_units == 'celsius' and tmp_units == 'fahrenheit':
                converted = self.celsius_to_fahrenheit()
                return (converted, self.weather)
        else:
            return (self.temperature, self.weather)

    def celsius_to_fahrenheit(self):
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self):
        return (self.temperature - 32) * 5 / 9

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
