from django.urls import path
from .views import RegestrationView , CustomLoginView, LogoutView ,VerifyTokenView

urlpatterns = [
    path("registration/", RegestrationView.as_view(), name="regestration"),
    path("login/", CustomLoginView.as_view(), name="custom-login"),
    path("verify/", VerifyTokenView.as_view(), name="token-verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
]