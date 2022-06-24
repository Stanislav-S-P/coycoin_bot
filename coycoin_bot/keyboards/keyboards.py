"""
Файл с клавиатурами бота
"""


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import select_button_text, select_award_city


def start_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция - создаёт Reply клавиатуру главного меню.
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key_help = KeyboardButton(text=select_button_text('help'))
    key_tasks = KeyboardButton(text=select_button_text('tasks'))
    key_shop = KeyboardButton(text=select_button_text('shop'))
    key_results = KeyboardButton(text=select_button_text('results'))
    return keyboards.add(key_tasks, key_shop, key_results, key_help)


def help_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция - создаёт Reply клавиатуру подменю help.
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key_help_task = KeyboardButton(text=select_button_text('help_task'))
    key_help_shop = KeyboardButton(text=select_button_text('help_shop'))
    key_help_result = KeyboardButton(text=select_button_text('help_result'))
    key_back = KeyboardButton(text=select_button_text('back'))
    return keyboards.add(key_help_task, key_help_result, key_back, key_help_shop)


def task_keyboard(title: str) -> InlineKeyboardMarkup:
    """
    Функция - создаёт Inline клавиатуру выполнения задания.
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=1)
    btn = select_button_text('task_complete')
    key = InlineKeyboardButton(text=btn, callback_data=title)
    return keyboards.add(key)


def award_keyboard(title: str) -> InlineKeyboardMarkup:
    """
    Функция - создаёт Inline клавиатуру получения приза.
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=1)
    btn = select_button_text('buy_award')
    key = InlineKeyboardButton(text=btn, callback_data=title)
    return keyboards.add(key)


def city_keyboard(title: str) -> InlineKeyboardMarkup:
    """
    Функция - создаёт Inline клавиатуру выбора города получения приза.
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=2)
    cities = select_award_city(title)
    for city in cities.split(','):
        keyboards.add(InlineKeyboardButton(text=city, callback_data=city))
    return keyboards


def result_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция - создаёт Reply клавиатуру подменю result.
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    my_result = KeyboardButton(text=select_button_text('my_result'))
    best_result = KeyboardButton(text=select_button_text('best_result'))
    key_back = KeyboardButton(text=select_button_text('back'))
    return keyboards.add(my_result, best_result, key_back)
