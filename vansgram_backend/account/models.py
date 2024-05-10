import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone



class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)

    people_you_may_know = models.ManyToManyField('self')

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIALQAvwMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABAUCAwYBB//EADYQAQACAQIFAgIHBgcAAAAAAAABAgMEEQUSMUFRISJSYRNxgZGhscEyNEJi8PEVIyQzcpLR/8QAFgEBAQEAAAAAAAAAAAAAAAAAAAEC/8QAFhEBAQEAAAAAAAAAAAAAAAAAAAER/9oADAMBAAIRAxEAPwD6WA0yAAAAAAAABETM7RG8+Ib6aLU36YpiPn6A0CX/AIbqdulf+zTm0+bB/uUmI89YFagBAAAAAAAAAAAAAAAABYaThs3iL596x2rHU4XpYvb6a8e2s+2PMrZLVYYsOPDG2OkV+pmCKPLVi9ZraImJ6xL0BR6vRZMWa0Y6XtTrExG+yL0naXTI+r0lNTXpEXjpZdTFCPb1tS81tG1onaYeKgAAAAAAAAAAAAREzO0dRu0VebV4o/m3+4F5gxxhw0xx/DDYDLQAAAAACp4xjiuWmSP4o2n7Fet+MR/p6T4v+kqhqIACAAAAAAAAAACTw399x/b+UozfoJ5dZin57Cr8BlQAAAAAEHjH7rX/AJx+UqdbcZn/ACccebb/AIKlqJQAQAAAAAAAAAAT+F6amWZy339kxy+vdAWnBbe3LXxMSVVkAyoAAAAACPrNNXU49rb81YnlmPKhdJeeWlrT2jdzaxKAKgAAAAAAAAAAlcOzRh1Mc07VtHLM+EUB0wg8JyTfTzSZ3mk/gnMtAAAAAPJmIjeekAicTzxi09qb++8bRHy7qVllvOTJa9pmZtO/qxaQAEAAAAAAAAAAAATOFZox6jltPpeNvt7LpzK64dq51FJpf9uses+UqxMARQABG4jmjFpbevut7YSJnaN1Dq9TbU5eafSsfsx4WDQArIAAAAAAAAAAAAAAseCx78s+Ij9VctuDV2w5Lebbfd/cqrABlQABzMxtMx4dM53U15NRlr4tKxK1gKgAAAAAAAAAAAAPaVte0VpWbTPaIWGn4Xafdnty/wAteoqFgw3z3imON57z2hfYMVcGKuOvSO/l7jx0xV5cdYrHyZpaoAgAAK7iektefpsUbzt7ojv81iA5kXmp0OLPvbbkv8Ufqq9To82DeZjmp8VWtRHAEAAAAAAAStJosmo2tPtx/FPf6hUWsTaYrWJmZ6RCw0/DL292eeSPhjqsNPpsWnjbHX172nrLcmmNeHDjw12x0iv6tgIoAAAAAAAAACJqOH4c281j6O3mOn3KvUaTLp/W9d6/FHRfnVdHMi31XDaZN7YdqW8dp/8AFVkx3xXmmSs1tHaVRiAIAyx0nJkrSOtp2BM4bo4zT9Llj2RPpHxLjoxx0jHStKxtFY2hky0AAAAAAAAAAAAAAAANOp09NRj5bx69rd4bgHN5cdsOS2O8esMVrxjDvSuaI9Y9J+r+vzVTSCVwyInWU37bz+DwBegMqAAAAAAAAAAAAAAAAAAj6+InR5d/h3UILEr/2Q=='


class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)
    request_sent = models.BooleanField(default=False)