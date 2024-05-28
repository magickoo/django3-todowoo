from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout , authenticate
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
    return render(request,'todo/currenttodos.html')
    
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
        
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
     