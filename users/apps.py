from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Import signals to ensure they are registered when the app is ready.
        This is necessary for the signal handlers to work correctly.
        """
        import users.signals
