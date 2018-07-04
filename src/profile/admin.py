from django.contrib import admin
from .models import Pelanggan
from django.contrib.auth.models import User
# Register your models here.

class PelangganAdmin(admin.ModelAdmin):
    list_display = ('user','address','phone_number','bio','birth_date','profile_pic')

admin.site.register(Pelanggan, PelangganAdmin)