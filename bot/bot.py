import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from loader import bot, dp
from common.constants import USER, INVITE
from database.mongodb.mongodriver import MongoDriver

logging.basicConfig(level=logging.INFO)


class BotState(StatesGroup):
    begin = State()  # initial state
    auth = State()  # state for authorization or registration
    main = State()  # state main menu
    active = State()  # state for posting info
    settings = State()  # state for changing settings
    end = State()  # state ending


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message,  state: FSMContext):
    user = types.User.get_current()
    if db_user.is_in(USER.ID, user[USER.ID]):
        await BotState.main.set()
        await message.answer("Снова здравствуйте!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Сделать пост")
        markup.add("Настройки", "Выход")
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer(str(message.from_user.first_name) + " Привет \n Место для красочного приветствия")
        await message.answer('Пройдите авторизацию')
        await BotState.auth.set()
        await message.answer('Введите код приглашения:')


@dp.message_handler(state=BotState.auth)
async def process_auth(message: types.Message, state: FSMContext):
    if db_invite.is_in(INVITE.INVITE_KEY, str(message.text)):
        db_user.push(dict(types.User.get_current()))
        await BotState.main.set()
        await message.answer("Успешный вход, добро пожаловать!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Сделать пост")
        markup.add("Настройки", "Выход")
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer("Такого приглашения не существует, повторите попытку")


@dp.message_handler(state=BotState.main)
async def process_main(message: types.Message, state: FSMContext):
    await state.finish()


if __name__ == '__main__':
    db_user = MongoDriver('posting_bot', 'users')
    db_invite = MongoDriver('posting_bot', 'invite_keys')
    executor.start_polling(dp, skip_updates=True)
