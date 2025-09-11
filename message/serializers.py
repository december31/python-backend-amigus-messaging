from rest_framework import serializers

from message.models import Message, Conversation, ConversationParticipant, ConversationRole
from user.serializers import UserSerializer


class SendPrivateMessageSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False, allow_blank=False)
    receiver_id = serializers.IntegerField(allow_null=True, required=False)


class SendGroupMessageSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False, allow_blank=False)
    conversation_id = serializers.IntegerField(allow_null=True, required=False)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationRole
        exclude = ("created_at", "updated_at")


class ConversationParticipantsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = RoleSerializer()

    class Meta:
        model = ConversationParticipant
        exclude = ("created_at", "updated_at", "conversation")


class ConversationSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantsSerializer(many=True)

    class Meta:
        model = Conversation
        exclude = ("created_at", "updated_at")


class MessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()
    sender = UserSerializer()

    class Meta:
        model = Message
        exclude = ("created_at", "updated_at")
