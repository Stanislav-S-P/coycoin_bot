# Generated by Django 4.0.5 on 2022-06-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_coycoin', '0002_awardlist_image_tasklist_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='awardrequest',
            name='user_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='id пользователя'),
        ),
        migrations.AddField(
            model_name='coinrequest',
            name='user_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='id пользователя'),
        ),
    ]
