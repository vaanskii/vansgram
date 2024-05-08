import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Conversation, ConversationMessage
from account.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_body = text_data_json['body']
        conversation_id = text_data_json['conversationId']
        user_id = text_data_json['created_by']['id']

        message_obj = await self.save_message(conversation_id, user_id, message_body)

        message_data = {
            'id': str(message_obj.id),
            'conversationId': conversation_id,
            'body': message_body,
            'created_by': {
                'id': user_id,
                'get_avatar': message_obj.created_by.get_avatar()
            },
            'created_at_formatted': message_obj.created_at_formatted()
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message_data = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message_data))

    @sync_to_async
    def save_message(self, conversation_id, user_id, message):
        conversation = Conversation.objects.get(id=conversation_id)
        user = User.objects.get(id=user_id)
        
        # Assuming 'sent_to' is another user in the conversation
        sent_to_user = conversation.users.exclude(id=user_id).first()
        if not sent_to_user:
            raise ValueError("No recipient found in the conversation.")

        message_obj = ConversationMessage.objects.create(
            conversation=conversation,
            created_by=user,
            body=message,
            sent_to=sent_to_user
        )
        return message_obj
