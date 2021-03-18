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
    parentpost = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'parentpost=' + str(self.parentpost) + ',user=' + self.user.username + ',content="' + self.content + '"'


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)

    def __str__(self):
        return "{} follows {}".format(self.user.username, self.friend.username)

class Commentship(models.Model):
    mainpost = models.ForeignKey(Post, related_name='mainpost', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return "{}-'{}' comments {}-'{}'".format(self.comment.user.username,self.comment.content, self.mainpost.user.username,self.mainpost.content)
