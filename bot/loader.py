from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.mongodb.mongodriver import MongoDriver
from common.config import api_key
from common.constants import KEY, MONGO_DATA
import logging

# логгирование
logging.basicConfig(level=logging.INFO)

# бот
bot = Bot(token=api_key[KEY.API])

# хранилище состояний
storage = MemoryStorage()  # использует оперативную память

# диспетчер для обработки действий пользователя
dp = Dispatcher(bot, storage=storage)

# пользователи
db_user_data = MongoDriver(MONGO_DATA.DB_NAME, MONGO_DATA.DB_COLLECTION_USER)

# приглашения
db_invite = MongoDriver(MONGO_DATA.DB_NAME, MONGO_DATA.DB_COLLECTION_INVITE)

db_user_request = MongoDriver(MONGO_DATA.DB_NAME, MONGO_DATA.DB_COLLECTION_REQUEST)
