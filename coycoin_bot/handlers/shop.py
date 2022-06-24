from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.database import select_award_list, select_button_text, select_award_title, select_all_city, \
    insert_award_request, select_complete_award, select_all_button, diff_coins
from database.models import FSMShop
from handlers.echo import custom_city_message, custom_award_message_keyboard, custom_message
from handlers.result import my_result_handler, best_result_handler, result_handler
from handlers.start import start_handler, help_handler, back_handler, help_task_handler, help_shop_handler, \
    help_result_handler
from handlers import tasks
from keyboards.keyboards import award_keyboard, city_keyboard
from loader import logger


async def shop_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду shop, входит в машину состояния FSMShop
    :param message: Message
    :return: None
    """
    try:
        for product in select_award_list():
            await custom_award_message_keyboard(message, product, award_keyboard(product[1]))
        await FSMShop.award.set()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def callback_shop_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMUserList.award
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        if diff_coins(call.from_user.id, call.data):
            async with state.proxy() as data:
                data['tg_account'] = call.from_user.username
                data['award'] = call.data
            await FSMShop.next()
            await custom_city_message(call, 'choice_city', city_keyboard(call.data))
        else:
            await custom_message(call, 'not_enough_coins')
            await state.finish()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def callback_city_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMUserList.city
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['city'] = call.data
        await FSMShop.next()
        await custom_message(call, 'add_information')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def add_info_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMUserList.add_information
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            created_at = datetime.today()
            award = select_complete_award(data['award'])
            insert_award_request(
                (data['tg_account'], data['city'], created_at, message.text,
                 award[0], 'Обработка', award[1], message.from_user.id)
            )
        await custom_message(message, 'award_complete')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def cancel_shop(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - реагирует на команды и выводит из машины состояния пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    if message.text == '/start':
        await start_handler(message)
    elif message.text == '/help' or message.text == select_button_text('help'):
        await help_handler(message)
    elif message.text == '/tasks' or message.text == select_button_text('tasks'):
        await tasks.tasks_handler(message)
    elif message.text == '/shop' or message.text == select_button_text('shop'):
        await shop_handler(message)
    elif message.text == '/results' or message.text == select_button_text('results'):
        await result_handler(message)
    elif message.text == select_button_text('back'):
        await back_handler(message)
    elif message.text == select_button_text('help_task'):
        await help_task_handler(message)
    elif message.text == select_button_text('help_shop'):
        await help_shop_handler(message)
    elif message.text == select_button_text('help_result'):
        await help_result_handler(message)
    elif message.text == select_button_text('my_result'):
        await my_result_handler(message)
    elif message.text == select_button_text('best_result'):
        await best_result_handler(message)


def register_shop_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла shop.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(
        cancel_shop, Text(startswith=['/start', '/help', '/tasks', '/shop', '/result']), state='*'
    )
    dp.register_message_handler(cancel_shop, Text(startswith=select_all_button()), state='*')
    dp.register_message_handler(shop_handler, commands=['shop'], state=None)
    dp.register_message_handler(shop_handler, lambda message: message.text == select_button_text('shop'), state=None)
    dp.register_callback_query_handler(
        callback_shop_handler, lambda call: call.data in select_award_title(), state=FSMShop.award
    )
    dp.register_callback_query_handler(
        callback_city_handler, lambda call: call.data in select_all_city(), state=FSMShop.city
    )
    dp.register_message_handler(add_info_handler, content_types=['text'], state=FSMShop.add_information)
