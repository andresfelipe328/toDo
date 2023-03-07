from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from base.forms import UserRegistration, TaskListForm, TaskForm
from base.models import User, TaskList, Task

# Create your views here.
def home(request):
   context = {}
   return render(request, 'home.html', context)

@login_required(login_url='login')
def createTaskList(request):
   form = TaskListForm()
   existingTaskLists = TaskList.objects.filter(creator=request.user.id)

   if request.method == 'POST':
      newTaskList = request.POST.get('name').lower()
      
      for taskList in existingTaskLists:
         if newTaskList == taskList.name:
            messages.error(request, 'Task List Name already exists')
            break
      else:
         TaskList.objects.create(
            creator= request.user.id,
            name = newTaskList.lower()
         )
         return redirect('display-taskLists')

   context = {'form':form, 'taskList':existingTaskLists}
   return render(request, 'create.html', context)


@login_required(login_url='login')
def updateTaskList(request, pk):
   taskList = TaskList.objects.get(name=pk, creator=request.user.id)
   tasks = Task.objects.filter(parent=pk, creator=request.user.id)
   form = TaskForm()

   if 'item' in request.POST:
      newItem = request.POST.get('item').lower()
      for task in tasks:
         if newItem == task.item:
            messages.error(request, 'Task List Name already exists')
            break

      Task.objects.create(
         creator = request.user.id,
         parent = taskList.name,
         item = newItem
      )
      return redirect(request.META.get('HTTP_REFERER'))


   if 'delete' in request.POST:
      task_id = int(request.POST.get('delete') or 0)
      
      if task_id != 0:
         Task.objects.get(id=task_id, creator=request.user.id).delete()
         return redirect(request.META.get('HTTP_REFERER'))


   if 'done' in request.POST:
      task_id = int(request.POST.get('done') or 0)
      if task_id != 0:
         task = Task.objects.get(id=task_id, creator=request.user.id)
         task.status = True
         task.save()
         print(task.status)
   else:
      task_id = int(request.POST.get('undone') or 0)
      if task_id != 0:
         task = Task.objects.get(id=task_id, creator=request.user.id)
         task.status = False
         task.save()      
   
   context = {'taskList': taskList, 'tasks':tasks, 'form': form}
   return render(request, 'update-taskList.html', context)


@login_required(login_url='login')
def displayTaskList(request):
   tasksName = TaskList.objects.filter(creator=request.user.id)
   tasks = Task.objects.all()

   if 'delete' in request.POST:
      task_id = int(request.POST.get('delete') or 0)
      
      if task_id != 0:
         parent = TaskList.objects.get(id=task_id, creator=request.user.id)
         for task in tasks:
            if task.parent == parent.name:
               task.delete()
         TaskList.objects.get(id=task_id, creator=request.user.id).delete()
         return redirect(request.META.get('HTTP_REFERER'))


   context = {'taskList':tasksName}
   return render(request, 'display-taskLists.html', context)


@login_required(login_url='login')
def completionPerc(request):
   taskLists = TaskList.objects.filter(creator=request.user.id)
   tasks = Task.objects.filter(creator=request.user.id)
   uncomplete = {}
   totalTasks = 0
   pageTitle = request.path.replace('/',"")
   
   for list in taskLists:
      totalTasks = 0
      completedTasks = 0
      for task in tasks:
         if task.parent == list.name:
            totalTasks += 1
            if task.status:
               completedTasks += 1
      
      if completedTasks > 0:
         totalPerc = int(round(completedTasks / totalTasks, 2) * 100)

      if completedTasks == 0:
         totalPerc = 0

      if 'taskList-completion' in request.path and totalPerc != 100:
         uncomplete[list.name] = totalPerc

      elif 'taskList-completed' in request.path and totalPerc == 100:
         uncomplete[list.name] = totalPerc
   
   context = {'listPerc': uncomplete, 'pageTitle': pageTitle}
   return render(request, 'taskList-completion.html', context)


def registerPage(request):
   form = UserRegistration()
   context = {'form': form}

   if request.method == 'POST':
      form = UserRegistration(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'Registration phase encountered an error')
   
   return render(request, 'login-register.html', context)


def loginPage(request):
   page = 'login'
   if request.user.is_authenticated:
      return redirect('home')
   
   if request.method == 'POST':
      email = request.POST.get('email').lower()
      psw = request.POST.get('password')

      try:
         user = User.objects.get(email=email)
      except:
         messages.error(request, 'Username does not exist')

      user = authenticate(request, email=email, password=psw)
      if user is not None:
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'Username or password is incorrect')
   
   context = {'page': page}
   return render(request, 'login-register.html', context)


def logoutUser(request):
   logout(request)
   return redirect('home')