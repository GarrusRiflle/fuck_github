# -*- coding: utf-8 -*-
from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


#class UserAdmin(BaseUserAdmin):
    #def admin_avatar(self, instance):
    #    return instance.avatar and u'<img src="{0}" width="100px" />'.format(
    #        instance.avatar.url
    #    )
    #admin_avatar.allow_tags = True
    #admin_avatar.short_description = 'Avatar'


admin.site.register(User)
#admin.site.register(UserAdmin)