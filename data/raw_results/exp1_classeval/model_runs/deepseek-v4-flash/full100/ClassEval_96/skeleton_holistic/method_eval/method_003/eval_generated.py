class WeatherSystem:
    def __init__(self, city) -> None:
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def query(self, weather_list, tmp_units = 'celsius'):
        if self.city not in weather_list:
            return False

        self.weather_list = weather_list
        city_data = self.weather_list[self.city]
        self.temperature = city_data["temperature"]
        self.weather = city_data["weather"]

        current_units = str(city_data.get("temperature units", "celsius")).lower()
        tmp_units = tmp_units.lower() if isinstance(tmp_units, str) else "celsius"

        if current_units == "celsius" and tmp_units == "fahrenheit":
            self.temperature = self.celsius_to_fahrenheit()
        elif current_units == "fahrenheit" and tmp_units == "celsius":
            self.temperature = self.fahrenheit_to_celsius()

        return self.temperature, self.weather

    def set_city(self, city):
        self.city = city

    def celsius_to_fahrenheit(self):
        return self.temperature * 9 / 5 + 32

    def fahrenheit_to_celsius(self):
        return (self.temperature - 32) * 5 / 9

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
