from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (
    RegistrationsSerializer,
    CustomAuthTokenSerializer,
    GuestCreationSerializer,
)
from rest_framework import status

# from join_app.models import GuestProfile, Task, Contact
# import uuid
# from django.utils import timezone
# from datetime import timedelta, date
# from django.contrib.auth.models import User
from .guest_service import (
    ensure_placeholder_users,
    cleanup_expired_guests,
    create_guest_user,
    create_guest_tasks,
    create_guest_contacts,
)


class RegestrationView(APIView):
    """
    Regestration des Benutzer mit Name, Email ,Passwort und Passwortkontrolle.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationsSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            response = Response(
                {
                    "username": saved_account.username,
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                secure=False,
                domain="localhost",
                samesite="Lax",
                max_age=24 * 60 * 60,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """
    Login des Benutzer mit Email ,Passwort als return obj mit cookie.token oder Error.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            response = Response(
                {"username": user.username},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                secure=True,
                domain="localhost",
                samesite="Lax",
                max_age=24 * 60 * 60,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: secure=True , wenn in Production !!!


class VerifyTokenView(APIView):
    """
    Überprüfung, ob ein Token vorhanden ist.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        token_key = request.COOKIES.get("auth_token")
        if not token_key:
            return Response(
                {"detail": "No token cookie."}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)


class PingCookieView(APIView):
    """
    Gibt 200 OK zurück, wenn das 'auth_token' HttpOnly-Cookie im Request enthalten ist,
    sonst 204 No Content.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        if "auth_token" in request.COOKIES:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            key="auth_token", domain="localhost", path="/", samesite="Lax"
        )

        if request.auth:
            try:
                request.auth.delete()
            except Exception as e:
                pass

        return response


class CreateGuestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ensure_placeholder_users()
        cleanup_expired_guests()

        guest, token_key = create_guest_user()
        create_guest_tasks(guest)
        create_guest_contacts(guest)

        resp = Response(
            GuestCreationSerializer(guest).data, status=status.HTTP_201_CREATED
        )
        resp.set_cookie(
            key="auth_token",
            value=token_key,
            httponly=True,
            secure=False,
            domain="localhost",
            samesite="Lax",
            max_age=24 * 3600,
        )
        return resp


# class CreateGuestView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):

#         # Platzhalter User anlegen für "Assigned to vergabe"

#         PLACEHOLDER_USERS = [
#             {"id": 555, "username": "anja-schulz", "email": "schulz@gmail.com"},
#             {"id": 556, "username": "anton-mayer", "email": "anton@gmx.com"},
#             {
#                 "id": 557,
#                 "username": "benedikt-ziegler",
#                 "email": "benedikt@googlemail.com",
#             },
#             {"id": 558, "username": "david-eisenberg", "email": "davidberg@hotmail.de"},
#             {"id": 559, "username": "emmanuel-mauer", "email": "emmalnuelma@live.com"},
#             {"id": 560, "username": "eva-fischer", "email": "eva@gmx.com"},
#             {"id": 561, "username": "marcel-bauer", "email": "bauer@gmail.com"},
#             {"id": 562, "username": "tatjana-wolf", "email": "wolfi@gmx.com"},
#         ]

#         for user_data in PLACEHOLDER_USERS:
#             if not User.objects.filter(username=user_data["id"]).exists():
#                 if not User.objects.filter(username=user_data["username"]).exists():
#                     password = User.objects.make_random_password()
#                     User.objects.create_user(
#                         id=user_data["id"],
#                         username=user_data["username"],
#                         email=user_data["email"],
#                         password=password,
#                     )

#         # Aufräumen: alle abgelaufenen Guests löschen
#         now = timezone.now()
#         expired = GuestProfile.objects.filter(expires_at__lt=now)

#         for gp in expired:
#             gp.user.delete()

#         # Neuen Guest anlegen
#         random_str = uuid.uuid4().hex[:8]
#         email = f"guest_{random_str}@example.com"
#         password = User.objects.make_random_password()
#         guest = User.objects.create_user(username=email, email=email, password=password)

#         #  GuestProfile mit Ablauf in 1 Tag erstellen
#         GuestProfile.create_for_user(guest, days=1)

#         #  Dummy-Data anlegen
#         Task.objects.bulk_create(
#             [
#                 Task(
#                     creator=guest,
#                     rubric="in progress",
#                     title="Kochwelt Page & Recipe Recommender",
#                     description="Build start page with recipe recommendation.",
#                     due_date=timezone.now().date()
#                     + timedelta(days=(date(2024, 10, 25) - date.today()).days),
#                     category="User story",
#                     prio="medium",
#                     assigned_users=[559, 561, 556, 557, 558],
#                     subtasks=[
#                         {"done": True, "title": "Implement Recipe Recommendation"},
#                         {"done": False, "title": "Start Page Layout"},
#                     ],
#                 ),
#                 Task(
#                     creator=guest,
#                     rubric="Await feedback",
#                     title="CSS Architecture Planning",
#                     description="Define CSS naming conventions and structure.",
#                     due_date=timezone.now().date()
#                     + timedelta(days=(date(2024, 9, 30) - date.today()).days),
#                     category="Technical Task",
#                     prio="urgent",
#                     assigned_users=[560, 557, 559],
#                     subtasks=[
#                         {"done": True, "title": "Establish CSS Methodology"},
#                         {"done": True, "title": "Setup Base Styles"},
#                     ],
#                 ),
#                 Task(
#                     creator=guest,
#                     rubric="Await feedback",
#                     title="HTML Base Template Creation",
#                     description="Create reuseable HTML base templates",
#                     due_date=timezone.now().date()
#                     + timedelta(days=(date(2024, 10, 15) - date.today()).days),
#                     category="Technical Task",
#                     prio="low",
#                     assigned_users=[558, 557, 555],
#                 ),
#                 Task(
#                     creator=guest,
#                     rubric="to do",
#                     title="Daily Kochwelt Recipe",
#                     description="Implement daily recipe and portion calculator",
#                     due_date=timezone.now().date()
#                     + timedelta(days=(date(2024, 11, 12) - date.today()).days),
#                     category="User story",
#                     prio="medium",
#                     assigned_users=[560, 555, 562],
#                 ),
#                 Task(
#                     creator=guest,
#                     rubric="Done",
#                     title="Bring Join on Stage",
#                     description="Let's finish this projekt until next week!",
#                     due_date=timezone.now().date()
#                     + timedelta(days=(date(2024, 9, 20) - date.today()).days),
#                     category="User Story",
#                     prio="urgent",
#                     assigned_users=[562, 555, 557, guest.id, 560, 561, 558, 559, 556],
#                     subtasks=[
#                         {"done": True, "title": "Contacts"},
#                         {"done": True, "title": "Add Task"},
#                         {"done": True, "title": "Board.js"},
#                     ],
#                 ),
#             ]
#         )
#         Contact.objects.bulk_create(
#             [
#                 Contact(
#                     user=guest,
#                     name="Anja Schulz",
#                     email="schulz@gmail.com",
#                     phone="174987674765",
#                     bgcolor="#6E52FF",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Anton Mayer",
#                     email="anton@gmx.com",
#                     phone="173867654653",
#                     bgcolor="#9327FF",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Benedikt Ziegler",
#                     email="benedikt@googlemail.com",
#                     phone="174987674765",
#                     bgcolor="#FC71FF",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="David Eisenberg",
#                     email="davidberg@hotmail.de",
#                     phone="176983474765",
#                     bgcolor="#FFBB2B",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Emmanuel Mauer",
#                     email="emmalnuelma@live.com",
#                     phone="174987674765",
#                     bgcolor="#462F8A",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Eva Fischer",
#                     email="eva@gmx.com",
#                     phone="1749876723765",
#                     bgcolor="#1FD7C1",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Marcel Bauer",
#                     email="bauer@gmail.com",
#                     phone="172932674765",
#                     bgcolor="#FF4646",
#                 ),
#                 Contact(
#                     user=guest,
#                     name="Tatjana Wolf",
#                     email="wolfi@gmx.com",
#                     phone="176127674765",
#                     bgcolor="#9437FF",
#                 ),
#             ]
#         )

#         #  Token generieren & Cookie setzen
#         token, _ = Token.objects.get_or_create(user=guest)
#         resp = Response(
#             GuestCreationSerializer(guest).data, status=status.HTTP_201_CREATED
#         )

#         resp.set_cookie(
#             key="auth_token",
#             value=token.key,
#             httponly=True,
#             secure=False,  # TODO: Produktion: True
#             domain="localhost",
#             samesite="Lax",
#             max_age=24 * 3600,
#         )
#         return resp
