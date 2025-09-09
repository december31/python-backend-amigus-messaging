from django.core.management import BaseCommand

from message.models import ConversationRole


class Command(BaseCommand):

    def handle(self, *args, **options):
        if ConversationRole.objects.count() == 3:
            print("Conversation Role already exists")
            return

        print("Creating conversation role")

        ConversationRole.objects.bulk_create(
            [
                ConversationRole(
                    name=ConversationRole.NameChoice.ADMIN.value,
                    permissions=["can_kick_member", "can_add_member", "can_promote_moderator", "can_demote_moderator"],
                ),
                ConversationRole(
                    name=ConversationRole.NameChoice.MODERATOR.value,
                    permissions=["can_add_member", "can_kick_member"]
                ),
                ConversationRole(
                    name=ConversationRole.NameChoice.MEMBER.value,
                    permissions=[]
                ),
            ]
        )

        print("Conversation Role created")
