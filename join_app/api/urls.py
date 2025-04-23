from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, ContactViewSet , TaskViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
   path('', include(router.urls)),
       path(
        "tasks/<int:task_pk>/subtasks/",
        SubTaskViewSet.as_view({"get": "list", "post": "create"}),
        name="task-subtask-list"
    ),
    path(
        "tasks/<int:task_pk>/subtasks/<int:pk>/",
        SubTaskViewSet.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "put": "update",
            "delete": "destroy"
        }),
        name="task-subtask-detail"
    ),
]