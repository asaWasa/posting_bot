from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from common.config import api_key
from common.constants import KEY

# бот
bot = Bot(token=api_key[KEY.API])

# хранилище состояний
storage = MemoryStorage()  # использует оперативную память

# диспетчер для обработки действий пользователя
dp = Dispatcher(bot, storage=storage)
