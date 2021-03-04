from django.db import models


# Create your models here.
class Profile(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    biography = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profiles')
