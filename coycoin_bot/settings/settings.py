"""
Файл содержащий Token бота
"""

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()


TOKEN = os.environ.get('TOKEN')
