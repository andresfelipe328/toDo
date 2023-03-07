from django.contrib import admin
from .models import User, TaskList, Task

# Register your models here.
admin.site.register(User)
admin.site.register(TaskList)
admin.site.register(Task)