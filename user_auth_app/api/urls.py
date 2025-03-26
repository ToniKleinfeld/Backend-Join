from django.urls import path
from .views import RegestrationView , CustomLoginView

urlpatterns = [
    path("registration/", RegestrationView.as_view(), name="regestration"),
    path("login/", CustomLoginView.as_view(), name="custom-login"),
]