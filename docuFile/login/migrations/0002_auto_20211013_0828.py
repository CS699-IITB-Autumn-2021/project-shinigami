# Generated by Django 3.2.8 on 2021-10-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certiinfo',
            name='user_name',
        ),
        migrations.AddField(
            model_name='certiinfo',
            name='type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='certiinfo',
            name='certi',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='certiinfo',
            name='user',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
