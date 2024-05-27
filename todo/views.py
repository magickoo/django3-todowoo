from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form': UserCreationForm()})
    # create a user
    else:
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
            user.save()
        else:
            # tell the user the password did'nt match
            print("Hello")
    
    
    