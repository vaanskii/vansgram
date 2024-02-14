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
        minutes = int(time_difference.total_seconds() / 60)

        if minutes < 60:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"
        else:
            hours = int(minutes / 60)
            return f"{hours} {'hour' if hours == 1 else 'hours'}"

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
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60

        if days > 0:
            # If more than a day, show days and remaining hours
            return f"{days} {'day' if days == 1 else 'days'} and {hours} {'hour' if hours == 1 else 'hours'} ago"
        elif hours > 0:
            # If less than a day but more than an hour, show hours and minutes
            return f"{hours} {'hour' if hours == 1 else 'hours'} and {minutes} {'minute' if minutes == 1 else 'minutes'} ago"
        else:
            # If less than an hour, show minutes only
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"