from aiogram import Bot, Dispatcher, executor, types
import requests, aioschedule, asyncio
from config import token_1
from logging import basicConfig, INFO

basicConfig(level=INFO)
bot = Bot(token=token_1)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Hello {message.from_user.full_name}')

async def send_message():
    await bot,send_message(-4037053389, 'Hello werld')

async def sheduler():
    aioschedule.every(5).seconds.do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_start_up(parameter):
    asyncio.create_task(sheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)