from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    picture = models.FileField(blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return 'id=' + str(self.id) + 'user="' + self.user.username + '"'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    # commented_by = models.ForeignKey("Comment", blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return 'id=' + str(self.id) + ',user="' + self.user.username + ',first_name="' + self.first_name + '"'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'id=' + str(self.id) + ',user="' + self.user.username + ',first_name="' + self.first_name + '"'


class Friend(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

    def __str__(self):
        return "{} follows {}".format(self.from_user.username, self.to_user.username)
