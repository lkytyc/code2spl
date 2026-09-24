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
