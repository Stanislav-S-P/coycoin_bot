import os
from typing import Union
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from database.database import select_bot_message, select_images
from loader import bot, logger


async def custom_message_keyboard(message, variable: str, keyboards_func: ReplyKeyboardMarkup) -> None:
    """
    Функция - шаблон для отправки сообщений с Reply клавиатурой.
    :param message: Message
    :param variable: str
    :param keyboards_func: ReplyKeyboardMarkup
    :return: None
    """
    image = select_images(variable)
    if image:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', image))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=select_bot_message(variable),
            reply_markup=keyboards_func,
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id, select_bot_message(variable), reply_markup=keyboards_func, parse_mode='Markdown'
        )


async def custom_message(message, variable: str) -> None:
    """
    Функция - шаблон для отправки сообщений без клавиатуры.
    :param message: Message
    :param variable: str
    :return: None
    """
    image = select_images(variable)
    if image:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', image))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=select_bot_message(variable),
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id, select_bot_message(variable), parse_mode='Markdown'
        )


async def custom_task_message(message, variable: str) -> None:
    """
    Функция - шаблон для отправки сообщений с запросом ссылки, телеграм-ника.
    :param message: Message
    :param variable: str
    :return: None
    """
    await bot.send_message(
        message.from_user.id, variable, parse_mode='Markdown'
    )


async def custom_task_message_keyboard(message, record, keyboards_func: InlineKeyboardMarkup) -> None:
    """
    Функция - шаблон для отправки сообщений списка заданий.
    :param message: Message
    :param record: Tuple
    :param keyboards_func: InlineKeyboardMarkup
    :return: None
    """
    if record[5]:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', record[5]))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=f'*{record[1]}*\n{record[2]}\n\nНаграда: {record[3]} коинов',
            reply_markup=keyboards_func,
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f'*{record[1]}*\n{record[2]}\n\nНаграда: {record[3]} коинов',
            reply_markup=keyboards_func, parse_mode='Markdown'
        )


async def custom_award_message_keyboard(message, record, keyboards_func: InlineKeyboardMarkup) -> None:
    """
    Функция - шаблон для отправки сообщений списка призов.
    :param message: Message
    :param record: Tuple
    :param keyboards_func: InlineKeyboardMarkup
    :return: None
    """
    if record[6]:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', record[6]))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=f'*{record[1]}*\n{record[2]}\n\nДоступен в: {record[3]}\n Стоимость: {record[4]} коинов',
            reply_markup=keyboards_func,
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f'*{record[1]}*\n{record[2]}\n\nДоступен в: {record[3]}\n Стоимость: {record[4]} коинов',
            reply_markup=keyboards_func, parse_mode='Markdown'
        )


async def custom_city_message(message, variable: str, keyboards_func: InlineKeyboardMarkup) -> None:
    """
    Функция - шаблон для отправки клавиатуры со списком городов.
    :param message: Message
    :param variable: str
    :param keyboards_func: InlineKeyboardMarkup
    :return: None
    """
    image = select_images(variable)
    if image:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', image))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=select_bot_message(variable),
            reply_markup=keyboards_func,
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id, select_bot_message(variable), reply_markup=keyboards_func, parse_mode='Markdown'
        )


async def custom_my_result(message, variable: str, index: int) -> None:
    """
    Функция - шаблон для отправки сообщения с результатом пользователя.
    :param message: Message
    :param variable: str
    :param index: int
    :return: None
    """
    image = select_images(variable)
    if image:
        path_photo = os.path.abspath(os.path.join('../coycoin/media/', image))
        await bot.send_photo(
            message.from_user.id,
            photo=open(path_photo, 'rb'),
            caption=select_bot_message(variable).format(index),
            parse_mode='Markdown'
        )
    else:
        await bot.send_message(
            message.from_user.id, select_bot_message(variable).format(index), parse_mode='Markdown'
        )


async def custom_top_result(message, index: Union[str, int], username: str, coins: int) -> None:
    """
    Функция - шаблон для отправки сообщений лидеров таблицы.
    :param message: Message
    :param index: Union[str, int]
    :param username: str
    :param coins: int
    :return: None
    """
    await bot.send_message(
        message.from_user.id, '{} | {} | {}'.format(index, username, coins)
    )


async def echo_handler(message: types.Message) -> None:
    """
    Хэндлер - оповещает бота о некорректной команде (Эхо)
    :param message: Message
    :return: None
    """
    try:
        await custom_message(message, 'incorrect_input')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_echo_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла echo.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(echo_handler)
