from aiogram.fsm.state import StatesGroup, State

class Settings(StatesGroup):
    choosing_language = State()
    choosing_frequency = State()
    choosing_size = State()
