from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout , authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'todo/home.html')
def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form': UserCreationForm()})
    # create a user
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form': UserCreationForm(),'error': 'Username already exists.Try with a different username'})
        else:
            # tell the user the password did'nt match
            return render(request,'todo/signupuser.html',{'form': UserCreationForm(),'error': 'passwords did not match'})

def currenttodos(request):
    #show todos for the logged in user only
    todos = Todo.objects.filter(user= request.user, date_completed__isnull =True )
    return render(request,'todo/currenttodos.html',{'todos':todos})
    
def completedtodos(request):
    #show todos for the logged in user only
    todos = Todo.objects.filter(user= request.user, date_completed__isnull =False ).order_by('date_completed')
    return render(request,'todo/completedtodos.html',{'todos':todos})
    
def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password= request.POST['password'])
        #if does'nt match
        if user is None:
            return render(request,'todo/loginuser.html',{'form': AuthenticationForm(),'error':'username and password did not match'})
        else:
        #if username and password is correct, log them in
            login(request,user)
            return redirect('currenttodos')
        
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit= False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form': TodoForm(),'error':'Bad Data passed in'})
       
@login_required           
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user= request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request,'todo/viewtodo.html',{'todo': todo, 'form' : form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo': todo, 'form' : form,'error': 'Bad data passed'})
        
@login_required    
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user= request.user)
    if request.method == 'POST':
        #todo item is completed
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')
    
@login_required           
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user= request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
    