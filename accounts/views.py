from allauth.account.views import PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, \
    PasswordResetFromKeyDoneView
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.forms import UserForm, InfoForm
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


def change_pw(request):
    context = {}
    if request.method == "POST":
        current_password = request.POST['origin_password']
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST['password1']
            password_confirm = request.POST['password2']
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                return redirect('accounts:login')
            else:
                context.update({
                    'error': "새로운 비밀번호를 다시 확인해주세요."
                })
        else:
            context.update({
                'error': "현재 비밀번호가 일치하지 않습니다."
            })
    return render(request, 'accounts/change_pw.html', context)


class reset_pw(PasswordResetView):
    template_name = "accounts/reset_pw.html"
    success_url = reverse_lazy('accounts:reset_pw_done')

    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다.')
        return super().form_valid(form)


class reset_pw_done(PasswordResetDoneView):
    template_name = "accounts/reset_pw_done.html"


class reset_pw_confirm(PasswordResetFromKeyView):
    template_name = "accounts/reset_pw_confirm.html"
    success_url = reverse_lazy("accounts:reset_pw_complete")


class reset_pw_complete(PasswordResetFromKeyDoneView):
    template_name = "accounts/reset_pw_complete.html"


def change_info(request):
    if request.method == "POST":
        form = InfoForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            form = InfoForm(request.POST)
            context = {
                'form': form
            }
            return render(request, 'accounts/change_info.html', context)
    else:
        form = InfoForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'accounts/change_info.html', context)