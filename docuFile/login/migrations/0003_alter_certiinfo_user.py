# Generated by Django 3.2.8 on 2021-10-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20211012_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certiinfo',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]