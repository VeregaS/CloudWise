import asyncio
import sqlite3
import pandas as pd


# функция получения информации из базы данных
async def get_data(db_name):
    conn = sqlite3.connect(db_name)
    sql_query = """SELECT * FROM main"""
    data = pd.read_sql_query(sql_query, con=conn)
    conn.close()
    return data


# анализ температурных данных
async def temperature_analytics(data: pd.DataFrame) -> None:
    for day in range(len(data)):
        pass


async def main():
    data = await get_data("data.db")
    temperature_analytics(data)


if __name__ == "__main__":
    asyncio.run(main())
