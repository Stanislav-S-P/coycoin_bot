from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from database.database import select_button_text, select_task_list, select_task_title, select_all_button, \
    insert_coin_request, select_complete_task, select_message_task
from database.models import FSMTask
from handlers.echo import custom_task_message_keyboard, custom_message, custom_task_message
from handlers.result import result_handler, my_result_handler, best_result_handler
from handlers.shop import shop_handler
from handlers.start import start_handler, help_handler, back_handler, help_task_handler, help_shop_handler, \
    help_result_handler
from keyboards.keyboards import task_keyboard
from loader import logger


async def tasks_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду tasks, входит в машину состояния FSMTask
    :param message: Message
    :return: None
    """
    try:
        for task in select_task_list():
            await custom_task_message_keyboard(message, task, task_keyboard(task[1]))
        await FSMTask.task.set()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def callback_task_handler(call: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMTask.task
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['tg_account'] = call.from_user.username
            data['task'] = call.data
        await FSMTask.next()
        task_message = select_message_task(call.data)
        await custom_task_message(call, task_message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def link_state_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMTask.link
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['link'] = message.text
        await FSMTask.next()
        await custom_message(message, 'task_description')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def description_state_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние FSMTask.description
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            created_at = datetime.today()
            task = select_complete_task(data['task'])
            insert_coin_request(
                (data['tg_account'], created_at, data['link'], message.text, task[0],
                    'Обработка', task[1], message.from_user.id)
            )
        await custom_message(message, 'task_complete')
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def cancel_tasks(message: types.Message, state: FSMContext) -> None:
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
        await tasks_handler(message)
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


def register_tasks_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла tasks.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(
        cancel_tasks, Text(startswith=['/start', '/help', '/tasks', '/shop', '/result']), state='*'
    )
    dp.register_message_handler(cancel_tasks, Text(startswith=select_all_button()), state='*')
    dp.register_message_handler(tasks_handler, commands=['tasks'], state=None)
    dp.register_message_handler(tasks_handler, lambda message: message.text == select_button_text('tasks'), state=None)
    dp.register_callback_query_handler(
        callback_task_handler, lambda call: call.data in select_task_title(), state=FSMTask.task
    )
    dp.register_message_handler(link_state_handler, content_types=['text'], state=FSMTask.link)
    dp.register_message_handler(description_state_handler, content_types=['text'], state=FSMTask.description)
