from django.contrib import admin
from .models import User, FriendshipRequest

admin.site.register(User)

admin.site.register(FriendshipRequest)