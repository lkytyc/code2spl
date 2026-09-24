class WeatherSystem:
    def __init__(self, city: object) -> None:
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def celsius_to_fahrenheit(self) -> float:
        temp_times_9 = self.temperature * 9
        temp_after_division = temp_times_9 / 5
        fahrenheit_result = temp_after_division + 32
        return fahrenheit_result

    def fahrenheit_to_celsius(self) -> float:
        temperature = self.temperature
        fahrenheit_offset = temperature - 32
        scaled_value = fahrenheit_offset * 5
        celsius_value = scaled_value / 9
        return celsius_value

    def query(self, weather_list: dict, tmp_units: str):
        self.weather_list = weather_list
        if self.city not in weather_list:
            return False
        self.temperature = self.weather_list[self.city]['temperature']
        self.weather = self.weather_list[self.city]['weather']
        if self.weather_list[self.city]['temperature units'] == tmp_units:
            return self.temperature, self.weather
        if tmp_units == 'celsius':
            return self.fahrenheit_to_celsius(), self.weather
        if tmp_units == 'fahrenheit':
            return self.celsius_to_fahrenheit(), self.weather
        return None

    def set_city(self, city: any):
        self.city = city

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
