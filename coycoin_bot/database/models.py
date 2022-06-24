"""
Файл с моделями машины состояний
"""


from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUserList(StatesGroup):
    full_name = State()


class FSMTask(StatesGroup):
    task = State()
    link = State()
    description = State()


class FSMShop(StatesGroup):
    award = State()
    city = State()
    add_information = State()
