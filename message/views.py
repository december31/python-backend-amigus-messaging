import json
import logging

from django.db.models import Count, Max, OuterRef, Subquery, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from base.response import BaseResponse, success, BaseListResponse
from message.models import Message, Conversation, ConversationParticipant, ConversationRole
from message.serializers import SendPrivateMessageSerializer, MessageSerializer, SendGroupMessageSerializer
from user.models import User

logger = logging.getLogger(__name__)


class SendPrivateMessageView(views.APIView):
    serializer_class = SendPrivateMessageSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Message"])
    def post(self, request):
        serializer = SendPrivateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_id = serializer.validated_data.get('receiver_id')
        content = serializer.validated_data.get("content")

        receiver = User.objects.get(id=receiver_id)

        conversation = Conversation.objects.filter(
            participants__user__id__in=[receiver_id, request.user.id]
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
                type=Conversation.TypeChoice.PRIVATE
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


class SendGroupMessageView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendGroupMessageSerializer

    @extend_schema(tags=["Message"])
    def post(self, request):
        pass


class RecentMessagesView(views.APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Message"],
        parameters=[
            OpenApiParameter(name="limit", type=int),
            OpenApiParameter(name="offset", type=int)
        ])
    def get(self, request):
        if self.get_limit(request) <= 0:
            return BaseListResponse.create(success, data=[])
        if self.get_offset(request) < 0:
            return BaseListResponse.create(success, data=[])

        latest_message_subquery = Message.objects.filter(
            conversation=OuterRef("conversation")
        ).order_by("-created_at", "-id")

        unread_message_subquery = Message.objects.filter(
            conversation=OuterRef("conversation")
        ).values("conversation").annotate(unread=Count(
            "id",
            filter=Q(status=Message.StatusChoice.SENT.value) & ~Q(sender__id=request.user.id)
        )).values("unread")[:1]


        latest_message = Message.objects.filter(
            id=Subquery(latest_message_subquery[:1].values("id")),
            conversation__participants__user__id=request.user.id
        ).order_by("-created_at").annotate(unread=Subquery(unread_message_subquery))

        print(latest_message.values())
        result = self.paginate_queryset(latest_message, request, view=self)

        return BaseListResponse.create(success, data=MessageSerializer(result, many=True).data)
