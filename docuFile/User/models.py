from django.db import models

# Create your models here.
class certiRequest(models.Model):
    uid = models.CharField(max_length=100)
    iid = models.CharField(max_length=100)
    type = models.CharField(max_length=100)