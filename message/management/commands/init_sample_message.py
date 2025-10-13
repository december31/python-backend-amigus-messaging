from django.core.management import BaseCommand

from message.models import Message
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        def build_messages(from_user, to_user):
            return Message(

            )

        for user in users:
            others = [u for u in users if u.id != user.id]
            messages = []
