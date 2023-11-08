from aiogram import Bot, Dispatcher, executor, types
import sqlite3

token = "6497163252:AAEStGlgMjZ9QqiwO6ZUtm0iIeQbn-gvFuU"

bot = Bot(token=token)
db = Dispatcher(bot)


connection = sqlite3.connect('client.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER,
               user_name VARCHAR (200),
               first_name VARCHAR (200),
               last_name VARCAR(200)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reseipt (
               payment_cod INT,
               first_name VARCHAR (200),
               last_name VARCHAR (200),
               direction VARCHAR (200),
               amount INT,
               date VARCHAR (2000)
);
""")


start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Наш адрес'),
    types.KeyboardButton('Наши контакты'),
    types.KeyboardButton('Курсы')
]

start_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@db.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет добро пожаловать в Geeks!!', reply_markup=start_buttons)
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    user = cursor.fetchone()
    if not user:
        user_id = message.from_user.id
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        cursor.execute('INSERT INTO users (id, user_name, first_name, last_name) VALUES (?,?,?,?)',(user_id, user_name, first_name, last_name))
        connection.commit()       
    print(message.from_user.first_name)
    print(message.from_user.username)
    print(message.from_user.id)
    
@db.message_handler(text='О нас')
async def about_us(message: types.Message):
    await message.answer("В Geeks ты сможеш найти все курсы по програмирование")

@db.message_handler(text='Наш адрес')
async def adres(message: types.Message):
    await message.answer("Наш адрес \n улица Мырзалы Аматова 1-B")
    await message.answer_location(12.32)

@db.message_handler(text = 'Наши контакты')
async def kontacts(message: types.Message):
    await message.answer_contact('0776001124', 'ERBOL', 'Adilbekov')
    await message.answer_contact('0508030879', 'Erbol_2', 'Adilbekov')

start_bottons = [
    types.KeyboardButton('Backend'),
    types.KeyboardButton('Frontent'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('UX/OI'),
    types.KeyboardButton('Стоимость курсов'),
    types.KeyboardButton('Назат')
    
]
corses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_bottons)

@db.message_handler(text= 'Курсы')
async def bac(message: types.Message):
    await message.answer('Вот все курсы: ', reply_markup=corses_keyboard)



@db.message_handler(text = 'Backend')
async def bac(message: types.Message):
    await message.answer('Backend - это разработка внутренней части сайта')

@db.message_handler(text='Frontent')
async def fr(message: types.Message):
    await message.answer('Frontent - это разработка внкешней части сайта')

@db.message_handler(text='Android')
async def android(message: types.Message):
    await message.answer('Android - разработка разлиных приложений')

@db.message_handler(text='UX/OI')
async def dizine(message: types.Message):
    await message.answer('UX/OI - это создание дизайна')


@db.message_handler(text='Назат')
async def exit(message: types.Message):
    await start(message)

@db.message_handler(text = 'Стоимость курсов')
async def money(message: types.Message):
    await message.answer('стоимость всех курсов состовляет:\n10 000 сом в месяц')


executor.start_polling(db)