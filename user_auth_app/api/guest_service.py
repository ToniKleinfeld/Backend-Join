import uuid
from datetime import timedelta, date
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from join_app.models import GuestProfile, Task, Contact
from django.utils.crypto import get_random_string
from join_app.models import Profile
import random


def random_hex_color():
    """
    Erstellt eine Zufällig Hex Farbe
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


# Placeholder‑User
PLACEHOLDER_USERS = [
    {
        "id": 555,
        "username": "anja-schulz",
        "email": "schulz@gmail.com",
        "color": random_hex_color(),
    },
    {
        "id": 556,
        "username": "anton-mayer",
        "email": "anton@gmx.com",
        "color": random_hex_color(),
    },
    {
        "id": 557,
        "username": "benedikt-ziegler",
        "email": "benedikt@googlemail.com",
        "bgcocolorlor": random_hex_color(),
    },
    {
        "id": 558,
        "username": "david-eisenberg",
        "email": "davidberg@hotmail.de",
        "color": random_hex_color(),
    },
    {
        "id": 559,
        "username": "emmanuel-mauer",
        "email": "emmalnuelma@live.com",
        "bgccolorolor": random_hex_color(),
    },
    {
        "id": 560,
        "username": "eva-fischer",
        "email": "eva@gmx.com",
        "color": random_hex_color(),
    },
    {
        "id": 561,
        "username": "marcel-bauer",
        "email": "bauer@gmail.com",
        "color": random_hex_color(),
    },
    {
        "id": 562,
        "username": "tatjana-wolf",
        "email": "wolfi@gmx.com",
        "color": random_hex_color(),
    },
]


def ensure_placeholder_users():
    """
    Legt placeholder User an, wenn nicht vorhanden und ID nicht vergeben wurde
    """
    for data in PLACEHOLDER_USERS:
        if not User.objects.filter(id=data["id"]).exists():
            user = User.objects.create_user(
                id=data["id"],
                username=data["username"],
                email=data["email"],
                password=get_random_string(length=12),
            )

            profile = user.profile
            profile.color = data.get("color", profile.color)
            profile.save()


def cleanup_expired_guests():
    """
    Abgelaufene Guests löschen
    """
    now = timezone.now()
    expired = GuestProfile.objects.filter(expires_at__lt=now)
    for gp in expired:
        gp.user.delete()


def create_guest_user():
    """
    Gast anlegen (User + Profile + Token + Cookie-Value)
    """
    random_str = uuid.uuid4().hex[:8]
    username = "guest"
    email = f"guest_{random_str}@example.com"
    guest = User.objects.create_user(
        username=username, email=email, password=get_random_string(length=12)
    )

    GuestProfile.create_for_user(guest, days=1)

    token, _ = Token.objects.get_or_create(user=guest)
    return guest, token.key


def create_guest_tasks(guest):
    """
    Legt Tasks für den Guest an
    """

    def future_date(year, month, day):
        today = date.today()
        target = date(year, month, day)
        delta = (target - today).days
        return timezone.now().date() + timedelta(days=delta)

    specs = [
        {
            "rubric": "In progress",
            "title": "Kochwelt Page & Recipe Recommender",
            "description": "Build start page with recipe recommendation.",
            "due": (2025, 10, 25),
            "category": "User Story",
            "prio": "medium",
            "assigned": [559, 561, 556, 557, 558],
            "subtasks": [
                {"done": True, "title": "Implement Recipe Recommendation"},
                {"done": False, "title": "Start Page Layout"},
            ],
        },
        {
            "rubric": "Await feedback",
            "title": "CSS Architecture Planning",
            "description": "Define CSS naming conventions and structure.",
            "due": (2025, 9, 30),
            "category": "Technical Task",
            "prio": "urgent",
            "assigned": [560, 557, 559],
            "subtasks": [
                {"done": True, "title": "Establish CSS Methodology"},
                {"done": True, "title": "Setup Base Styles"},
            ],
        },
        {
            "rubric": "Await feedback",
            "title": "HTML Base Template Creation",
            "description": "Create reuseable HTML base templates",
            "due": (2025, 10, 15),
            "category": "Technical Task",
            "prio": "low",
            "assigned": [558, 557, 555],
            "subtasks": [],
        },
        {
            "rubric": "To do",
            "title": "Daily Kochwelt Recipe",
            "description": "Implement daily recipe and portion calculator",
            "due": (2025, 11, 12),
            "category": "User Story",
            "prio": "medium",
            "assigned": [560, 555, 562],
            "subtasks": [],
        },
        {
            "rubric": "Done",
            "title": "Bring Join on Stage",
            "description": "Let's finish this projekt until next week!",
            "due": (2025, 9, 20),
            "category": "User Story",
            "prio": "urgent",
            "assigned": ["guest"],
            "subtasks": [
                {"done": True, "title": "Contacts"},
                {"done": True, "title": "Add Task"},
                {"done": True, "title": "Board.js"},
            ],
        },
    ]

    tasks = []
    for spec in specs:
        task = Task.objects.create(
            creator=guest,
            rubric=spec["rubric"],
            title=spec["title"],
            description=spec["description"],
            due_date=future_date(*spec["due"]),
            category=spec["category"],
            prio=spec["prio"],
        )

        assigned_ids = [guest.id if x == "guest" else x for x in spec["assigned"]]
        task.assigned_users.set(assigned_ids)

        for st in spec["subtasks"]:
            task.subtasks.create(done=st["done"], title=st["title"])
        tasks.append(task)
    return tasks


def create_guest_contacts(guest):
    """
    Legt Contacts für den Guest an
    """
    contact_specs = [
        {
            "name": "Anja Schulz",
            "email": "schulz@gmail.com",
            "phone": "174987674765",
            "bgcolor": "#6E52FF",
        },
        {
            "name": "Anton Mayer",
            "email": "anton@gmx.com",
            "phone": "173867654653",
            "bgcolor": "#9327FF",
        },
        {
            "name": "Benedikt Ziegler",
            "email": "benedikt@googlemail.com",
            "phone": "174987674765",
            "bgcolor": "#FC71FF",
        },
        {
            "name": "David Eisenberg",
            "email": "davidberg@hotmail.de",
            "phone": "176983474765",
            "bgcolor": "#FFBB2B",
        },
        {
            "name": "Emmanuel Mauer",
            "email": "emmalnuelma@live.com",
            "phone": "174987674765",
            "bgcolor": "#462F8A",
        },
        {
            "name": "Eva Fischer",
            "email": "eva@gmx.com",
            "phone": "1749876723765",
            "bgcolor": "#1FD7C1",
        },
        {
            "name": "Marcel Bauer",
            "email": "bauer@gmail.com",
            "phone": "172932674765",
            "bgcolor": "#FF4646",
        },
        {
            "name": "Tatjana Wolf",
            "email": "wolfi@gmx.com",
            "phone": "176127674765",
            "bgcolor": "#9437FF",
        },
    ]
    contacts = []
    for c in contact_specs:
        contacts.append(Contact(user=guest, **c))
    Contact.objects.bulk_create(contacts)
    return contacts
