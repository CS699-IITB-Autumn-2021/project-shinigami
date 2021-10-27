from django.db import models

# Create firstname, lastname, userid models
class viewRequest(models.Model):
    ifirst = models.CharField(max_length=100)
    ilast = models.CharField(max_length=100)
    uid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)