from dataclasses import fields
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, TaskList, Task

class UserForm(ModelForm):
   class Meta:
      model = User
      fields = ['username', 'email']

class UserRegistration(UserCreationForm):
   class Meta:
      model = User
      fields = ['name', 'username', 'email', 'password1', 'password2']

class TaskListForm(ModelForm):
   class Meta:
      model = TaskList
      fields = '__all__'
      exclude = ['creator']

class TaskForm(ModelForm):
   class Meta:
      model = Task
      fields = ['item']
      exclude = ['creator']