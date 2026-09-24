class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self):
        self.temperature = (self.temperature * 9 / 5) + 32
        return self.temperature

    def fahrenheit_to_celsius(self):
        self.temperature = (self.temperature - 32) * 5 / 9
        return self.temperature

    def query(self, weather_list, tmp_units='celsius'):
        self.weather_list = weather_list
        if self.city not in self.weather_list:
            return False

        data = self.weather_list[self.city]
        self.temperature = data['temperature']
        self.weather = data['weather']
        stored_units = data['temperature units']

        if stored_units != tmp_units:
            if tmp_units == 'celsius':
                self.fahrenheit_to_celsius()
            elif tmp_units == 'fahrenheit':
                self.celsius_to_fahrenheit()

        return self.temperature, self.weather

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
