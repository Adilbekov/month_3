from aiogram import Bot, Dispatcher, types, executor
from config import token

bot = Bot(token=token)      
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer('Hello bro!')

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("чем я могу помочь,")

@dp.message_handler(text='hello')
async def hello(message:types.Message):
    await message.answer("Hello как дела,")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.answer("тестовое сообщение")
    await message.answer_location(0, 0)
    await message.answer_dice()
    await message.answer_photo('https://geeks.kg/back_media/main_block/2023/06/22/e775ccf8-e496-4e01-9bfb-dc53073d3700.webp')
    await message.answer_contact('07776001124', 'Erbol', 'Adilbekov')
    # with open("photo,jpg", "rb") as photo:
    #     await message.answer_photo(photo)

if __name__ == '__main__':
    executor.start_polling(dp)