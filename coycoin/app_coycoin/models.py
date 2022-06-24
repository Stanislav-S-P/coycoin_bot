from django.db import models


class UserList(models.Model):
    """
    Класс - модель таблицы user_list, хранит информацию о пользователях.
    """
    user_id = models.BigIntegerField(null=True, blank=True, verbose_name='id пользователя')
    tg_account = models.CharField(max_length=50, verbose_name='TG аккаунт')
    full_name = models.CharField(max_length=70, verbose_name='Ф.И.О.')
    change_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения баланса')
    coins = models.IntegerField(default=0, verbose_name='Кол-во коинов')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        db_table = 'user_list'
        ordering = ['-coins']


class TaskList(models.Model):
    """
    Класс - модель таблицы task_list, хранит информацию о заданиях.
    """
    STATUS_TASK = [
        ('Не активна', 'Не активна'),
        ('Активна', 'Активна')
    ]

    title = models.CharField(max_length=500, verbose_name='Название')
    description = models.CharField(max_length=2000, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Стоимость')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    status = models.CharField(max_length=20, choices=STATUS_TASK, default='Не активна', verbose_name='Статус')
    message = models.TextField(blank=True, null=True, verbose_name='Сообщение')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        db_table = 'task_list'


class AwardList(models.Model):
    """
    Класс - модель таблицы award_list, хранит информацию о призах.
    """
    STATUS_AWARD = [
        ('Не активна', 'Не активна'),
        ('Активна', 'Активна')
    ]

    title = models.CharField(max_length=500, verbose_name='Название')
    description = models.CharField(max_length=2000, verbose_name='Описание')
    cities = models.CharField(max_length=150, verbose_name='Город получения')
    price = models.IntegerField(verbose_name='Стоимость')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    status = models.CharField(max_length=20, choices=STATUS_AWARD, default='Не активна', verbose_name='Статус')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = 'Призы'
        db_table = 'award_list'
        ordering = ['price']


class AwardRequest(models.Model):
    """
    Класс - модель таблицы award_request, хранит информацию о запросах на получение призов.
    """
    CHOICE_AWARD = [
        ('Новый запрос', 'Новый запрос'),
        ('Обработка', 'Обработка'),
        ('Выполнено', 'Выполнено')
    ]

    tg_account = models.CharField(max_length=50, verbose_name='TG аккаунт')
    cities = models.CharField(max_length=50, verbose_name='Город получения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')
    add_information = models.TextField(verbose_name='Дополнительная информация')
    award = models.ForeignKey(AwardList, on_delete=models.CASCADE, related_name='award_request', verbose_name='Приз')
    price = models.IntegerField(verbose_name='Стоимость')
    status = models.CharField(max_length=20, choices=CHOICE_AWARD, default='Новый запрос', verbose_name='Статус')
    user_id = models.BigIntegerField(null=True, blank=True, verbose_name='id пользователя')

    class Meta:
        verbose_name = 'Заявка на получение приза'
        verbose_name_plural = 'Заявки на получение призов'
        db_table = 'award_request'
        ordering = ['-status']


class CoinRequest(models.Model):
    """
    Класс - модель таблицы award_request, хранит информацию о запросах на получение коинов.
    """
    CHOICE_COIN = [
        ('Обработка', 'Обработка'),
        ('Выполнено', 'Выполнено')
    ]

    tg_account = models.CharField(max_length=50, verbose_name='TG аккаунт')
    task = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='coin_request', verbose_name='Задание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')
    link = models.CharField(max_length=200, verbose_name='Ссылка')
    description = models.CharField(max_length=2000, verbose_name='Описание')
    quantity_coins = models.IntegerField(verbose_name='Кол-во коинов')
    status = models.CharField(max_length=20, choices=CHOICE_COIN, default='Обработка', verbose_name='Статус')
    user_id = models.BigIntegerField(null=True, blank=True, verbose_name='id пользователя')

    class Meta:
        verbose_name = 'Заявка на получение коинов'
        verbose_name_plural = 'Заявки на получение коинов'
        db_table = 'coin_request'
        ordering = ['-status']
