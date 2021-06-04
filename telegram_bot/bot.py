from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from loader import dp, db_user_data, db_invite, db_user_request, stats
from common.constants import USER_DATA, UserRequest, INVITE, SOCIAL_NETWORKS, UserTypeRequest, RIGHTS
from database.db_format.user_data import ElementaryUserDataFormat
from database.db_format.user_request import UserRequestFormat
from posting_tools.telegram.telegram_api import get_photo_path
from common.errors import *


class BotMainState(StatesGroup):
    begin = State()  # initial state
    auth = State()  # state for authorization or registration
    main = State()  # state main menu
    active = State()  # state for posting info
    settings = State()  # state for changing settings
    end = State()  # state ending


class BotAdminState(StatesGroup):
    main = State()  # state main menu
    active = State()  # state for posting info
    settings = State()  # state for changing settings


# todo можно переделать в одно состояние и добавить его к основным состояниям
class BotAddSocialState(StatesGroup):
    business_id = State()  # state for input facebook business_id
    token = State()  # state for input facebook token


class BotAddPostState(StatesGroup):
    post_processing = State()


class BotCreateInviteState(StatesGroup):
    add_key = State()
    add_right = State()


def reply_keyboard_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сделать пост")
    markup.add("Настройки", "Выход")
    return markup


def reply_keyboard_admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Сделать пост", 'Создать приглашение')
    markup.add("Настройки", "Ошибки")
    markup.add('Выход')
    return markup


def reply_keyboard_backward():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Назад")
    return markup


def reply_passive_social_networks_keyboard():
    btns = list()
    media = types.InlineKeyboardMarkup(row_width=3)
    social_network = [SOCIAL_NETWORKS.INSTAGRAM, SOCIAL_NETWORKS.VK, SOCIAL_NETWORKS.YOUTUBE,
                      SOCIAL_NETWORKS.TIKTOK, SOCIAL_NETWORKS.TWITTER]
    for net in social_network:
        btns.append(types.InlineKeyboardButton(text="{}".format(net), callback_data='add_{}'.format(net)))
    media.add(*btns)
    return media


def reply_active_social_networks_keyboard(social_networks):
    btns = list()
    media = types.InlineKeyboardMarkup(row_width=3)
    for net in social_networks:
        btns.append(types.InlineKeyboardButton("{}".format(net), callback_data='post_{}'.format(net)))
    media.add(*btns)
    if len(social_networks) > 1:
        media.add(types.InlineKeyboardButton("All", callback_data='all'))
    return media


def reply_keyboard_right():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("User")
    markup.add("Admin")
    return markup


def get_id(request_table, param_for_search='id_request'):
    try:
        return int(request_table.get_count(param_for_search)[param_for_search]) + 1
    except:
        return 0


def __check_photo(photo):
    pass


def __check_caption(caption):
    pass


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    try:
        user = types.User.get_current()
        db_user = db_user_data.get(USER_DATA.ID, user[USER_DATA.ID])
        if db_user[USER_DATA.RIGHTS] == RIGHTS.USER:
            await BotMainState.main.set()
            await message.answer("Снова здравствуйте! " + str(message.from_user.first_name) +
                                 "\nЧем займемся на этот раз?", reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите действие", reply_markup=reply_keyboard_menu())
        elif db_user[USER_DATA.RIGHTS] == RIGHTS.ADMIN:
            await BotAdminState.main.set()
            s_users, s_errors = stats.get_statistic()
            await message.answer("Статистика по боту:\n"
                                 "Пользователей: {}\n"
                                 "Ошибки: {}".format(s_users, s_errors),
                                 reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Выберите действие", reply_markup=reply_keyboard_admin_menu())
        else:
            raise
    except:
        await message.answer('Привет ' + str(message.from_user.first_name) +
                             "\nРад что ты с нами!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Пройдите авторизацию')
        await BotMainState.auth.set()
        await message.answer('Введите код приглашения:')

    # if db_user_data.if_in(USER_DATA.ID, user[USER_DATA.ID]):
    #     await BotMainState.main.set()
    #     await message.answer("Снова здравствуйте! " + str(message.from_user.first_name) + "\nЧем займемся на этот раз?",
    #                          reply_markup=types.ReplyKeyboardRemove())
    #     markup = reply_keyboard_menu()
    #     await message.answer("Выберите действие", reply_markup=markup)
    # else:
    #     await message.answer('Привет ' + str(message.from_user.first_name) + "\nРад что ты с нами!",
    #                          reply_markup=types.ReplyKeyboardRemove())
    #     await message.answer('Пройдите авторизацию')
    #     await BotMainState.auth.set()
    #     await message.answer('Введите код приглашения:')


@dp.message_handler(state=BotMainState.auth)
async def process_auth(message: types.Message):
    try:
        invite_key = db_invite.get(INVITE.KEY, str(message.text))
        if invite_key[USER_DATA.RIGHTS] == RIGHTS.USER:
            user_data = ElementaryUserDataFormat(types.User.get_current())
            db_user_data.push(user_data.to_dict())
            await message.answer("Успешный вход, добро пожаловать!")
            await BotMainState.active.set()
            await message.answer("Какую сеть подключим?", reply_markup=reply_passive_social_networks_keyboard())
        elif invite_key[USER_DATA.RIGHTS] == RIGHTS.ADMIN:
            user_data = ElementaryUserDataFormat(types.User.get_current(), rights=RIGHTS.ADMIN)
            db_user_data.push(user_data.to_dict())
            await message.answer("Царь во дворца!")
            await BotAdminState.main.set()
            await message.answer("Выберите действие", reply_markup=reply_keyboard_admin_menu())
        else:
            raise
    except:
        await message.answer("Такого приглашения не существует, повторите попытку")
        await message.answer('Введите код приглашения:')

    # if db_invite.if_in(INVITE.KEY, str(message.text)):
    #     user_data = ElementaryUserDataFormat(types.User.get_current())
    #     db_user_data.push(user_data.to_dict())
    #     await message.answer("Успешный вход, добро пожаловать!")
    #     await BotMainState.active.set()
    #     await message.answer("Какую сеть подключим?", reply_markup=reply_passive_social_networks_keyboard())
    # else:
    #     await message.answer("Такого приглашения не существует, повторите попытку")
    #     await message.answer('Введите код приглашения:')


@dp.message_handler(Text(equals="Сделать пост"), state=BotMainState.main)
async def add_post(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Добавить")
    markup.add("Назад")
    await BotMainState.active.set()
    await message.answer("Выберите нужную социальную сеть или отправьте сразу во все", reply_markup=markup)
    user = types.User.get_current()
    user = db_user_data.get(USER_DATA.ID, user[USER_DATA.ID])
    social_networks = user[USER_DATA.SOCIAL_NETWORK]
    btns = list()
    if social_networks is None or social_networks == {}:
        await message.answer('У вас нет подключенных сетей')
    else:
        await message.answer('Подключенные социальные сети:',
                             reply_markup=reply_active_social_networks_keyboard(social_networks))


@dp.message_handler(Text(equals="Добавить"), state=BotMainState.active)
async def add_social_net(message: types.Message):
    await message.answer('Выберите какую социальную сеть подключить:',
                         reply_markup=reply_passive_social_networks_keyboard())


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORKS.INSTAGRAM), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Процесс добавления социальной сети {} введите данные аккаунта'
                               .format(SOCIAL_NETWORKS.INSTAGRAM))
    await state.update_data(name=SOCIAL_NETWORKS.INSTAGRAM)
    await BotAddSocialState.business_id.set()
    await query.message.answer('Введите business id :', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORKS.VK), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery):
    await query.message.answer('Скоро...', reply_markup=reply_keyboard_backward())


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORKS.YOUTUBE), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery):
    await query.message.answer('Скоро...', reply_markup=reply_keyboard_backward())


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORKS.TWITTER), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery):
    await query.message.answer('Скоро...', reply_markup=reply_keyboard_backward())


@dp.callback_query_handler(Text(equals='add_' + SOCIAL_NETWORKS.TIKTOK), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery):
    await query.message.answer('Скоро...', reply_markup=reply_keyboard_backward())


@dp.message_handler(state=BotAddSocialState.business_id)
async def add_login(message: types.Message, state: FSMContext):
    login = message.text
    try:
        __check_business_id(login)
        async with state.proxy() as social_net:
            social_net['business_id'] = login
        await BotAddSocialState.token.set()
        await message.answer('Введите token:')
    except:
        await message.answer('Такой business id невозможен')


def __check_business_id(business_id):
    pass


@dp.message_handler(state=BotAddSocialState.token)
async def add_password(message: types.Message, state: FSMContext):
    password = message.text
    try:
        __check_token(password)
        async with state.proxy() as social_net:
            name = social_net['name']
            login = social_net['business_id']
        user = types.User.get_current()
        user = db_user_data.get(USER_DATA.ID, user[USER_DATA.ID])
        user[USER_DATA.SOCIAL_NETWORK][name] = {'business_id': login, 'token': password}
        db_user_data.update_id(USER_DATA.ID, user[USER_DATA.ID], user)
        await BotMainState.main.set()
        await message.answer("Отлично! аккаунт для социальной сети {} добавлен, теперь \nВыберите действие"
                             .format('instagram'), reply_markup=reply_keyboard_menu())
    except Exception as e:
        await message.answer('Такой token невозможен')


def __check_token(token):
    pass


@dp.callback_query_handler(Text(equals='post_' + SOCIAL_NETWORKS.INSTAGRAM), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as social_net:
        social_net['name'] = SOCIAL_NETWORKS.INSTAGRAM
    await query.message.answer('Отправте изображение:', reply_markup=types.ReplyKeyboardRemove())
    await BotAddPostState.post_processing.set()


@dp.message_handler(content_types=['photo'], state=BotAddPostState.post_processing)
async def get_photo(message, state: FSMContext):
    try:
        image_id = message.photo[2].file_id
        image = get_photo_path(image_id)
        __check_photo(image)
        async with state.proxy() as post_object:
            post_object['image'] = image
        await message.answer('Добавте описание :')
    except Exception as e:
        await message.answer('Что-то пошло не так (  \n {}'.format(e))


@dp.message_handler(state=BotAddPostState.post_processing)
async def get_caption(message: types.Message, state: FSMContext):
    try:
        caption = message.text
        __check_caption(caption)
        async with state.proxy() as post_object:
            name = post_object['name']
            image = post_object['image']
        data = dict()
        data[UserRequest.Id_request] = get_id(db_user_request, 'id_request')
        data[UserRequest.User_id] = str(message.from_user.id)
        data[UserRequest.Type_request] = UserTypeRequest.Post_image
        data[UserRequest.Name] = name
        data[UserRequest.Data_object] = {'image': image, 'caption': caption}
        post_object = UserRequestFormat(data=data)
        db_user_request.push(post_object.to_dict())
        await message.answer('Принято в обработку')
        await message.answer('Возврат в главное меню\nВыберите действие', reply_markup=reply_keyboard_menu())
        await BotMainState.main.set()
    except UserCaptionError:
        await message.answer('Такое описание невозможно')
    except UserGoBack:
        await message.answer('Выберите действие', reply_markup=reply_keyboard_menu())
    except Exception as e:
        await message.answer('Что-то пошло не так (  \n {}'.format(e))


@dp.message_handler(Text(equals="Настройки"), state=BotMainState.main)
async def get_settings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Удалить подключенный аккаунт')
    markup.add("Назад")
    markup.add('Стереть все данные')
    await BotMainState.settings.set()
    await message.answer("Настройки", reply_markup=markup)


@dp.message_handler(Text(equals="Удалить подключенный аккаунт"), state=BotMainState.settings)
async def del_(message: types.Message, state: FSMContext):
    media = types.InlineKeyboardMarkup(row_width=3)
    user = types.User.get_current()
    user = db_user_data.get(USER_DATA.ID, user[USER_DATA.ID])
    social_networks = user[USER_DATA.SOCIAL_NETWORK]
    btns = list()
    for net in social_networks:
        btns.append(types.InlineKeyboardButton("{}".format(net),
                                               callback_data='del_{}'.format(net)))
    media.add(*btns)
    if len(social_networks) > 1:
        media.add(types.InlineKeyboardButton("All", callback_data='all'))
    await message.answer("Выберите аккаунт для удаления", reply_markup=media)


@dp.callback_query_handler(Text(equals='del_' + SOCIAL_NETWORKS.INSTAGRAM), state=BotMainState.settings)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    user = types.User.get_current()
    user = db_user_data.get(USER_DATA.ID, user[USER_DATA.ID])
    user[USER_DATA.SOCIAL_NETWORK] = {}
    db_user_data.update_id(USER_DATA.ID, user[USER_DATA.ID], user)
    await query.message.answer('Аккаунт социальной сети instagram удален\nВыберите действие:',
                               reply_markup=reply_keyboard_menu())
    await BotMainState.main.set()


@dp.message_handler(Text(equals="Стереть все данные"), state=BotMainState.settings)
async def exit_(message: types.Message, state: FSMContext):
    user = types.User.get_current()
    if db_user_data.if_in(USER_DATA.ID, user[USER_DATA.ID]):
        db_user_data.pop(USER_DATA.ID, user[USER_DATA.ID])
    await state.finish()
    await message.answer("Вся информация о вас полностью очищена!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Выход"), state=BotMainState.main)
async def exit_(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Вышел", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Назад"), state=[BotMainState.active, BotMainState.settings])
async def go_back(message: types.Message):
    await BotMainState.main.set()
    await message.answer("<-")
    await message.answer("Выберите действие", reply_markup=reply_keyboard_menu())


#_________________________ADMIN_PANEL____________________________#

@dp.message_handler(Text(equals="Создать приглашение"), state=BotAdminState.main)
async def add_invite(message: types.Message, state: FSMContext):
    await message.answer("Придумайте приглашение:", reply_markup=types.ReplyKeyboardRemove())
    await BotCreateInviteState.add_key.set()


@dp.message_handler(state=BotCreateInviteState.add_key)
async def add_right(message: types.Message, state: FSMContext):
    try:
        key = str(message.text)
        async with state.proxy() as post_object:
            post_object['key'] = key
        await message.answer("Выберите права для приглашения", reply_markup=reply_keyboard_right())
        await BotCreateInviteState.add_right.set()
    except Exception as e:
        await message.answer("Неизвестная ошибка1", reply_markup=reply_keyboard_admin_menu())
        await BotAdminState.main.set()


@dp.message_handler(state=BotCreateInviteState.add_right)
async def add_right(message: types.Message, state: FSMContext):

    try:
        right = __format_right(message.text)
        __check_right(right)
        async with state.proxy() as post_object:
            key = post_object['key']
        db_invite.push({INVITE.KEY: key, USER_DATA.RIGHTS: right})
        await message.answer('Приглашение создано\n'
                             'Возврат в главное меню', reply_markup=reply_keyboard_admin_menu())
        await BotAdminState.main.set()
    except:
        await message.answer("Неизвестная ошибка2", reply_markup=reply_keyboard_admin_menu())
        await BotAdminState.main.set()


def __format_right(_str):
    if _str == 'User':
        return RIGHTS.USER
    elif _str == 'Admin':
        return RIGHTS.ADMIN
    else:
        raise


def __check_right(right):
    if right == RIGHTS.USER or right == RIGHTS.ADMIN:
        pass
    else:
        raise


# @dp.message_handler(Text(equals="Ошибки"), state=BotAdminState.main)
# async def get_errors(message: types.Message, state: FSMContext):
#     for error in db_errors.find_all():





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
