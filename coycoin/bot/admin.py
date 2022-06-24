from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *


class BotMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'variable', 'message']
    list_display_links = ['id', 'variable', 'message']


class ButtonTextAdmin(admin.ModelAdmin):
    list_display = ['id', 'variable', 'message']
    list_display_links = ['id', 'variable', 'message']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'bot_message', 'image']
    list_display_links = ['id', 'bot_message', 'image']


admin.site.register(BotMessage, BotMessageAdmin)
admin.site.register(ButtonText, ButtonTextAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
