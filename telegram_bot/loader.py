from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.mongodb.mongodriver import MongoDriver
from common.config import api_key
from common.constants import Key, MongoData
import logging

# логгирование
logging.basicConfig(level=logging.INFO)

# бот
bot = Bot(token=api_key[Key.Api])

# хранилище состояний
storage = MemoryStorage()  # использует оперативную память

# диспетчер для обработки действий пользователя
dp = Dispatcher(bot, storage=storage)

# пользователи
db_user_data = MongoDriver(MongoData.db_main, MongoData.db_collection_user)

# приглашения
db_invite = MongoDriver(MongoData.db_main, MongoData.db_collection_invite)

# запросы пользователей
db_user_request = MongoDriver(MongoData.db_main, MongoData.db_collection_requests)

