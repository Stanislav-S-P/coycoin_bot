from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from.models import *


class UserListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'tg_account', 'full_name', 'change_at', 'coins']
    list_display_links = ['id', 'user_id', 'tg_account', 'full_name', 'change_at', 'coins']
    list_filter = ['coins']
    search_fields = ['full_name']


class TaskListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'show_description', 'price', 'image', 'status']
    list_display_links = ['id', 'title', 'show_description', 'price', 'image', 'status']
    list_filter = ['title']

    actions = ['mark_as_active', 'mark_as_no_active']

    def mark_as_active(self, request, queryset):
        queryset.update(status='Активна')

    def mark_as_no_active(self, request, queryset):
        queryset.update(status='Не активна')

    mark_as_active.short_description = 'Перевести в статус Активна'
    mark_as_no_active.short_description = 'Перевести в статус Не активна'

    def show_description(self, obj):
        return truncatechars(obj.description, 40)
    show_description.short_description = 'Описание'


class AwardListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'show_description', 'cities', 'price', 'image', 'status']
    list_display_links = ['id', 'title', 'show_description', 'cities', 'price', 'image', 'status']
    list_filter = ['title', 'status']

    actions = ['mark_as_active', 'mark_as_no_active']

    def mark_as_active(self, request, queryset):
        queryset.update(status='Активна')

    def mark_as_no_active(self, request, queryset):
        queryset.update(status='Не активна')

    mark_as_active.short_description = 'Перевести в статус Активна'
    mark_as_no_active.short_description = 'Перевести в статус Не активна'

    def show_description(self, obj):
        return truncatechars(obj.description, 40)
    show_description.short_description = 'Описание'


class AwardRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_account', 'cities', 'created_at', 'show_information', 'award', 'price', 'status']
    list_display_links = ['id', 'tg_account', 'cities', 'created_at', 'show_information', 'award', 'price', 'status']
    list_filter = ['created_at', 'award', 'status']
    search_fields = ['cities']

    actions = ['mark_as_active', 'mark_as_no_active', 'mark_as_new_request']

    def mark_as_active(self, request, queryset):
        for elem in queryset:
            user_id = elem.user_id
            price = elem.price
            i_user = UserList.objects.filter(user_id=user_id)
            coins = i_user.get().coins
            i_user.update(coins=coins - price)
            i_user.update(change_at=datetime.today())
            elem.status = 'Выполнено'
            elem.save()

    def mark_as_no_active(self, request, queryset):
        queryset.update(status='Обработка')

    def mark_as_new_request(self, request, queryset):
        queryset.update(status='Новый запрос')

    mark_as_active.short_description = 'Перевести в статус Выполнено'
    mark_as_no_active.short_description = 'Перевести в статус Обработка'
    mark_as_new_request.short_description = 'Перевести в статус Новый запрос'

    def show_information(self, obj):
        return truncatechars(obj.add_information, 40)
    show_information.short_description = 'Доп. информация'


class CoinRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_account', 'task', 'created_at', 'link', 'show_description', 'quantity_coins', 'status']
    list_display_links = [
        'id', 'tg_account', 'task', 'created_at', 'link', 'show_description', 'quantity_coins', 'status'
    ]
    list_filter = ['created_at', 'status', 'task']
    search_fields = ['task']

    actions = ['mark_as_active', 'mark_as_no_active']

    def mark_as_active(self, request, queryset):
        for elem in queryset:
            user_id = elem.user_id
            quantity_coins = elem.quantity_coins
            i_user = UserList.objects.filter(user_id=user_id)
            coins = i_user.get().coins
            i_user.update(coins=coins + quantity_coins)
            i_user.update(change_at=datetime.today())
            elem.status = 'Выполнено'
            elem.save()

    def mark_as_no_active(self, request, queryset):
        queryset.update(status='Обработка')

    mark_as_active.short_description = 'Перевести в статус Выполнено'
    mark_as_no_active.short_description = 'Перевести в статус Обработка'

    def show_description(self, obj):
        return truncatechars(obj.description, 40)
    show_description.short_description = 'Описание'


admin.site.register(UserList, UserListAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(AwardList, AwardListAdmin)
admin.site.register(AwardRequest, AwardRequestAdmin)
admin.site.register(CoinRequest, CoinRequestAdmin)
