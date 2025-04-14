from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, ContactViewSet

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
   path('', include(router.urls)),
]