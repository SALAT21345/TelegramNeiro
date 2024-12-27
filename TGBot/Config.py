from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
token = '7052647638:AAGzBpl65HjA0olywqzsQHt7pNH0cD9LNUQ'
bot = Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))