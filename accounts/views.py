from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import User


def login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('accounts:login')
        else:
            errors = True
            context = {
                'errors': errors
            }
            return render(request, 'accounts/login.html', context)
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(username=new_user.username, password=new_user.password)
            auth.login(request, user)
            return redirect('login')
        else:
            form = UserForm(request.POST)
            context = {
                'form': form,
            }
            return render(request, 'accounts/signup.html', context)
    else:
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/signup.html', context)
