from django.urls import path
from .views import RegestrationView , CustomLoginView, LogoutView ,VerifyTokenView, PingCookieView

urlpatterns = [
    path("registration/", RegestrationView.as_view(), name="regestration"),
    path("login/", CustomLoginView.as_view(), name="custom-login"),
    path("verify/", VerifyTokenView.as_view(), name="token-verify"),
    path("ping-cookie/", PingCookieView.as_view(), name="ping-cookie"),
    path("logout/", LogoutView.as_view(), name="logout"),
]