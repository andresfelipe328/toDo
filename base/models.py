from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.db import models

# Create your models here.
class User(AbstractUser):
   name = models.CharField(max_length=150, null=True)
   email = models.EmailField(unique=True, null=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']


class TaskList(models.Model):
   creator = models.IntegerField(default=00000)
   name = models.CharField(max_length=50, null=True, default='list')
   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      ordering = ['-updated','created']
   
   def __str__(self):
      return self.name


class Task(models.Model):
   creator = models.IntegerField(default=00000)
   parent = models.CharField(max_length=50, null=True, default='list')
   item = models.CharField(max_length=50, null=True, default='task')
   status = models.BooleanField(default=False)

   def __str__(self):
      return self.item