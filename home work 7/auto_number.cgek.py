from aiogram import Bot, Dispatcher, executor, types
from logging import basicConfig, INFO
from config import token_6
import sqlite3
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
connect = sqlite3.connect('car.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS car_info(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               license_plates_of_cars VARCHAR (200),
               brand VARCHAR (200),
               model VARCHAR (200),
               color VARCHAR (200),
               year INTEGER,
               complect VARCHAR (200),
               state VARCHAR (200)
);""")
def add_car(license_plates_of_cars,brand, model, color, year, complect, state):
    cursor.execute("INSERT INTO car_info (license_plates_of_cars, brand, model, color, year, complect, state) VALUES (?,?,?,?,?,?,?)", (license_plates_of_cars, brand, model, color, year, complect, state))
    connect.commit()
# add_car('01-001-ERA', 'BMW', 'M 5-competition', 'blue', 2017, 'Полная комплектация!', 'Новый')
# add_car('01-100-CTO', 'MERSEDES-BENS', 'E-124', 'BLACK', 1993, 'Полная комплектация!', 'Новый')
# add_car('02-002-OSH', 'FIT', 'FIT', 'blue', 2005, 'не-полная!', 'Новый')
# add_car('01-063-CLS', 'MERSEDES', 'CLS-500', 'WHILE', 2020, 'Полная СРЕДНЯЯ!', 'БУ')
# add_car('01-100-BRO', 'BMW', 'M 3-competition', 'WHILE', 2022, 'Полная комплектация!', 'Новый')
# add_car('01-777-SEM', 'MERSEDES-BENS', 'W-211', 'WILE', 2015, 'Полная комплектация!', 'Новый')
# add_car('01-001-BEK', 'BMW', 'M 8-competition', 'BLACK', 2022, 'Полная комплектация!', 'Новый')
# add_car('02-002-TWO', 'MERSEDES', 'GT-300', 'YELLO', 2022, 'Полная комплектация!', 'Новый')
# add_car('02-888-OSH', 'MERSEDES-BENZ', 'W-210', 'BLACK', 2013, 'Полная комплектация!', 'Новый')
# add_car('01-001-ONE', 'BMW', 'M 5-SAMURAY', 'BLACK', 2015, 'Полная комплектация!', 'Новый')

basicConfig(level=INFO)
bot = Bot(token_6)
storege = MemoryStorage()
dp = Dispatcher(bot, storage=storege)

# Обработка команды /старт
@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}!\nЭтот бот может находить машину по номерам и дать информацию о авто!\nЗапросы:\nВсе номера наших авто: /number_all_cars\nНайти машину по номеру: /find_a_car')

# функция для выведение информации авто если есть номер введенным пользователем
def number_car(number):
    cursor.execute('SELECT * FROM car_info WHERE license_plates_of_cars = ?', (number,))
    result = cursor.fetchone()
    connect.commit()
    if result:
        return f"""Информация о машине:\n
Номер: {result[1]}
Марка: {result[2]}
Модель: {result[3]}
Цвет: {result[4]}
Год выпуска: {result[5]}
Комплектация: {result[6]}
Состояние: {result[7]}"""
    else:
        return "У нас нет машин с такими номерами"

# использовании Машины состоянии
class Car(StatesGroup):
    number = State()

# Обработка команды /нахождении авто по номепру
@dp.message_handler(commands='find_a_car')
async def car(message: types.Message, state:FSMContext):
    await message.answer("Введите номер машины:")
    await Car.number.set()

# обрабатываем Машины состоянию и исползуем функцию созданный раньше и передаем функции то сообшение что ввел пользователь
@dp.message_handler(state=Car.number)
async def find_car_number(message: types.Message, state:FSMContext):
    await state.update_data(number=message.text)
    date = await state.get_data()
    car_num = date.get('number')
    await message.answer(number_car(car_num))
    await state.finish()

# Обработка команды /все номера машин
@dp.message_handler(commands='number_all_cars')
async def all_number_car(message: types.Message):
    cursor.execute("SELECT license_plates_of_cars FROM car_info")
    result = cursor.fetchall()
    await message.answer('Вот все свежие номера:')
    for car_num in result:
        await message.answer({car_num[0]})
    await message.answer('алтыным стоимость всех номеров состовляет: 110млн$')


@dp.message_handler()
async def errror_message(message: types.Message):
    await message.answer('Извините, вы ввели неправильную команду\nДля информации о нас нажмите /start')


executor.start_polling(dp)