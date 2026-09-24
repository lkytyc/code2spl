class WeatherSystem:
    def __init__(self, city):
        self.temperature = None
        self.weather = None
        self.city = city
        self.weather_list = {}

    def celsius_to_fahrenheit(self):
        celsius_value = self.temperature
        scaled_value = (celsius_value * 9) / 5
        fahrenheit_value = scaled_value + 32
        return fahrenheit_value

    def fahrenheit_to_celsius(self):
        fahrenheit_value = self.temperature
        shifted_value = fahrenheit_value - 32
        celsius_value = shifted_value * (5 / 9)
        return celsius_value

    def query(self, weather_list, tmp_units):
        self.weather_list = weather_list
        if self.city not in weather_list:
            return False
        self.temperature = self.weather_list[self.city]['temperature']
        self.weather = self.weather_list[self.city]['weather']
        if self.weather_list[self.city]['temperature units'] == tmp_units:
            return (self.temperature, self.weather)
        elif self.weather_list[self.city]['temperature units'] == 'fahrenheit' and tmp_units == 'celsius':
            return (self.fahrenheit_to_celsius(), self.weather)
        elif self.weather_list[self.city]['temperature units'] == 'celsius' and tmp_units == 'fahrenheit':
            return (self.celsius_to_fahrenheit(), self.weather)

    def set_city(self, city):
        self.city = city

import unittest

class WeatherSystemTestQuery(unittest.TestCase):
    def test_query(self):
        weatherSystem = WeatherSystem('New York')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 27,
                'temperature units': 'celsius'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 23,
                'temperature units': 'celsius'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list), (27, 'sunny'))

    def test_query_2(self):
        weatherSystem = WeatherSystem('Shanghai')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 27,
                'temperature units': 'celsius'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 23,
                'temperature units': 'celsius'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list), False)

    def test_query_3(self):
        weatherSystem = WeatherSystem('Beijing')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 27,
                'temperature units': 'celsius'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 23,
                'temperature units': 'celsius'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list, 'fahrenheit'), (73.4, 'cloudy'))

    def test_query_4(self):
        weatherSystem = WeatherSystem('Beijing')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 73.47,
                'temperature units': 'fahrenheit'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 73.4,
                'temperature units': 'fahrenheit'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list, 'celsius'), (23.000000000000004, 'cloudy'))

    def test_query_5(self):
        weatherSystem = WeatherSystem('New York')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 80.6,
                'temperature units': 'fahrenheit'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 23,
                'temperature units': 'celsius'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list, tmp_units='celsius'), (26.999999999999996, 'sunny'))

    def test_query_6(self):
        weatherSystem = WeatherSystem('New York')
        weather_list = {
            'New York': {
                'weather': 'sunny',
                'temperature': 27,
                'temperature units': 'celsius'
            },
            'Beijing': {
                'weather': 'cloudy',
                'temperature': 23,
                'temperature units': 'celsius'
            }
        }
        self.assertEqual(weatherSystem.query(weather_list, tmp_units='fahrenheit'), (80.6, 'sunny'))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
