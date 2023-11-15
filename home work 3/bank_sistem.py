# Здесь мы все импортируем
from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
# from config import token_3
token_3 = "6407838890:AAEzapSdEMaREqWalJf4LWApcC0qoHpH17M"
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# создаем таблицу
connection = sqlite3.connect('bank_sistem')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_users (
               user_id INTEGER PRIMARY KEY,
               first_name VARCHAR (200),
               last_name VARCHAR (100),
               balance INTEGER  DEFAULT 0,
               number_number INTEGER
);""")
connection.commit()

bot = Bot(token=token_3)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)
# команды
@dp.message_handler(commands='start')
async def regist(message: types.Message):
    await message.answer('''Здравствуйте!
Этот бот может упровлять вашими счетами в нашем банке!
Вот весь функционал банка:
/start - информация о нас и саморегистрация!
/balance - проверка баланса!
/replenishment - пополнение баланса!
/transfer - перевод денег с помощю номера счета!
Рады каждому запросу!
''')
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM bank_users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    first_name = message.from_user.first_name
    last_name =  message.from_user.last_name
    user_number_balans = message.from_user.id
    
    if not user:
        cursor.execute('INSERT INTO bank_users (user_id, last_name, first_name, number) VALUES(?,?,?,?);', (user_id, first_name, last_name, user_number_balans))
        connection.commit()
        await message.answer(f'''поздровляем {first_name} зарегистрировались!\nтеперь вы можете пользоваться нашими услугами!
ваши данные:
Имя: {first_name}
Фамилия: {last_name}
номер счета: {user_id}
''')
    else:
        await message.answer(f'''{first_name} вы оказывается зарегистрированы!\nВы можете пользоваться нашими услугами!
ваши данные:
Имя: {first_name}
Фамилия: {last_name}
номер счета: {user_id}
''')

@dp.message_handler(commands='balance')
async def balance(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM bank_users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]
    await message.answer(f'ваш текущий баланс: {balance} сомов')
    if balance == 0:
        await message.answer('у вас нет средств для совершение операции в нашем банке\nПожалуйста пополните свой баланс\nДля пополнение нажмите /replenishment')

class Replenish(StatesGroup):
    money = State()

@dp.message_handler(commands='replenishment')
async def replenish_balance(message: types.Message, state:FSMContext):
    await message.answer('Введите сумму для пополнение:\n')
    await Replenish.money.set()


@dp.message_handler(state=Replenish.money)
async def replenish_finish(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    money_data = await state.get_data()
    summ = money_data.get('money')

    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM bank_users WHERE user_id = ?', (user_id,))
    current_balans = cursor.fetchone()[0]

    result = current_balans + int(summ)

    cursor.execute('UPDATE bank_users SET balance = ? WHERE user_id = ?', (result, user_id))
    connection.commit()

    await message.answer(f'Баланс успешно пополнен!\nВаш новый баланс: {result} сом!')

class Translation(StatesGroup):
    summ_2 = State()
    user_chek = State()
# создаем переводы /transfer
@dp.message_handler(commands='transfer')
async def transfer(message: types.Message, state:FSMContext):
    await message.answer('Для перевода введите cумму:\n')
    await Translation.summ_2.set()

@dp.message_handler(state=Translation.summ_2)
async def get_user_chek(message: types.Message, state:FSMContext):
    await state.update_data(summ_2 = message.text)
    await message.answer('введите номер счета:')
    await Translation.user_chek.set()

@dp.message_handler(state=Translation.user_chek)
async def finish(message: types.Message, state: FSMContext):
    await state.update_data(user_chek=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    amount = data.get('summ_2')
    recipient_user_id = data.get('user_chek')

    # Проверяем, что введенный номер счета является корректным пользователем
    cursor.execute('SELECT * FROM bank_users WHERE user_id = ?', (recipient_user_id,))
    recipient = cursor.fetchone()

    if recipient:
        # Проверяем, что у отправителя достаточно средств
        cursor.execute('SELECT balance FROM bank_users WHERE user_id = ?', (user_id,))
        sender_balance = cursor.fetchone()[0]

        if sender_balance >= int(amount):
            # Выполняем перевод
            sender_new_balance = sender_balance - int(amount)
            recipient_new_balance = recipient[3] + int(amount)

            cursor.execute('UPDATE bank_users SET balance = ? WHERE user_id = ?', (sender_new_balance, user_id))
            cursor.execute('UPDATE bank_users SET balance = ? WHERE user_id = ?', (recipient_new_balance, recipient_user_id))

            connection.commit()

            await message.answer(f'Перевод успешно выполнен!\n'
                                 f'Сумма: {amount} сом\n'
                                 f'Отправитель: {user_id}\n'
                                 f'Получатель: {recipient_user_id}\n'
                                 f'Баланс отправителя: {sender_new_balance} сом\n'
                                 f'Баланс получателя: {recipient_new_balance} сом')
        else:
            await message.answer('Недостаточно средств для выполнения перевода.')
    else:
        await message.answer('Получатель с указанным номером счета не найден.')

    # Сбрасываем состояние
    await state.finish()



@dp.message_handler()
async def none_message(message: types.Message):
    await message.answer('Возможно вы дали не ту команду😥\nнажмите /start чтобы ознакмица с нами и с нашими командами😆')

executor.start_polling(dp)