# Generated by Django 3.2.8 on 2021-10-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewrequest',
            name='iid',
        ),
        migrations.AddField(
            model_name='viewrequest',
            name='ifirst',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='viewrequest',
            name='ilast',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
