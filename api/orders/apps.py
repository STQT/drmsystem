from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'orders'

    def ready(self):
        import orders.signals # noqa
