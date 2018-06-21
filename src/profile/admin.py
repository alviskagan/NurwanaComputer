from django.contrib import admin
from .models import Customer
from django.contrib.auth.models import User
# Register your models here.

class CutomerAdmin(admin.ModelAdmin):
    list_display = ('user','address','phone_number','bio','birth_date')

admin.site.register(Customer, CutomerAdmin)