from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # Import the signals inside the ready function
    def ready(self):
        import users.signals
