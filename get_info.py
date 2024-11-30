import asyncio
import aiohttp
import sqlite3
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from datetime import datetime, timedelta


# Функция отвечает за запись данных погоды в базу данных
async def data_write(data: list, data_len: int) -> None:
    conn = sqlite3.connect("DataBase/data.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM main') # очищаю базу данных для новых значений данного города
    for i in range(data_len):
        cursor.executemany("""
        INSERT INTO main (Date, T_min, T_max, T_day, T_app, W_speed, Rel_hum)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", [data[i]]) # записываю новые данные
    conn.commit()
    cursor.close()
    conn.close()


async def city_valid(city_name: str) -> bool:
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name, exactly_one=True, addressdetails=True)
    address = location.raw.get("address", {})
    found_name = address.get('city') or address.get('town') or address.get('village')
    if found_name and found_name.lower() == city_name.lower():
        return True
    else:
        return False
    

async def date_valid(start_date: str, end_date: str) -> bool:
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date= datetime.strptime(end_date, "%Y-%m-%d")
        if end_date > datetime.now() or start_date > end_date:
            return False
        else:
            return True
    except ValueError:
        return False


# получает информацию о погоде в городе
async def get_weather(city_name: str, start_day: str, end_day: str) -> None:
    print('все гуд!')
    # geolocator = Nominatim(user_agent="geoapi")
    # link = "https://archive-api.open-meteo.com/v1/archive"
    # location = geolocator.geocode(city_name, exactly_one=True, addressdetails=True)
    # address = location.raw.get("address", {})
    # found_name = address.get('city') or address.get('town') or address.get('village')
    # if found_name.lower() == city_name.lower():
    #     x, y = location.latitude, location.longitude
    #     params = {
    #         "latitude": location.latitude,
    #         "longitude": location.longitude,
    #         "start_date": start_day,
    #         "end_date": end_day,
    #         "daily": ["temperature_2m_max", "temperature_2m_min"], # запрашиваем дневную информацию о максимальной и минимальной температуре
    #         "hourly": ["temperature_2m", "apparent_temperature", 
    #                     "wind_speed_10m", "relative_humidity_2m"], # запрашиваем часовую информацию о действ.температуре, чувств.температуре, скорости ветра и влажности
    #         "timezone": "Europe/Moscow"
    #     }
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(link, params=params) as resp:
    #             output = await resp.json()
    #             data = []
    #             for i in range(31):
    #                 date = output['daily']['time'][i]
    #                 t_min = output['daily']['temperature_2m_min'][i]
    #                 t_max = output['daily']['temperature_2m_max'][i]
    #                 t_day, t_app_day, w_speed_day, rel_humid_day = [], [], [], []
    #                 for j in range(24):
    #                     index = j + i * 24
    #                     day_hour = output['hourly']['time'][index]
    #                     if date in day_hour:
    #                         t_hour = output['hourly']['temperature_2m'][index]
    #                         t_app_hour = output['hourly']['apparent_temperature'][index]
    #                         w_speed_hour = output['hourly']['wind_speed_10m'][index]
    #                         rel_humid_hour = output['hourly']['relative_humidity_2m'][index]
    #                         t_day.append(t_hour)
    #                         t_app_day.append(t_app_hour)
    #                         w_speed_day.append(w_speed_hour)
    #                         rel_humid_day.append(rel_humid_hour)
    #                 data.append([date, t_min, t_max, str(t_day), str(t_app_day), str(w_speed_day), str(rel_humid_day)])
    #             return data
    # else:
    #     return 'Такого города нет'

async def get_info_main(city_name: str, start_day: str, end_day: str) -> bool:
    data = await get_weather(city_name, start_day, end_day)
    return data


if __name__ == "__main__":
    asyncio.run(get_info_main())
