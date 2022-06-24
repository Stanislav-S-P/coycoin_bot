from aiogram import Dispatcher, types
from database.database import select_button_text, select_user_coins, select_coin_desc, select_coin_desc_limit
from handlers.echo import custom_message_keyboard, custom_my_result, custom_message, custom_top_result
from keyboards.keyboards import result_keyboard
from loader import logger


async def result_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду results
    :param message: Message
    :return: None
    """
    try:
        await custom_message_keyboard(message, 'result_menu', result_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def my_result_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю my_result
    :param message: Message
    :return: None
    """
    try:
        coins = select_user_coins(message.from_user.id)
        user_list = select_coin_desc()
        index = 0
        print(user_list)
        for elem in user_list:
            index += 1
            if elem[1] == message.from_user.id:
                break
        await custom_my_result(message, 'my_coins', coins)
        await custom_my_result(message, 'my_place', index)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def best_result_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает кнопку подменю best_result
    :param message: Message
    :return: None
    """
    try:
        top_list = select_coin_desc_limit()
        await custom_message(message, 'top_result_head')
        for index, elem in enumerate(top_list):
            username = elem[2][: -3] + '***'
            if index == 0:
                template = '🥇'
            elif index == 1:
                template = '🥈'
            elif index == 2:
                template = '🥉'
            else:
                template = index + 1
            await custom_top_result(message, template, username, elem[5])
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_result_handlers(dp: Dispatcher):
    """
     Функция - регистрирует все хэндлеры файла result.py
     :param dp: Dispatcher
     :return: None
     """
    dp.register_message_handler(result_handler, commands=['results'], state=None)
    dp.register_message_handler(
        result_handler, lambda message: message.text == select_button_text('results'), state=None
    )
    dp.register_message_handler(
        my_result_handler, lambda message: message.text == select_button_text('my_result'), state=None
    )
    dp.register_message_handler(
        best_result_handler, lambda message: message.text == select_button_text('best_result'), state=None
    )
