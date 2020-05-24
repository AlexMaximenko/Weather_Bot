import pyowm
from config import OWM_TOKEN
from datetime import datetime
from datetime import date

owm = pyowm.OWM(OWM_TOKEN, language='ru')

months = {1: 'Январь',
          2: 'Февраль',
          3: 'Март',
          4: 'Апрель',
          5: 'Май',
          6: 'Июнь',
          7: 'Июль',
          8: 'Август',
          9: 'Сентябрь',
          10: 'Октябрь',
          11: 'Ноябрь',
          12: 'Декабрь'}

def get_weather(city):
    observation = owm.weather_at_place(city)
    weather = observation.get_weather()
    temperature = "%.1f"%(weather.get_temperature('celsius')["temp"])
    wind = "%.1f"%(weather.get_wind()['speed'])
    clouds = weather.get_clouds()
    humidity = weather.get_humidity()
    weather = f"В городе {city} сейчас {weather.get_detailed_status()}, \n🌡️ {temperature} °C \n💨 {wind} m/s \n🌫️ {clouds} % \n💦 {humidity} %"
    return weather

def get_forecast(city, days):
    observation = owm.weather_at_place(city)
    forecast = owm.three_hours_forecast(city).get_forecast()
    today = date.today()
    start_date = date(today.year, today.month, today.day + days)
    finish_date = date(today.year, today.month, today.day + days + 1)
    answer = ''

    for weather in forecast:
        ref_date = weather.get_reference_time('date').date()
        ref_time = weather.get_reference_time('date').time()
        if ref_date < start_date or ref_date >= finish_date:
            continue
        temperature = "%.1f"%(weather.get_temperature('celsius')["temp"])
        wind = "%.1f"%(weather.get_wind()['speed'])
        answer += f'В {ref_time.strftime("%H:%M")} будет {weather.get_detailed_status()},🌡️ = {temperature} °C, 💨 {wind} m/s \n\n'

    return answer
