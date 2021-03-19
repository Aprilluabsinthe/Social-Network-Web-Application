from django.contrib import admin

# Register your models here.
from socialnetwork.models import Profile, Friendship

admin.site.register(Profile)
admin.site.register(Friendship)