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
