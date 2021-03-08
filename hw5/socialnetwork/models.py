from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=255, blank=True)
    picture = models.ImageField()
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return 'id=' + str(self.id) + ', user="' + self.user.username + '"'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    # commented_by = models.ForeignKey("Comment", blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return 'id=' + str(self.id) + ',user="' + self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'id=' + str(self.id) + ',user="' + self.user.username + ',first_name="' + self.first_name + '"'


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)

    def __str__(self):
        return "{} follows {}".format(self.user.username, self.friend.username)
