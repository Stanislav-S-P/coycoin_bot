"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""


from loader import dp
from aiogram.utils import executor
from handlers import start, echo, tasks, shop, result


start.register_start_handlers(dp)
tasks.register_tasks_handlers(dp)
shop.register_shop_handlers(dp)
result.register_result_handlers(dp)
echo.register_echo_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
