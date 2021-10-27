from django.db import models

# model contains the user id, institute id, and type field
class certiRequest(models.Model):
    uid = models.CharField(max_length=100)
    iid = models.CharField(max_length=100)
    type = models.CharField(max_length=100)