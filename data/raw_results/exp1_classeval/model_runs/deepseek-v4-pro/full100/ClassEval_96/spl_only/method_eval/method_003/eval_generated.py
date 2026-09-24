class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def query(self, weather_list, tmp_units='celsius'):
        self.weather_list = weather_list
        if self.city not in weather_list:
            return False
        else:
            self.temperature = self.weather_list[self.city]['temperature']
            self.weather = self.weather_list[self.city]['weather']
            if self.weather_list[self.city]['temperature units'] == tmp_units:
                return self.temperature, self.weather
            elif tmp_units == 'celsius':
                return self.fahrenheit_to_celsius(), self.weather
            elif tmp_units == 'fahrenheit':
                return self.celsius_to_fahrenheit(), self.weather
            else:
                return None

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self):
        return ((self.temperature * 9) / 5) + 32

    def fahrenheit_to_celsius(self):
        temperature_f = self.temperature
        fahrenheit_offset = temperature_f - 32
        scaled_value = fahrenheit_offset * 5
        celsius_value = scaled_value / 9
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
