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
            self.temperature = None
            self.weather = None
            return None, None

        info = weather_list[self.city]
        self.weather = info.get('weather')
        self.temperature = info.get('temperature')
        current_units = info.get('temperature units', 'celsius')

        target_units = tmp_units.lower() if isinstance(tmp_units, str) else tmp_units
        current_units = current_units.lower() if isinstance(current_units, str) else current_units

        if target_units == current_units or target_units is None:
            return self.temperature, self.weather

        if current_units == 'celsius' and target_units == 'fahrenheit':
            self.temperature = self.celsius_to_fahrenheit()
        elif current_units == 'fahrenheit' and target_units == 'celsius':
            self.temperature = self.fahrenheit_to_celsius()

        return self.temperature, self.weather

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
        if self.temperature is None:
            return None
        return self.temperature * 9 / 5 + 32

    def fahrenheit_to_celsius(self):
        """
        Convert the temperature from Fahrenheit to Celsius.
        :return: the temperature in Celsius, float.
        """
        if self.temperature is None:
            return None
        return (self.temperature - 32) * 5 / 9

import unittest

class WeatherSystemTestSetCity(unittest.TestCase):
    def test_set_city(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Beijing')
        self.assertEqual(weatherSystem.city, 'Beijing')

    def test_set_city_2(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertEqual(weatherSystem.city, 'Shanghai')

    def test_set_city_3(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'Beijing')

    def test_set_city_4(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'New York')

    def test_set_city_5(self):
        weatherSystem = WeatherSystem('New York')
        weatherSystem.set_city('Shanghai')
        self.assertNotEqual(weatherSystem.city, 'Tokyo')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
