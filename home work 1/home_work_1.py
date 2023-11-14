from aiogram import Dispatcher, Bot, executor, types
from config import token
from random import randint


bot = Bot(token = token)
db = Dispatcher(bot)



@db.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Я загодал число от 1 до 3\nугадай:\n')

@db.message_handler(text=['1','2','3'])
async def ran(message: types.Message):
    comp = randint(1,3)

    if int(message.text) == comp:
        await message.answer("yor winner!")
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
        await message.answer(f'угаданное число: {comp}')
    elif int(message.text) != comp:
        await message.answer(f'угаданное число: {comp}')
        await message.answer('вы проиграли!!')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
    else:
        print('Syntax error!!')

executor.start_polling(db)