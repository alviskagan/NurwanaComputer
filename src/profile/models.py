from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# Create your models here.
class Pelanggan(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address = models.CharField(max_length = 250, null = True)
    phone_number = models.CharField(max_length = 250)
    bio = models.TextField(max_length=250)
    birth_date = models.DateField(null=True, default = "1997-01-29")
    postal_code = models.CharField(max_length= 10, null = True)
    def content_file_name(instance, filename):
        ext 		= filename.split('.')[-1]
        filename 	= "%s.%s" % (instance.user, ext)
        return os.path.join('profile', filename)   
    profile_pic 	= models.FileField(upload_to= content_file_name ,null = True, blank = True)
