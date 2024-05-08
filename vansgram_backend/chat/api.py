from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from account.models import User
from django.db.models import Max

from .models import Conversation, ConversationMessage
from .serializers import ConversationDetailSerializer, ConversationSerializer, ConversationMessageSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=[request.user])
    conversations = conversations.annotate(last_message_at=Max('messages__created_at'))
    conversations = conversations.order_by('-last_message_at')

    # Calculate the count of unread messages for each conversation
    for conversation in conversations:
        conversation.unread_messages_count = conversation.messages.filter(sent_to=request.user, is_read=False).count()

    serializer = ConversationSerializer(conversations, many=True, context={'request': request})

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to,
    )
    
    serializer = ConversationMessageSerializer(conversation_message)
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def mark_messages_as_read(request, pk):
    conversation = Conversation.objects.get(pk=pk, users__in=[request.user])
    messages = conversation.messages.filter(sent_to=request.user, is_read=False)
    count = messages.update(is_read=True)
    
    return JsonResponse({'marked_as_read': count}, safe=False)