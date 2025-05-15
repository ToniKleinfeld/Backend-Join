import uuid
from datetime import timedelta, date
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from join_app.models import GuestProfile, Task, Contact

# Placeholder‑User
PLACEHOLDER_USERS = [
    {"id": 555, "username": "anja-schulz", "email": "schulz@gmail.com"},
    {"id": 556, "username": "anton-mayer", "email": "anton@gmx.com"},
    {"id": 557, "username": "benedikt-ziegler", "email": "benedikt@googlemail.com"},
    {"id": 558, "username": "david-eisenberg", "email": "davidberg@hotmail.de"},
    {"id": 559, "username": "emmanuel-mauer", "email": "emmalnuelma@live.com"},
    {"id": 560, "username": "eva-fischer", "email": "eva@gmx.com"},
    {"id": 561, "username": "marcel-bauer", "email": "bauer@gmail.com"},
    {"id": 562, "username": "tatjana-wolf", "email": "wolfi@gmx.com"},
]


def ensure_placeholder_users():
    for data in PLACEHOLDER_USERS:
        if not User.objects.filter(id=data["id"]).exists():
            User.objects.create_user(
                id=data["id"],
                username=data["username"],
                email=data["email"],
                password=User.objects.make_random_password(),
            )


# Abgelaufene Guests löschen
def cleanup_expired_guests():
    now = timezone.now()
    expired = GuestProfile.objects.filter(expires_at__lt=now)
    for gp in expired:
        gp.user.delete()


# Gast anlegen (User + Profile + Token + Cookie-Value)
def create_guest_user():
    random_str = uuid.uuid4().hex[:8]
    email = f"guest_{random_str}@example.com"
    guest = User.objects.create_user(
        username=email, email=email, password=User.objects.make_random_password()
    )

    GuestProfile.create_for_user(guest, days=1)

    token, _ = Token.objects.get_or_create(user=guest)
    return guest, token.key


# Dummy‑Tasks
def create_guest_tasks(guest):

    def future_date(year, month, day):
        today = date.today()
        target = date(year, month, day)
        delta = (target - today).days
        return timezone.now().date() + timedelta(days=delta)

    specs = [
        {
            "rubric": "in progress",
            "title": "Kochwelt Page & Recipe Recommender",
            "description": "Build start page with recipe recommendation.",
            "due": (2024, 10, 25),
            "category": "User story",
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
            "due": (2024, 9, 30),
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
            "due": (2024, 10, 15),
            "category": "Technical Task",
            "prio": "low",
            "assigned": [558, 557, 555],
            "subtasks": [],
        },
        {
            "rubric": "to do",
            "title": "Daily Kochwelt Recipe",
            "description": "Implement daily recipe and portion calculator",
            "due": (2024, 11, 12),
            "category": "User story",
            "prio": "medium",
            "assigned": [560, 555, 562],
            "subtasks": [],
        },
        {
            "rubric": "Done",
            "title": "Bring Join on Stage",
            "description": "Let's finish this projekt until next week!",
            "due": (2024, 9, 20),
            "category": "User Story",
            "prio": "urgent",
            "assigned": "guest",
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


# Dummy‑Contacts
def create_guest_contacts(guest):
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
