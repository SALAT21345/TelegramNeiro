import Config as CFG
import handlers.MainHandlers as MH

from aiogram import Dispatcher 
import asyncio
from aiogram.filters import CommandStart

# Создание экземпляра Dispatcher
dp = Dispatcher()

async def main():
    dp.include_routers(MH.router)
    await dp.start_polling(CFG.bot)

# Правильная проверка имени
if __name__ == '__main__':
    asyncio.run(main())
