from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('login/', views.loginPage, name='login'),
   path('register/', views.registerPage, name='register'),
   path('logout/', views.logoutUser, name='logout'),
   path('create-taskList/', views.createTaskList, name='create-taskList'),
   path('update-taskList/<str:pk>/', views.updateTaskList, name='update-taskList'),
   path('display-taskLists/', views.displayTaskList, name='display-taskLists'),
   path('taskList-completion', views.completionPerc, name='taskList-completion'),
   path('taskList-completed', views.completionPerc, name='taskList-completed'),
]