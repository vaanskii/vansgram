from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'unread_messages_count')

    def get_unread_messages_count(self, obj):
        request_user = self.context['request'].user
        return obj.messages.filter(sent_to=request_user, is_read=False).count()

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body',)


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages',)