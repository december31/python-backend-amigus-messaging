from datetime import datetime
import json
from django.core.management import BaseCommand
from django.db.models import Count
from message.models import (
    Conversation,
    ConversationParticipant,
    ConversationRole,
    Message,
)
from user.models import User
from utils.utils import random_datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()

        def build_messages(from_user, to_user):
            print(f"{from_user.email} -> {to_user.email}")
            conversation = (
                Conversation.objects.filter(participants__user__id__in=[from_user.id, to_user.id])
                .annotate(participant_count=Count("participants"))
                .filter(participant_count=2)
                .first()
            )

            if conversation is None:
                conversation = Conversation.objects.create(
                    type=Conversation.TypeChoice.PRIVATE
                )

                admin_role = ConversationRole.objects.get(
                    name=ConversationRole.NameChoice.ADMIN.value
                )

                ConversationParticipant.objects.bulk_create(
                    [
                        ConversationParticipant(
                            conversation=conversation,
                            user=from_user,
                            role=admin_role,
                        ),
                        ConversationParticipant(
                            conversation=conversation,
                            user=to_user,
                            role=admin_role,
                        ),
                    ]
                )

            def generate_message():
                start_date = datetime(
                    year=2024, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                )
                end_date = datetime.now()
                date = random_datetime(start_date, end_date)

                return Message(
                    conversation=conversation,
                    content=f"message from {from_user.email} to {to_user.email}",
                    sender=from_user,
                    status=Message.StatusChoice.SENT,
                    created_at=date,
                    updated_at=date,
                )

            return [generate_message() for _ in range(100)]

        total_messages = []
        for user in users:
            others = [u for u in users if u.id != user.id]
            messages = [
                build_messages(from_user=user, to_user=other) for other in others
            ]

            messages = [item for sublist in messages for item in sublist]
            total_messages += messages
        
        print(f"creating {len(total_messages)} messages . . .")
        
        Message.objects.bulk_create(total_messages)

        print(f"Successful created {len(total_messages)} messages for {len(users)} users")
