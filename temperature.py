import asyncio
import sqlite3
import pandas as pd
from pprint import pprint
from draw import draw


# функция получения информации из базы данных
async def get_data(db_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_name)
    sql_query = """SELECT * FROM main"""
    data = pd.read_sql_query(sql_query, con=conn)
    conn.close()
    return data


# обработчик температурных данных
async def temperature_handler(data: pd.DataFrame) -> None:
    for day in range(len(data)):
        t_day = eval(data['T_day'][day])
        t_min = data['T_min'][day]
        t_max = data['T_max'][day]
        t_app = eval(data['T_app'][day])
        t_day_sep = []
        for i in range(4):
            t_day_sep.append(t_day[6 * i : 6 * (i + 1)])




async def main(data_ba):
    data = await get_data("DataBase/data.db")
    await temperature_handler(data)


if __name__ == "__main__":
    asyncio.run(main())
