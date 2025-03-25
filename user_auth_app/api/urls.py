from django.urls import path
from .views import UserProfileList, UserProfileDetail , RegestrationView , CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("profiles/", UserProfileList.as_view(), name="userprofile-list"),
    path("profiles/<int:pk>/", UserProfileDetail.as_view(), name="userprofile-detail"),
    path("registration/", RegestrationView.as_view(), name="regestration"),
    # path("login/", obtain_auth_token, name="login"),
    path("login/", CustomLoginView.as_view(), name="custom-login"),
]