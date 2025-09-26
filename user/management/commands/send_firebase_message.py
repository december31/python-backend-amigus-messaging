from django.core.management import BaseCommand
from firebase_admin import messaging

from project import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)

    def handle(self, *args, **options):
        token = options['token']
        print(token)


        message = messaging.Message(
            data={
                "title": "test"
            },
            token=token
        )

        response = messaging.send(message)
        print('Successfully sent message:', response)
