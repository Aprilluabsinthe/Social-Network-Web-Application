from django.contrib import admin

# Register your models here.
from socialnetwork.models import Profile, Friend

admin.site.register(Profile)
admin.site.register(Friend)