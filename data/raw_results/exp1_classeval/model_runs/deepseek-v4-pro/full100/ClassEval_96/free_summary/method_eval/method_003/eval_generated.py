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
