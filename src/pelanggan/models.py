from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(User):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email

# class Profile(AbstractUser):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nama = models.CharField(blank=True, max_length=255)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)


#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()

#     def update_profile(request, user_id):
#         user = User.objects.get(pk=user_id)
#         user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#         user.save()