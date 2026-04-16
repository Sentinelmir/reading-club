from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'Reading_Club.accounts'

    def ready(self):
        import Reading_Club.accounts.signals
