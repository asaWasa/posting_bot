from aiogram import Bot, Dispatcher, executor, types
from common.passwords import key
from common.constants import KEY

bot = Bot(token=key[KEY.API])

dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
