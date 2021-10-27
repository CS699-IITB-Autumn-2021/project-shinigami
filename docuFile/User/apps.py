from django.apps import AppConfig

# configuring the name field
class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'
