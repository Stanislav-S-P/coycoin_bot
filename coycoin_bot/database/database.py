"""
Файл - взаимодействует с базой данных
"""


import sqlite3
from sqlite3 import Cursor
from typing import Tuple, List, Callable
from loader import logger


def db_decorator(func: Callable) -> Callable:
    """
    Декоратор - Производит подключение к БД.
    :param func: Callablе
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            connection = sqlite3.connect('../coycoin/db.sqlite3')
            connection.isolation_level = None
            cursor = connection.cursor()
            result = func(*args, **kwargs, cursor=cursor)
            return result
        except TypeError:
            pass
        except Exception as ex:
            logger.error('Ошибка БД', exc_info=ex)
            print(ex, 'Ошибка БД')
        finally:
            connection.close()
    return wrapped_func


"""Запросы к таблице bot_message"""


@db_decorator
def select_bot_message(variable: str, cursor: Cursor) -> str:
    cursor.execute("SELECT message FROM bot_message WHERE variable=?", (variable, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_images(variable: str, cursor: Cursor) -> str:
    cursor.execute("SELECT id FROM bot_message WHERE variable=?", (variable, ))
    message_id, *_ = cursor.fetchone()
    cursor.execute("SELECT image FROM images WHERE bot_message_id=?", (message_id, ))
    result, *_ = cursor.fetchone()
    return result


"""Запросы к таблице button_text"""


@db_decorator
def select_button_text(variable: str, cursor: Cursor) -> str:
    cursor.execute("SELECT message FROM button_text WHERE variable=?", (variable, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_all_button(cursor: Cursor) -> List:
    cursor.execute("SELECT message FROM button_text")
    variables = cursor.fetchall()
    result = []
    for elem in variables:
        result.append(elem[0])
    return result


"""Запросы к таблице user_list"""


@db_decorator
def select_user(user_id: int, cursor: Cursor) -> str:
    cursor.execute("SELECT id FROM user_list WHERE user_id=?", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def insert_user_list(user_tuple: Tuple, cursor: Cursor) -> None:
    cursor.execute(
        "INSERT INTO user_list (user_id, tg_account, full_name, change_at, coins) "
        "VALUES (?, ?, ?, ?, ?)", user_tuple
    )


@db_decorator
def select_user_coins(user_id: int, cursor: Cursor) -> int:
    cursor.execute("SELECT coins FROM user_list WHERE user_id=?", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_coin_desc(cursor: Cursor) -> List:
    cursor.execute("SELECT * FROM user_list ORDER BY coins DESC")
    result = cursor.fetchall()
    return result


@db_decorator
def select_coin_desc_limit(cursor: Cursor) -> List:
    cursor.execute("SELECT * FROM user_list ORDER BY coins DESC LIMIT 10")
    result = cursor.fetchall()
    return result


"""Запросы к таблице task_list"""


@db_decorator
def select_task_list(cursor: Cursor) -> List:
    cursor.execute("SELECT * FROM task_list WHERE status='Активна'")
    result = cursor.fetchall()
    return result


@db_decorator
def select_task_title(cursor: Cursor) -> List:
    cursor.execute("SELECT title FROM task_list WHERE status='Активна'")
    titles = cursor.fetchall()
    result = []
    for elem in titles:
        result.append(elem[0])
    return result


@db_decorator
def select_complete_task(title: str, cursor: Cursor) -> Tuple:
    cursor.execute("SELECT price, id FROM task_list WHERE title=?", (title, ))
    result, *_ = cursor.fetchall()
    return result


@db_decorator
def select_message_task(title: str, cursor: Cursor) -> str:
    cursor.execute("SELECT message FROM task_list WHERE title=?", (title, ))
    result, *_ = cursor.fetchone()
    return result


"""Запросы к таблице award_list"""


@db_decorator
def select_award_list(cursor: Cursor) -> List:
    cursor.execute("SELECT * FROM award_list WHERE status='Активна'")
    result = cursor.fetchall()
    return result


@db_decorator
def select_award_title(cursor: Cursor) -> List:
    cursor.execute("SELECT title FROM award_list WHERE status='Активна'")
    titles = cursor.fetchall()
    result = []
    for elem in titles:
        result.append(elem[0])
    return result


@db_decorator
def select_award_city(title: str, cursor: Cursor) -> str:
    cursor.execute("SELECT cities FROM award_list WHERE title=?", (title, ))
    cities, *_ = cursor.fetchone()
    return cities


@db_decorator
def select_all_city(cursor: Cursor) -> List:
    cursor.execute("SELECT cities FROM award_list WHERE status='Активна'")
    cities = cursor.fetchall()
    result = []
    for elem in cities:
        elem = elem[0].split(',')
        result.extend(elem)
    return result


@db_decorator
def select_complete_award(title: str, cursor: Cursor) -> Tuple:
    cursor.execute("SELECT price, id FROM award_list WHERE title=?", (title, ))
    result, *_ = cursor.fetchall()
    return result


@db_decorator
def diff_coins(user_id: int, title: str, cursor: Cursor) -> bool:
    cursor.execute("SELECT coins FROM user_list WHERE user_id=?", (user_id, ))
    coins, *_ = cursor.fetchone()
    cursor.execute("SELECT price FROM award_list WHERE title=?", (title, ))
    price, *_ = cursor.fetchone()
    if coins - price >= 0:
        return True


"""Запросы к таблице coin_request"""


@db_decorator
def insert_coin_request(coin_request_tuple: Tuple, cursor: Cursor) -> None:
    cursor.execute(
        "INSERT INTO coin_request (tg_account, created_at, link, description, quantity_coins, status, task_id, user_id)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", coin_request_tuple
    )


"""Запросы к таблице award_request"""


@db_decorator
def insert_award_request(award_request_tuple: Tuple, cursor: Cursor) -> None:
    cursor.execute(
        "INSERT INTO award_request (tg_account, cities, created_at, add_information, price, status, award_id, user_id)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", award_request_tuple
    )
