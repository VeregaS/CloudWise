import asyncio
from get_info import get_info_main, city_valid, date_valid

async def main():
    while True:
        city = input('Введите город: ')
        if await city_valid(city):
            start_date = input('Вводите в формате год-месяц-дата! \nС какой даты: ')
            end_date = input('До какой даты: ')
            if await date_valid(start_date, end_date):
                break
            else:
                print('Неверные даты! Попробуйте снова.')
        else:
            print('Такого города нет! Попробуйте снова.')
    ans = await get_info_main(city, start_date, end_date)
    return ans


if __name__ == "__main__":
    asyncio.run(main())
