import json
from textwrap import indent
from openai import OpenAI
import config
import requests

TOKEN = config.weatherapi_token


BASE_URL = 'http://api.weatherapi.com/v1/'
current_json = 'current.json'
forecast_json = 'forecast.json'
def get_weather_text(region: str, city: str = ''):
    query = {'key': TOKEN, 'q': f'{region}, {city}', 'lang': 'ru' }
    weather = requests.get(f'{BASE_URL}{current_json}', params= query)
    location_current = weather.json()
    current = location_current['current']
    wind = round(int(current['wind_kph']) / 3.6, 1)
    temp = current['temp_c']
    pressure = round(current['pressure_mb'])
    condition = current['condition']
    icon = condition['icon']
    text = condition['text']
    weather = f'Сегодня \n{text} \nТемпература {temp}c°, Ветер {wind} м/с, Давление {pressure}р.с'
    return weather


def get_weather_icon(region: str, city: str = ''):
    query = {'key': TOKEN, 'q':  f'{region}, {city}', 'lang': 'ru' }
    weather = requests.get(f'{BASE_URL}{current_json}', params= query)
    # location_current = json.dumps(weather.json(), indent=4, ensure_ascii=False, sort_keys=True)
    location_current = weather.json()
    current = location_current['current']
    condition = current['condition']
    icon = condition['icon']
    icon = str(icon)
    return icon


def get_weather_forecast(region: str, city: str = ''):
    query = {'key': TOKEN, 'q': f'{region}, {city}', 'lang': 'ru','days': '7' }
    weather = requests.get(f'{BASE_URL}{forecast_json}', params= query)
    info = weather.json()
    forecast = info['forecast']
    message = 'Прогноз на семь дней:'
    for forecastday in forecast['forecastday']:
        avg_day = forecastday['day']
        condition = avg_day['condition']
        date = forecastday['date']
        avgtemp = avg_day['avgtemp_c']
        max_wind = round(int(avg_day['maxwind_kph']) / 3.6, 1)
        text = condition['text']
        message += (f'\n---------\n{date}\n{text}, температура - {avgtemp}c°, ветер - {max_wind} m/c')
    return message

def get_weather_name(region: str, city: str = ''):
    query = {'key': TOKEN, 'q': f'{region}, {city}', 'lang': 'ru' }
    weather = requests.get(f'{BASE_URL}{current_json}', params= query)
    location_current = weather.json()
    location = location_current['location']
    country = location['country']
    region = location['region']
    name = location['name']
    result = f'{country}, {region}, {name}'
    return result


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= config.neiro_token,
)
def finding_sity(prompt: str):
  completion = client.chat.completions.create(
    extra_headers={
      "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
      "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-chat:free",
    messages=[
      {
        "role": "user",
        "content": f'Ты должен обработать ввод пользователя, который будет вставлен в переменную и отправлен в качестве запроса для api который выдает прогноз погоды. Пользователь произвольно введет регион и  населенный пункт. Твоя задача по-английски ответить в формате "Region, City" Пользователь ввел: {prompt}'
      }
    ]
  )
  result = completion.choices[0].message.content
  return result


def translating_city(prompt: str):
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="deepseek/deepseek-chat:free",
        messages=[
            {
                "role": "user",
                "content": f'Ты должен обработать вывод от api для погоды в читаемый для пользователя вид. Строка будет нести информацию о населенном пункте на английском языке, просто переведи ее на русский. Вот строчка: {prompt}'
            }
        ]
    )
    result = completion.choices[0].message.content
    return result



