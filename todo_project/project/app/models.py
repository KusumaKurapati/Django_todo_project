from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password,check_password
# Create your models here.


class Users(models.Model):

    user_id=models.AutoField(primary_key=True)

    name=models.CharField(max_length=100)

    email=models.EmailField(unique=True)

    password=models.CharField(max_length=200)
    


from django.contrib.auth.models import User

class Todo(models.Model):
    todo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()

    def __str__(self):
        return self.title





