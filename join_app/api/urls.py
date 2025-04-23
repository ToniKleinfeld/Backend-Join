from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, ContactViewSet , TaskViewSet

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
   path('', include(router.urls)),
]