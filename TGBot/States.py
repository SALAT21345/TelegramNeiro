
from aiogram.fsm.state import StatesGroup,State

class ChatGPT(StatesGroup):
    Model = State()
    Prompt = State()
    SendAnswer = State()

class Image(StatesGroup):
    SendImage = State()