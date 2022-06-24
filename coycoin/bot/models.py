from django.db import models


class BotMessage(models.Model):
    """
    Класс - модель таблицы bot_message, хранит сообщения бота.
    """
    variable = models.CharField(max_length=30, verbose_name='Переменная')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f"{self.variable}"

    class Meta:
        verbose_name = 'Сообщение бота'
        verbose_name_plural = 'Сообщения бота'
        db_table = 'bot_message'


class ButtonText(models.Model):
    """
    Класс - модель таблицы button_text, хранит текста кнопок бота.
    """
    variable = models.CharField(max_length=30, verbose_name='Переменная')
    message = models.TextField(verbose_name='Сообщение')

    class Meta:
        verbose_name = 'Текст кнопки'
        verbose_name_plural = 'Текста кнопок'
        db_table = 'button_text'


class Images(models.Model):
    """
    Класс - модель таблицы images, хранит изображения к сообщениям.
    """
    bot_message = models.ForeignKey(
        BotMessage, related_name='images', on_delete=models.CASCADE, verbose_name='Сообщение'
    )
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        db_table = 'images'
