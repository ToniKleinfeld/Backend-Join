from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    name = "user_auth_app"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import user_auth_app.signals
