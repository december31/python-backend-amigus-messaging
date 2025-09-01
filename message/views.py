from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from base.response import BaseResponse, success
from message.models import Message, Conversation, ConversationParticipant, ConversationRole
from message.serializers import SendMessageSerializer, MessageSerializer
from user.models import User


class SendPrivateMessageView(views.APIView):
    serializer_class = SendMessageSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Message"])
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_id = serializer.validated_data.get('receiver_id')
        content = serializer.validated_data.get("content")

        receiver = User.objects.get(id=receiver_id)

        conversation = Conversation.objects.filter(
            participants_user_id__in=[receiver_id, request.user.id]
        ).annotate(
            participant_count=Count("participants")
        ).filter(
            participant_count=2
        ).first()

        print(f"sender_id: {request.user.id}")
        print(f"receiver_id: {receiver_id}")
        print(conversation)

        if conversation is None:

            role = ConversationRole.objects.get(name=ConversationRole.NameChoice.ADMIN.value)

            conversation = Conversation.objects.create(
                type = Conversation.TypeChoice.PRIVATE
            )

            ConversationParticipant.objects.bulk_create(
                [
                    ConversationParticipant(
                        conversation=conversation,
                        user=request.user,
                        role=role,
                        accepted=True
                    ),

                    ConversationParticipant(
                        conversation=conversation,
                        user=receiver,
                        role=role,
                        accepted=False
                    )
                ]
            )


        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        return BaseResponse.create(success, data=MessageSerializer(message).data)
