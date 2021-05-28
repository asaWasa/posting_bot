from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from database.mongodb.mongodriver import MongoDriver
from common.config import api_key
from common.constants import Key, MongoData
import logging

# логгирование
logging.basicConfig(level=logging.INFO)

# бот
bot = Bot(token=api_key[Key.Api])

# todo заменить хранилище состояний, чтобы состояния хранились в базе mongodb  (MongoStorage)
# хранилище состояний

# storage = MemoryStorage()  # хранилище состояний использует оперативную память
storage = MongoStorage(
    host='localhost',
    port=27017,
    db_name='posting_bot_fsm'
)  # Хранилище состояний использует базу данных mongodb

# диспетчер для обработки действий пользователя
dp = Dispatcher(bot, storage=storage)

# пользователи
db_user_data = MongoDriver(MongoData.db_main, MongoData.db_collection_user)

# приглашения
db_invite = MongoDriver(MongoData.db_main, MongoData.db_collection_invite)

# запросы пользователей
db_user_request = MongoDriver(MongoData.db_main, MongoData.db_collection_requests)
