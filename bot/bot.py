import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
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


def out_keyword_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сделать пост")
    markup.add("Настройки", "Выход")
    return markup


@dp.message_handler(commands=['start'], state=None)
async def cmd_start(message: types.Message,  state: FSMContext):
    user = types.User.get_current()
    if db_user.is_in(USER.ID, user[USER.ID]):
        await BotState.main.set()
        await message.answer("Снова здравствуйте!")
        markup = out_keyword_menu()
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
        markup = out_keyword_menu()
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer("Такого приглашения не существует, повторите попытку")


@dp.message_handler(Text(equals="Сделать пост"), state=BotState.main)
async def add_post(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Назад")
    await BotState.active.set()
    await message.answer("Выберите соц сети:", reply_markup=markup)
    # Вывести все соцсети пользователя и all для отправки во все соц сети


@dp.message_handler(Text(equals="Настройки"), state=BotState.main)
async def get_settings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Назад")
    await BotState.settings.set()
    await message.answer("Настройки", reply_markup=markup)


@dp.message_handler(Text(equals="Выход"), state=BotState.main)
async def exit_(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    await state.finish()
    await message.answer("Вышел", reply_markup=markup)


@dp.message_handler(Text(equals="Назад"), state=BotState.active)
async def go_back(message: types.Message):
    await BotState.main.set()
    await message.answer("<-")
    markup = out_keyword_menu()
    await message.answer("Выберите действие", reply_markup=markup)


@dp.message_handler(Text(equals="Назад"), state=BotState.settings)
async def go_back(message: types.Message):
    await BotState.main.set()
    await message.answer("<-")
    markup = out_keyword_menu()
    await message.answer("Выберите действие", reply_markup=markup)


if __name__ == '__main__':
    db_user = MongoDriver('posting_bot', 'users')
    db_invite = MongoDriver('posting_bot', 'invite_keys')
    executor.start_polling(dp, skip_updates=True)
