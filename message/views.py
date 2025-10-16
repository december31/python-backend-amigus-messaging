import json
import logging

from django.db.models import Count, Max, OuterRef, Subquery, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from base.response import (
    BaseResponse,
    success,
    BaseListResponse,
    conversation_not_found,
    bad_request,
    user_not_found,
)
from message.models import (
    Message,
    Conversation,
    ConversationParticipant,
    ConversationRole,
)
from message.serializers import (
    ConversationSerializer,
    RecentConversationSerializer,
    SendPrivateMessageSerializer,
    MessageSerializer,
    SendGroupMessageSerializer,
    SimpleMessageSerializer,
)
from user.models import User
from user.permissions import IsInitialized
from utils.model_utils import get_object_or_exception, get_object_or_none
from utils.pagination import PageBasedPagination


logger = logging.getLogger(__name__)


class SendPrivateMessageView(views.APIView):
    serializer_class = SendPrivateMessageSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Message"])
    def post(self, request):
        serializer = SendPrivateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver_id = serializer.validated_data.get("receiver_id")
        content = serializer.validated_data.get("content")

        receiver = User.objects.get(id=receiver_id)

        conversation = (
            Conversation.objects.filter(
                participants__user__id__in=[receiver_id, request.user.id]
            )
            .annotate(participant_count=Count("participants"))
            .filter(participant_count=2)
            .first()
        )

        print(f"sender_id: {request.user.id}")
        print(f"receiver_id: {receiver_id}")
        print(conversation)

        if conversation is None:
            role = ConversationRole.objects.get(
                name=ConversationRole.NameChoice.ADMIN.value
            )

            conversation = Conversation.objects.create(
                type=Conversation.TypeChoice.PRIVATE
            )

            ConversationParticipant.objects.bulk_create(
                [
                    ConversationParticipant(
                        conversation=conversation,
                        user=request.user,
                        role=role,
                        accepted=True,
                    ),
                    ConversationParticipant(
                        conversation=conversation,
                        user=receiver,
                        role=role,
                        accepted=False,
                    ),
                ]
            )

        message = Message.objects.create(
            conversation=conversation, sender=request.user, content=content
        )

        return BaseResponse.create(success, data=MessageSerializer(message).data)


class SendGroupMessageView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendGroupMessageSerializer

    @extend_schema(tags=["Message"])
    def post(self, request):
        pass


class PrivateMessageView(views.APIView, PageBasedPagination):
    @extend_schema(
        tags=["Message"],
        parameters=[
            OpenApiParameter(name="receiver_id", type=int, default=1),
            OpenApiParameter(name="page", type=int, default=1),
            OpenApiParameter(name="page-size", type=int, default=10),
        ],
    )
    def get(self, request):
        if self.get_limit(request) <= 0:
            return BaseListResponse.create(success, data=[])
        if self.get_offset(request) < 0:
            return BaseListResponse.create(success, data=[])

        receiver_id = request.query_params.get("receiver_id")

        if receiver_id is None:
            return BaseResponse.create(
                bad_request, message="receiver_id should not be null"
            )

        receiver = get_object_or_exception(User, user_not_found, id=receiver_id)

        conversation = (
            Conversation.objects.filter(
                participants__user__id__in=[request.user.id, receiver.id]
            )
            .annotate(participants_count=Count("participants"))
            .filter(participants_count=2)
            .first()
        )

        if conversation is None:
            return BaseResponse.create(conversation_not_found)
        
        result = self.paginate_queryset(conversation.messages.all(), request, view=self)

        return BaseResponse.create(
            success, SimpleMessageSerializer(result, many=True).data
        )


class GroupMessageView(views.APIView, PageBasedPagination):
    @extend_schema(
        tags=["Message"],
        parameters=[
            OpenApiParameter(name="conversation_id", type=int, default=1),
            OpenApiParameter(name="page", type=int, default=1),
            OpenApiParameter(name="page-size", type=int, default=10),
        ],
    )
    def get(self, request):
        conversation_id = request.query_params.get("conversation_id")
        
        if conversation_id is None:
            return BaseResponse.create(bad_request, "conversation_id cannot be null")
        
        conversation = get_object_or_exception(Conversation, conversation_not_found, id=conversation_id)

        if conversation is None:
            return BaseResponse.create(conversation_not_found)

        result = self.paginate_queryset(conversation.messages, request, view=self)

        return BaseResponse.create(
            success, SimpleMessageSerializer(result, many=True).data
        )


class RecentMessagesView(views.APIView, PageBasedPagination):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Message"],
        parameters=[
            OpenApiParameter(name="page", type=int, default=1),
            OpenApiParameter(name="page-size", type=int, default=10),
        ],
    )
    def get(self, request):
        if self.get_limit(request) <= 0:
            return BaseListResponse.create(success, data=[])
        if self.get_offset(request) < 0:
            return BaseListResponse.create(success, data=[])

        # latest_message_subquery = Message.objects.filter(
        #     conversation=OuterRef("conversation")
        # ).order_by("-created_at", "-id")

        # unread_message_subquery = Message.objects.filter(
        #     conversation=OuterRef("conversation")
        # ).values("conversation").annotate(unread=Count(
        #     "id",
        #     filter=Q(status=Message.StatusChoice.SENT.value) & ~Q(sender__id=request.user.id)
        # )).values("unread")[:1]

        # latest_message = Message.objects.filter(
        #     id=Subquery(latest_message_subquery[:1].values("id")),
        #     conversation__participants__user__id=request.user.id
        # ).order_by("-created_at").annotate(unread=Subquery(unread_message_subquery))

        # print(latest_message.values())

        conversation = Conversation.objects.filter(participants__user=request.user)

        result = self.paginate_queryset(conversation, request, view=self)

        return BaseListResponse.create(
            success, data=RecentConversationSerializer(result, many=True).data
        )