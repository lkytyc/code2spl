class WeatherSystem:
    def __init__(self, city):
        self.city = city
        self.temperature = None
        self.weather_condition = None
        self.weather_data = {}

    def query(self, weather_data, temperature_unit='Celsius'):
        if self.city not in weather_data:
            return False
        city_data = weather_data[self.city]
        self.temperature = city_data['temperature']
        self.weather_condition = city_data['condition']
        self.weather_data = weather_data
        if city_data.get('unit', 'Celsius') != temperature_unit:
            if temperature_unit == 'Fahrenheit':
                self.temperature = self.celsius_to_fahrenheit(self.temperature)
            elif temperature_unit == 'Celsius':
                self.temperature = self.fahrenheit_to_celsius(self.temperature)
        return self.temperature, self.weather_condition

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5/9

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
