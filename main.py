import asyncio
from get_info import get_info_main, city_valid, date_valid


async def main():
    while True:
        city = input('Введите город: ')
        if await city_valid(city):
            start_date = input('Вводите в формате: ГОД-МЕСЯЦ-ДАТА! \nС какой даты: ')
            end_date = input('До какой даты (не больше 50 дней дельта): ')
            if await date_valid(start_date, end_date):
                break
            else:
                print('Неверные даты! Попробуйте снова и вводите дату в нужном формате.')
        else:
            print('Такого города нет! Попробуйте снова.')
    status = await get_info_main(city, start_date, end_date)
    if status:
        print('Все гуд!')
    else:
        print('Произошла ошибка! Попробуйте снова.')
    

if __name__ == "__main__":
    asyncio.run(main())
