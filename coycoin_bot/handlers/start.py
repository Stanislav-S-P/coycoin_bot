from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.models import FSMUserList
from handlers.echo import custom_message_keyboard, custom_message
from database.database import select_button_text, select_user, insert_user_list
from keyboards.keyboards import start_menu_keyboard, help_keyboard
from loader import logger


async def start_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду start
    :param message: Message
    :return: None
    """
    try:
        await custom_message(message, 'welcome')
        if select_user(message.from_user.id):
            await custom_message_keyboard(message, 'menu', start_menu_keyboard())
        else:
            await FSMUserList.full_name.set()
            await custom_message(message, 'full_name')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def full_name_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMUserList.full_name
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if message.text.isalpha() and message.text not in ['/start', '/help', '/tasks', '/shop', '/result']:
            await state.finish()
            data = datetime.today()
            insert_user_list((message.from_user.id, message.from_user.username, message.text, data, 0))
            await custom_message_keyboard(message, 'menu', start_menu_keyboard())
        else:
            await custom_message(message, 'incorrect_name')
            await custom_message(message, 'full_name')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду help
    :param message: Message
    :return: None
    """
    try:
        await custom_message_keyboard(message, 'help', help_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_task_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю help_task
    :param message: Message
    :return: None
    """
    try:
        await custom_message(message, 'help_task')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_shop_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю help_shop
    :param message: Message
    :return: None
    """
    try:
        await custom_message(message, 'help_shop')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_result_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю help_result
    :param message: Message
    :return: None
    """
    try:
        await custom_message(message, 'help_result')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def back_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю back
    :param message: Message
    :return: None
    """
    try:
        await custom_message_keyboard(message, 'menu', start_menu_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_start_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла start.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(start_handler, commands=['start'], state=None)
    dp.register_message_handler(help_handler, commands=['help'], state=None)
    dp.register_message_handler(help_handler, lambda message: message.text == select_button_text('help'), state=None)
    dp.register_message_handler(full_name_handler, content_types=['text'], state=FSMUserList.full_name)
    dp.register_message_handler(
        help_task_handler, lambda message: message.text == select_button_text('help_task'), state=None
    )
    dp.register_message_handler(
        help_shop_handler, lambda message: message.text == select_button_text('help_shop'), state=None
    )
    dp.register_message_handler(
        help_result_handler, lambda message: message.text == select_button_text('help_result'), state=None
    )
    dp.register_message_handler(back_handler, lambda message: message.text == select_button_text('back'), state=None)
