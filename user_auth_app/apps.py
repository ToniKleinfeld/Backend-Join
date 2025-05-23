from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    """
    Läst Signal zu , wenn neuer User Erstellt wird ( Um Profile model hinzufügen zu können )
    """
    name = "user_auth_app"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import user_auth_app.signals
