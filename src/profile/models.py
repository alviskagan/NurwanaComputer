from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Customer(models.Model):
    '''
    The Customer model represents a customer of the online store. 
    It extends Django's built-in auth.User model, which contains information such as first and last name, 
    and e-mail, and adds phone number and address information.
    '''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address = models.CharField(max_length = 250, default = "-")
    phone_number = models.CharField(max_length = 250, default = "-")
    bio = models.TextField(max_length=250, default = "-")
    birth_date = models.DateField(null=True,  default = "-")


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)

# @receiver(user_signed_up)
# def user_signed_up_(request, user, sociallogin=None, **kwargs):
#         print(user)
#         Customer.objects.create(user)
#         user.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print(User)
#     instance.User.save()