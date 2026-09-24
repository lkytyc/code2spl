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
