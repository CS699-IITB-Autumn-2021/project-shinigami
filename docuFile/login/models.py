from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class UserType(models.Model):
    user_type = models.CharField(max_length=100, blank=True)
    user_name =models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

class CertiInfo(models.Model):
    user = models.CharField(max_length=100)
    insti = models.CharField(max_length=100)
    certi = models.FileField()
    type = models.CharField(max_length=100)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserType.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usertype.save()

@receiver(post_save, sender=User)
def create_user_certi(sender, instance, created, **kwargs):
    if created:
        CertiInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_certi(sender, instance, **kwargs):
    instance.usertype.save()