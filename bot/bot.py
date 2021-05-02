from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from loader import dp, db_user, db_invite
from common.constants import USER, INVITE, SOCIAL_NETWORK
from common.db_user_format import USER_FORMAT


def out_keyword_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сделать пост")
    markup.add("Настройки", "Выход")
    return markup


class BotMainState(StatesGroup):
    begin = State()  # initial state
    auth = State()  # state for authorization or registration
    main = State()  # state main menu
    active = State()  # state for posting info
    settings = State()  # state for changing settings
    end = State()  # state ending


class BotAddSocialState(StatesGroup):
    login = State()
    password = State()


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    user = types.User.get_current()
    markup = types.ReplyKeyboardRemove()
    if db_user.is_in(USER.ID, user[USER.ID]):
        await BotMainState.main.set()
        await message.answer("Снова здравствуйте!", reply_markup=markup)
        markup = out_keyword_menu()
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer(str(message.from_user.first_name) + " Привет \n Место для красочного приветствия",
                             reply_markup=markup)
        await message.answer('Пройдите авторизацию')
        await BotMainState.auth.set()
        await message.answer('Введите код приглашения:')


@dp.message_handler(state=BotMainState.auth)
async def process_auth(message: types.Message):
    if db_invite.is_in(INVITE.INVITE_KEY, str(message.text)):
        user_data = USER_FORMAT(types.User.get_current())
        db_user.push(user_data.to_dict())
        await BotMainState.main.set()
        await message.answer("Успешный вход, добро пожаловать!")
        markup = out_keyword_menu()
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer("Такого приглашения не существует, повторите попытку")
        await message.answer('Введите код приглашения:')


@dp.message_handler(Text(equals="Сделать пост"), state=BotMainState.main)
async def add_post(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Добавить")
    markup.add('Удалить')
    markup.add("Назад")
    await BotMainState.active.set()
    await message.answer("Выберите нужную социальную сеть или отправьте сразу во все", reply_markup=markup)
    media = types.InlineKeyboardMarkup(row_width=3)
    user = types.User.get_current()
    user = db_user.get(USER.ID, user[USER.ID])
    social_networks = dict(user[USER.SOCIAL_NET])
    btns = list()
    if social_networks is None or social_networks == {}:
        await message.answer('У вас нет подключенных сетей')
    else:
        for net in social_networks:
            btns.append(types.InlineKeyboardButton("{}".format(net), callback_data='post_{}'.format(net), ))
        media.add(*btns)
        if len(social_networks) > 1:
            media.add(types.InlineKeyboardButton("All", callback_data='all'))
        await message.answer('Подключенные социальные сети:', reply_markup=media)


@dp.message_handler(Text(equals="Добавить"), state=BotMainState.active)
async def add_social_net(message: types.Message):
    media = types.InlineKeyboardMarkup(row_width=3)
    social_network = [SOCIAL_NETWORK.INSTAGRAM]
    btns = list()
    for net in social_network:
        btns.append(types.InlineKeyboardButton(text="{}".format(net), callback_data='add_{}'.format(net)))
    media.add(*btns)
    await message.answer('Выберите какую социальную сеть подключить:', reply_markup=media)


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORK.INSTAGRAM), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Процесс добавления социальной сети {} введите данные аккаунта'
                               .format(SOCIAL_NETWORK.INSTAGRAM))
    await state.update_data(name=SOCIAL_NETWORK.INSTAGRAM)
    await BotAddSocialState.login.set()
    await query.message.answer('Введите логин:', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=BotAddSocialState.login)
async def add_login(message: types.Message, state: FSMContext):
    login = message.text
    try:
        __check_login(login)
        async with state.proxy() as social_net:
            social_net['login'] = login
        await BotAddSocialState.password.set()
        await message.answer('Введите пароль:')
    except:
        await message.answer('Такой логин невозможен')


def __check_login(login):
    pass


@dp.message_handler(state=BotAddSocialState.password)
async def add_password(message: types.Message, state: FSMContext):
    password = message.text
    try:
        __check_password(password)
        async with state.proxy() as social_net:
            name = social_net['name']
            login = social_net['login']
        user = types.User.get_current()
        user = db_user.get(USER.ID, user[USER.ID])
        user[USER.SOCIAL_NET][name] = {'login': login, 'password': password}
        db_user.update_id(USER.ID, user[USER.ID], user)
        await BotMainState.main.set()
        markup = out_keyword_menu()
        await message.answer("Выберите действие", reply_markup=markup)
    except:
        await message.answer('Такой пароль невозможен')


def __check_password(password):
    pass

# def __add_in_user_social_net(user, social_net, key):
#     if user[key]:
#         user[key]

# @dp.callback_query_handler(Text(equals='post_' + SOCIAL_NETWORK.INSTAGRAM), state=BotState.active)
# async def callback_button_media(message: types.Message):
#     await message.answer('Процесс постинга в социальной сети {} '.format(SOCIAL_NETWORK.INSTAGRAM))


@dp.message_handler(Text(equals="Настройки"), state=BotMainState.main)
async def get_settings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Назад")
    await BotMainState.settings.set()
    await message.answer("Настройки", reply_markup=markup)


@dp.message_handler(Text(equals="Выход"), state=BotMainState.main)
async def exit_(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    await state.finish()
    await message.answer("Вышел", reply_markup=markup)


@dp.message_handler(Text(equals="Назад"), state=BotMainState.active)
async def go_back(message: types.Message):
    await BotMainState.main.set()
    await message.answer("<-")
    markup = out_keyword_menu()
    await message.answer("Выберите действие", reply_markup=markup)


@dp.message_handler(Text(equals="Назад"), state=BotMainState.settings)
async def go_back(message: types.Message):
    await BotMainState.main.set()
    await message.answer("<-")
    markup = out_keyword_menu()
    await message.answer("Выберите действие", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
