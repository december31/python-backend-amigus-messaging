from django.core.management import BaseCommand

from message.models import Message
from user.models import User
from utils.model_utils import get_object_or_none


class Command(BaseCommand):
    emails = [
        "ducan123@gmail.com",
        "maria.garcia@example.com",
        "david.smith@example.org",
        "li.wei@example.net",
        "fatima.khan@example.com",
        "lucas.martin@example.org",
        "sofia.rossi@example.net",
        "hiroshi.tanaka@example.com",
        "emma.johnson@example.org",
        "ahmed.hassan@example.net",
        "isabella.silva@example.com",
        "thomas.müller@example.org",
        "olivia.brown@example.net",
        "raj.patel@example.com",
        "chloe.dubois@example.org",
        "miguel.torres@example.net",
        "hannah.wilson@example.com",
        "yusuf.demir@example.org",
        "anna.nielsen@example.net",
        "peter.jones@example.com",
        "noor.al-farsi@example.org",
    ]

    def handle(self, *args, **options):
        def get_or_create_user(email):
            user = get_object_or_none(User.objects, email=email)
            if user is None:
                user = User(username=email, email=email, is_initialized=True, is_active=True)
                user.set_password("anthony123")
                user.save()
            print(f"user created {user.email}")
            return user

        [get_or_create_user(email) for email in self.emails]
