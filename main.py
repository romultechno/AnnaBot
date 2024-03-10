import asyncio
import config
from aiogram import Bot, Dispatcher
from db_utils import db_commands
import logging
import warnings
from handlers import common

warnings.simplefilter("ignore", DeprecationWarning)


async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)

    # Создаем объект бота
    bot = Bot(token=config.token)

    # Диспечер
    dp = Dispatcher()

    #dp.include_router(career_choice.router)
    dp.include_router(common.router)

    await dp.start_polling(bot)


# Использование функции для инициализации базы данных

if __name__ == '__main__':
    db_commands.initialize_db(config.db_path)
    asyncio.run(main())
