class WeatherSystem:
    def __init__(self, city):
        self.city = city
        self.temperature = None
        self.weather = None
        self.weather_data = {}

    def query(self, weather_dict, target_unit='Celsius'):
        if self.city not in weather_dict:
            return False
        data = weather_dict[self.city]
        self.temperature = data['temperature']
        self.weather = data['condition']
        self.weather_data = data
        unit = data.get('unit', 'Celsius')
        if target_unit == 'Fahrenheit':
            if unit == 'Celsius':
                temp = self.celsius_to_fahrenheit(self.temperature)
            else:
                temp = self.temperature
        elif target_unit == 'Celsius':
            if unit == 'Fahrenheit':
                temp = self.fahrenheit_to_celsius(self.temperature)
            else:
                temp = self.temperature
        else:
            temp = self.temperature
        return (temp, self.weather)

    def change_city(self, new_city):
        self.city = new_city

    def celsius_to_fahrenheit(self, celsius):
        return celsius * 9/5 + 32

    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5/9

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
