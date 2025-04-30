# TODO: JOIN Django / DRF Backend

## 📦 Models

- [x] `User` (Built-in oder CustomUser)
- [x] `Contact`
  - `name: CharField`
  - `email: EmailField`
  - `phone: CharField`
  - `user: ForeignKey(User)`
- [x] `Task`
  - `title: CharField`
  - `description: TextField`
  - `rubric: CharField`
  - `category: CharField`
  - `prio: CharField`
  - `due_date: DateTimeField`
  - `assigned_users: ManyToManyField(User)`
  - `owner: ForeignKey(User)`
- [x] `Subtask`
  - `title: CharField`
  - `done: BooleanField`
  - `task: ForeignKey(Task)`

## 🔄 Serializer

- [x] `UserSerializer`
- [x] `ContactSerializer`
- [x] `SubtaskSerializer`
- [x] `TaskSerializer`
  - Inkl. Nested `SubtaskSerializer`
  - `assigned_users` als PrimaryKeyRelatedField

## 🔐 Authentication

- [x] Endpunkte:
  - `POST /api/auth/regestration/`
  - `POST /api/auth/login/` → `CustomLoginView`
  - `POST /api/auth/verify/` → `VerifyTokenView`

## 📂 Views & ViewSets

- [x] `UserViewSet`
  - `list`, `retrieve`
- [x] `ContactViewSet`
  - CRUD-Methoden
  - Queryset gefiltert nach `owner=request.user`
- [x] `TaskViewSet`
  - CRUD-Methoden
  - Nested Routes für Subtasks optional
- [x] `SubtaskViewSet`
  - CRUD-Methoden
  - `perform_create` mit `task_id`

## 🌐 URLs / Endpunkte

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContactViewSet, TaskViewSet, SubtaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubtaskViewSet, basename='subtask')

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
# Nicht final!
```

-[x] HTTP only cookie token
