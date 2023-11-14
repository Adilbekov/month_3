from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token_2
from logging import basicConfig, INFO
import sqlite3
from datetime import datetime

bot = Bot(token=token_2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)


connect = sqlite3.connect('ojak_users.db')
cursor = connect.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR(100),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        date_joined DATETIME
    );
''')
connect.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100),
        title TEXT,
        phone_number VARCHAR(100),
        address VARCHAR(100)
    );
''')
connect.commit()

class OrderFoodState(StatesGroup):
    name = State()
    title = State()
    phone_number = State()
    address = State()



start_buttons = [
    types.KeyboardButton('Меню'),
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Заказать еду'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if not  res:
        cursor.execute(f"""INSERT INTO users (id, username, first_name, last_name, date_joined) VALUES (
            {message.from_user.id},
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{message.from_user.username}',
            '{datetime.now()}'
        );
        """)
        cursor.connection.commit()
    await message.answer(f"Здравствуйте {message.from_user.full_name}, добро пожаловать в Ojak Kebab!", reply_markup=start_keyboard)

@dp.message_handler(text='Меню')
async def manu(message:types.Message):
    await message.answer('https://nambafood.kg/ojak-kebap#99')


@dp.message_handler(text='О нас')
async def about(message:types.Message):
    await message.answer('Кафе "Ожак Кебап" на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.\nНаше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.\nПодробнее https://ocak.uds.app/c/about')


@dp.message_handler(text='Адрес')
async def about(message:types.Message):
    await message.answer('Исы Ахунбаева ,97а. +996700505333\nОткрыто до 00:00.\n Наши другие точки можете посмотреть: https://ocak.uds.app/c/about')


@dp.message_handler(text='Заказать еду')
async def about(message:types.Message):
    await message.answer('Введите ваше имя')
    await OrderFoodState.name.set()


@dp.message_handler(state=OrderFoodState.name)
async def process_food_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Что хотите заказать?")
    await OrderFoodState.next()

@dp.message_handler(state=OrderFoodState.title)
async def process_food_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await message.answer("Введите свой номер телефона")
    await OrderFoodState.next()


@dp.message_handler(state=OrderFoodState.phone_number)
async def process_food_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.answer("Введите свой адрес")
    await OrderFoodState.next()


@dp.message_handler(state=OrderFoodState.address)
async def process_food_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

    async with state.proxy() as data:
        name = data['name']
        title = data['title']
        phone_number = data['phone_number']
        address = data['address']

    cursor.execute('''
        INSERT INTO orders (name, title, phone_number, address )
        VALUES (?, ?, ?, ?)
    ''', (name, title, phone_number, address))
    connect.commit()

    await message.answer("Ваш заказ принять.\nЖдите он никогда не приедет")
    await state.finish()



executor.start_polling(dp, skip_updates=True)