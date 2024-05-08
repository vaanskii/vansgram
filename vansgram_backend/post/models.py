import uuid
from django.db import models
from django.utils.timezone import now
from account.models import User
from django.conf import settings


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)  
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        time_difference = now() - self.created_at
        days = time_difference.days
        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'}"
        else:
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            if hours > 0:
                return f"{hours} {'hour' if hours == 1 else 'hours'}"
            else:
                return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='posts_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    is_private = models.BooleanField(default=False)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.body:
            return
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def created_at_formatted(self):
            time_difference = now() - self.created_at
            days = time_difference.days
            if days > 0:
                return f"{days} {'day' if days == 1 else 'days'}"
            else:
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes = remainder // 60
                if hours > 0:
                    return f"{hours} {'hour' if hours == 1 else 'hours'}"
                else:
                    return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"
        
    def __str__(self):
        return self.body
    

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurrences = models.IntegerField()