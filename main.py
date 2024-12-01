import asyncio
import time
from get_info import get_info_main, city_valid, date_valid

async def main():
    while True:
        city = input('Введите город: ')
        start_time = time.time()
        if await city_valid(city):
            print('-' * 44 + '\n', time.time() - start_time, '\t Валидация города\n', '-' * 44 + '\n')
            start_date = input('Вводите в формате: ГОД-МЕСЯЦ-ДАТА! \nС какой даты: ')
            end_date = input('До какой даты (не больше 50 дней дельта): ')
            start_time = time.time()
            if await date_valid(start_date, end_date):
                print('-' * 44 + '\n', time.time() - start_time, '\t Валидация даты\n', '-' * 44 + '\n')
                break
            else:
                print('Неверные даты! Попробуйте снова и вводите дату в нужном формате.')
        else:
            print('Такого города нет! Попробуйте снова.')
    start_time = time.time()
    status = await get_info_main(city, start_date, end_date)
    print('-' * 44 + '\n', time.time() - start_time, '\t Получение инфорации\n', '-' * 44 + '\n')
    if status:
        print('Все гуд!')
    else:
        print('Произошла ошибка! Попробуйте снова.')
    


if __name__ == "__main__":
    asyncio.run(main())
