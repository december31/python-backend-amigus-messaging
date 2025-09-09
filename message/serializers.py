from rest_framework import serializers

from message.models import Message


class SendPrivateMessageSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False, allow_blank=False)
    receiver_id = serializers.IntegerField(allow_null=True, required=False)


class SendGroupMessageSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False, allow_blank=False)
    conversation_id = serializers.IntegerField(allow_null=True, required=False)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
