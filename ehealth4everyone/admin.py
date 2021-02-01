from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import User

# Register your models here.

class profileAdmin(admin.ModelAdmin):
    search_fields = ['user__user__email', 'age', 'sex','blood_group','genotype']
    list_display = ['user', 'age', 'sex','blood_group', 'genotype', 'height','weight','nationality']
    list_filter = ('age', 'sex',)
   




admin.site.register(User, UserAdmin)
admin.register(Profile, profileAdmin)
