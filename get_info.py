import asyncio
import aiohttp
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from pprint import pprint


async def data_write(data, data_len):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    for i in range(data_len):
        cursor.executemany("""
        INSERT INTO main (Date, T_min, T_max, T_day)
        VALUES (?, ?, ?, ?)""", [data[i]])
    conn.commit()
    cursor.close()
    conn.close()


async def get_weather(city):
    geolocator = Nominatim(user_agent="geoapi")
    async with aiohttp.ClientSession() as session:
        link = "https://archive-api.open-meteo.com/v1/archive"
        location = geolocator.geocode(city)
        time_now = datetime.now() - timedelta(days=5)
        time_30_ago = time_now - timedelta(days=30)
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "start_date": time_30_ago.strftime("%Y-%m-%d"),
            "end_date": time_now.strftime("%Y-%m-%d"),
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "hourly": ["temperature_2m"],
            "timezone": "Europe/Moscow"
        }
        async with session.get(link, params=params) as resp:
            output = await resp.json()
            data = []
            for i in range(31):
                date = output['daily']['time'][i]
                t_min = output['daily']['temperature_2m_min'][i]
                t_max = output['daily']['temperature_2m_max'][i]
                t_day = []
                for j in range(24):
                    t_hour = output['hourly']['time'][j + i * 24]
                    if date in t_hour:
                        t_hour = output['hourly']['temperature_2m'][j + i * 24]
                        t_day.append(t_hour)
                data.append([date, t_min, t_max, str(t_day)])
            await data_write(data, len(data))


if __name__ == "__main__":
    asyncio.run(get_weather('Moscow'))