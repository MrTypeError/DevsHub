# from django.apps import AppConfig


# class ProjectsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'projects'


from django.apps import AppConfig
from django.db import connection

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    def ready(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA journal_mode=WAL;')
        except Exception as e:
            print("Could not enable WAL mode:", e)
