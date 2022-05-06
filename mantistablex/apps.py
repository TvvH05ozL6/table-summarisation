from django.apps import AppConfig


class MantistablexConfig(AppConfig):
    name = 'mantistablex'
    def ready(self):
        import mantistablex.signals
