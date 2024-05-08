import uuid
from django.db import models
from account.models import User
from django.utils.timezone import now

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)

    def modified_at_formatted(self):
            time_difference = now() - self.created_at
            days = time_difference.days
            hours, _ = divmod(time_difference.seconds, 3600)

            if days > 0:
                return f"{days} {'day' if days == 1 else 'days'} ago"
            elif hours > 0:
                return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            else:
                minutes = time_difference.seconds // 60
                return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)

    def created_at_formatted(self):
            time_difference = now() - self.created_at
            days = time_difference.days
            hours, _ = divmod(time_difference.seconds, 3600)

            if days > 0:
                return f"{days} {'day' if days == 1 else 'days'} ago"
            elif hours > 0:
                return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            else:
                minutes = time_difference.seconds // 60
                return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"