from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from common.config import api_key
from common.constants import KEY


bot = Bot(token=api_key[KEY.API])


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
