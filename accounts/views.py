from allauth.account.views import PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, \
    PasswordResetFromKeyDoneView
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from Kasa.models import Comments
from accounts.forms import UserForm, InfoForm
from accounts.models import User


# 로그인 뷰
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


# 로그아웃 뷰
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


# 회원가입 뷰
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


# 비밀번호 변경 뷰
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


# 비밀번호 초기화 뷰
class reset_pw(PasswordResetView):
    template_name = "accounts/reset_pw.html"
    success_url = reverse_lazy('accounts:reset_pw_done')

    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다.')
        return super().form_valid(form)


# 비밀번호 초기화 완료 뷰 / 메일발송 후
class reset_pw_done(PasswordResetDoneView):
    template_name = "accounts/reset_pw_done.html"


# 비밀번호 초기화 메일로 들어온 URL 처리
# 새로운 비밀번호 설정 뷰
class reset_pw_confirm(PasswordResetFromKeyView):
    template_name = "accounts/reset_pw_confirm.html"
    success_url = reverse_lazy("accounts:reset_pw_complete")


# 새로운 비밀번호 설정 완료 뷰
class reset_pw_complete(PasswordResetFromKeyDoneView):
    template_name = "accounts/reset_pw_complete.html"


# 닉네임, 관심사에 대한 정보 변경 뷰
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


# 사용자가 작성한 댓글들 확인하는 뷰
def check_comment(request):
    comments = Comments.objects.filter(user=request.user)
    context = {
        'comments': comments
    }

    return render(request, 'accounts/check_comment.html', context)


# 특정 댓글 삭제 뷰
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comments, pk=comment_pk)

    # 요청을 보낸 사용자와 comment 작성자가 같은지 확인
    # 한번의 검증단계(굳이 필요없을 수도...)
    if comment.user.pk == request.user.pk:
        comment.delete()

    return redirect('accounts:check_comment')