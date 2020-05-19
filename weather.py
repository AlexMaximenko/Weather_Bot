import pyowm
from config import OWM_TOKEN

owm = pyowm.OWM(OWM_TOKEN)

def get_weather(city):
    observation = owm.weather_at_place(city)
    weather = observation.get_weather()
    temperature = weather.get_temperature('celsius')["temp"]
    wind = weather.get_wind()['speed']
    clouds = weather.get_clouds()
    humidity = weather.get_humidity()
    weather = f"В городе {city} сейчас {weather.get_detailed_status()} \nТемпература: {temperature} °C \nВетер: {wind} m/s \nОблачность: {clouds} % \nВлажность: {humidity} %"
    return weather
