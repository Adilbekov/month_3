from aiogram import Bot,executor,Dispatcher,types
from config import token_1
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging


start_buttons = [
    types.KeyboardButton("Отправь номер", request_contact=True),
    types.KeyboardButton("Отправь локацию", request_location=True),
    types.KeyboardButton("Отправь сообшение")
    
]
start_key = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)
bot = Bot(token=token_1)
storege = MemoryStorage()
dp = Dispatcher(bot,storage=storege)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"привет {message.from_user.full_name}", reply_markup=start_key)
    
    
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_con(message:types.Message):
    await message.answer(f"{message.contact.phone_number}")
    
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_loc(message:types.Message):
    await message.answer(f"{message.location}")
    
anonim_butt = [
    types.InlineKeyboardButton('Да', callback_data="select_yes"),
    types.InlineKeyboardButton('Нет', callback_data="select_no")
    
]   
anonim_key = types.InlineKeyboardMarkup().add(*anonim_butt) 

@dp.message_handler(text='Отправь сообшение')
async def get_mess(message:types.Message):
    await message.answer('вы хотите отправить анонимное сообщение?', reply_markup=anonim_key)
    
    
@dp.callback_query_handler(lambda call: call.data == 'select_no')
async def select_no_answer(message:types.CallbackQuery):
    await message.answer("типо ОКЕЙ")
    print(message)
    await bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    
class AnonimState(StatesGroup):
    message = State()
@dp.callback_query_handler(lambda call: call.data == "select_yes")
async def select_yes_answer(message:types.CallbackQuery):
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                text="Напишите свое сообщение")
    await AnonimState.message.set()   
    
@dp.message_handler(state=AnonimState.message)
async def send_message_group(message:types.Message, state:FSMContext):
    await message.answer("Отправляю сообщение ..............")
    await bot.send_message(chat_id= -4037053389, text=message.text)
    await message.answer("Oтправили сообшение")
    await state.finish()
@dp.message_handler()
async def echo(message:types.Message):
    await message.reply('ERROR')
    
executor.start_polling(dp,skip_updates=True)