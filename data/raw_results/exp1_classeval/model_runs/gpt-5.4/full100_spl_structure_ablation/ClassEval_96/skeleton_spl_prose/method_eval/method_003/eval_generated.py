class WeatherSystem:
    """
    This is a class representing a weather system that provides functionality to query weather information for a specific city and convert temperature units between Celsius and Fahrenheit.
    """

    def __init__(self, city) -> None:
        """
        Initialize the weather system with a city name.
        """
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def query(self, weather_list, tmp_units='celsius'):
        """
        Query the weather system for the weather and temperature of the city,and convert the temperature units based on the input parameter.
        :param weather_list: a dictionary of weather information for different cities,dict.
        :param tmp_units: the temperature units to convert to, str.
        :return: the temperature and weather of the city, tuple.
        """
        self.weather_list = weather_list

        if self.city not in weather_list:
            return False

        self.temperature = self.weather_list[self.city]['temperature']
        self.weather = self.weather_list[self.city]['weather']

        units_differ = (
            self.weather_list[self.city]['temperature units'] != tmp_units
        )

        if not units_differ:
            return self.temperature, self.weather

        if tmp_units == 'celsius':
            converted_temperature = self.fahrenheit_to_celsius()
            return converted_temperature, self.weather

        if tmp_units == 'fahrenheit':
            converted_temperature = self.celsius_to_fahrenheit()
            return converted_temperature, self.weather

    def set_city(self, city):
        """
        Set the city of the weather system.
        :param city: the city to set, str.
        :return: None
        """
        self.city = city

    def celsius_to_fahrenheit(self):
        """
        Convert the temperature from Celsius to Fahrenheit.
        :return: the temperature in Fahrenheit, float.
        """
        temperature_celsius = self.temperature
        scaled_temperature = temperature_celsius * 9 / 5
        result = scaled_temperature + 32
        return result

    def fahrenheit_to_celsius(self):
        """
        Convert the temperature from Fahrenheit to Celsius.
        :return: the temperature in Celsius, float.
        """
        temperature_fahrenheit = self.temperature
        fahrenheit_offset = temperature_fahrenheit - 32
        celsius_value = fahrenheit_offset * 5 / 9
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
