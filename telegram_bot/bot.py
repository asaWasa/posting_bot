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
    name = State()
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
    user = types.User.get_current()
    if db_user_data.is_in(UserData.Id, user[UserData.Id]):
        await BotMainState.main.set()
        await message.answer("Снова здравствуйте! " + str(message.from_user.first_name) + "\nЧем займемся на этот раз?",
                             reply_markup=types.ReplyKeyboardRemove())
        markup = reply_keyboard_menu()
        await message.answer("Выберите действие", reply_markup=markup)
    else:
        await message.answer('Привет ' + str(message.from_user.first_name) + "\nРад что ты с нами!",
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Пройдите авторизацию')
        await BotMainState.auth.set()
        await message.answer('Введите код приглашения:')


@dp.message_handler(state=BotMainState.auth)
async def process_auth(message: types.Message):
    if db_invite.is_in(Invite.Invite_key, str(message.text)):
        user_data = UserDataFormat(types.User.get_current())
        db_user_data.push(user_data.to_dict())
        await BotMainState.main.set()
        await message.answer("Код принят, добро пожаловать!")
        await BotMainState.active.set()
        await message.answer("Какую сеть подключим?", reply_markup=reply_add_social_networks())
    else:
        await message.answer("Такого приглашения не существует, повторите попытку")
        await message.answer('Введите код приглашения:')


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
        for net in social_networks:
            for account in social_networks[net]:
                #todo непонятно как понимать с какого аккаунта человек хочет запостить
                btns.append(types.InlineKeyboardButton("{}".format(account + ':' + net),
                                                       callback_data='post_{}_{}'.format(net, account)))
        media.add(*btns)
        if len(social_networks) > 1:
            media.add(types.InlineKeyboardButton("All", callback_data='all'))
        await message.answer('Подключенные социальные сети:', reply_markup=media)


@dp.message_handler(Text(equals="Добавить"), state=BotMainState.active)
async def add_social_net(message: types.Message):
    await message.answer('Выберите какую социальную сеть подключить:', reply_markup=reply_add_social_networks())


@dp.callback_query_handler(Text(contains='add_' + SocialNetwork.Instagram), state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Процесс добавления социальной сети {} введите данные аккаунта'
                               .format(SocialNetwork.Instagram))
    await state.update_data(name=SocialNetwork.Instagram)
    await BotAddSocialState.name.set()
    async with state.proxy() as social_net:
        social_net['name_social_net'] = SocialNetwork.Instagram
    await query.message.answer('Введите отображаемое название:', reply_markup=types.ReplyKeyboardRemove())


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


@dp.message_handler(state=BotAddSocialState.name)
async def add_name(message: types.Message, state: FSMContext):
    name = message.text
    try:
        __check_name(name)
        async with state.proxy() as social_net:
            social_net['name'] = name
        await BotAddSocialState.business_id.set()
        await message.answer('Введите business id аккаунта:')
    except:
        await message.answer('Такое название невозможно')


def __check_name(name):
    return name


@dp.message_handler(state=BotAddSocialState.business_id)
async def add_login(message: types.Message, state: FSMContext):
    login = message.text
    try:
        __check_business_id(login)
        async with state.proxy() as social_net:
            social_net['business_id'] = login
        await BotAddSocialState.token.set()
        await message.answer('Введите token:')
    except BusinessIdError:
        await message.answer('Такой business id невозможен')
    except:
        await message.answer('Неизвестная ошибка, возврат в главное меню\nВыберите действие',
                             reply_markup=reply_keyboard_menu())
        await BotMainState.main.set()


def __check_business_id(business_id):
    pass


@dp.message_handler(state=BotAddSocialState.token)
async def add_token(message: types.Message, state: FSMContext):
    token = message.text
    try:
        __check_token(token)
        async with state.proxy() as social_net:
            name = social_net['name']
            social = social_net['name_social_net']
            business = social_net['business_id']
        user = types.User.get_current()
        user = db_user_data.get(UserData.Id, user[UserData.Id])

        # user[UserData.Social_net][social] = {'name': name, 'business_id': business, 'token': token}
        try:
            user[UserData.Social_net][social][name] = {'business_id': business,
                                                       'token': token}
        except:
            user[UserData.Social_net][social] = dict()
            user[UserData.Social_net][social][name] = {'business_id': business,
                                                       'token': token}

        db_user_data.update_id(UserData.Id, user[UserData.Id], user)
        await BotMainState.main.set()
        markup = reply_keyboard_menu()
        await message.answer("Отлично! аккаунт для социальной сети {} добавлен, теперь \nВыберите действие"
                             .format(social), reply_markup=markup)
    except UserTokenError:
        await message.answer('Такой token невозможен')
    except Exception as e:
        #todo Закинуть в лог ошибку
        await message.answer('Неизвестная ошибка, возврат в главное меню\nВыберите действие',
                             reply_markup=reply_keyboard_menu())
        await BotMainState.main.set()


def __check_token(token):
    pass


@dp.callback_query_handler(text_contains='post_' + SocialNetwork.Instagram, state=BotMainState.active)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as social_net:
        social_net['name_social_net'] = SocialNetwork.Instagram

    await query.message.answer('Отправте изображение:', reply_markup=types.ReplyKeyboardRemove())
    await BotAddPostState.post_processing.set()


@dp.message_handler(content_types=['photo'], state=BotAddPostState.post_processing)
async def get_photo(message, state: FSMContext):
    try:
        image_id = message.photo[-1].file_id
        image = get_photo_path(image_id)
        __check_photo(image)
        async with state.proxy() as post_object:
            post_object['image'] = image
        await message.answer('Добавте описание если требуется\n'
                             'отправте пуское поле если не хотите добавлять:',
                             reply_markup=reply_keyboard_skip_caption())
    except Exception as e:
        await message.answer('Что-то пошло не так (  \n {}'.format(e))


@dp.message_handler(state=BotAddPostState.post_processing)
async def get_caption(message: types.Message, state: FSMContext):
    try:
        caption = message.text
        caption = __check_caption(caption)
        async with state.proxy() as post_object:
            # name = post_object['name']
            name_social_net = post_object['name_social_net']
            image = post_object['image']
        data = dict()
        data[UserRequest.Id_request] = get_id(db_user_request, 'id_request')
        data[UserRequest.User_id] = str(message.from_user.id)
        data[UserRequest.Type_request] = UserTypeRequest.Post_image
        # data[UserRequest.Name] = name
        data[UserRequest.Social_network] = name_social_net
        data[UserRequest.Data_object] = {'image': image, 'caption': caption}
        post_object = UserRequestFormat(data=data)
        db_user_request.push(post_object.to_dict())
        await message.answer('Добавлено в очередь на отправку')
        await BotMainState.active.set()
    except UserCaptionError:
        await message.answer('Такое описание невозможно')
    except UserGoBack:
        await message.answer('Выберите действие', reply_markup=reply_keyboard_menu())
    except Exception as e:
        await message.answer('Неизвестная ошибка, возврат в главное меню\nВыберите действие',
                             reply_markup=reply_keyboard_menu())
        await BotMainState.main.set()


@dp.message_handler(Text(equals="Настройки"), state=BotMainState.main)
async def get_settings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Удалить подключенный аккаунт')
    markup.add("Назад")
    markup.add('Стереть все данные')
    await BotMainState.settings.set()
    await message.answer("Настройки", reply_markup=markup)


@dp.message_handler(Text(equals="Удалить подключенный аккаунт"), state=BotMainState.settings)
async def exit_(message: types.Message, state: FSMContext):
    media = types.InlineKeyboardMarkup(row_width=3)
    user = types.User.get_current()
    user = db_user_data.get(UserData.Id, user[UserData.Id])
    social_networks = user[UserData.Social_net]
    btns = list()
    for net in social_networks:
        btns.append(types.InlineKeyboardButton("{}".format(social_networks[net]['name'] + ':' + net),
                                               callback_data='del_{}'.format(net)))
    media.add(*btns)
    if len(social_networks) > 1:
        media.add(types.InlineKeyboardButton("All", callback_data='all'))
    await message.answer("Выберите аккаунт для удаления", reply_markup=media)


@dp.message_handler(Text(equals="Стереть все данные"), state=BotMainState.settings)
async def exit_(message: types.Message, state: FSMContext):
    user = types.User.get_current()
    if db_user_data.is_in(UserData.Id, user[UserData.Id]):
        db_user_data.pop(UserData.Id, user[UserData.Id])
    markup = types.ReplyKeyboardRemove()
    await state.finish()
    await message.answer("Вся информация о вас полностью очищена!", reply_markup=markup)


@dp.message_handler(Text(equals="Выход"), state=BotMainState.main)
async def exit_(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    await state.finish()
    await message.answer("Вышел", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Назад"), state=[BotMainState.active, BotMainState.settings])
async def go_back(message: types.Message):
    await BotMainState.main.set()
    await message.answer("<-")
    markup = reply_keyboard_menu()
    await message.answer("Выберите действие", reply_markup=markup)


@dp.message_handler(Text(equals="Назад"), state=BotMainState.settings)
async def go_back(message: types.Message):
    await BotMainState.main.set()
    await message.answer("<-")
    markup = reply_keyboard_menu()
    await message.answer("Выберите действие", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
