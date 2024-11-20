from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomUser(AbstractUser):
    first_name = models.TextField(max_length=100)
    last_name=models.TextField(max_length=100)
    birthdate = models.DateField(validators=[UnicodeUsernameValidator])
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return self.username
