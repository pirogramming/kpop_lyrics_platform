from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordChangeDoneView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from Kasa.models import Comments
from accounts.decorators import login_required
from accounts.forms import InfoForm, UserForm, PasswordResetForm, SetPasswordForm
from accounts.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# 로그인 뷰
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_url = request.POST.get('next_url', 'accounts:login')
            if next_url == '/search/':
                next_url = ''
            return redirect(next_url)
            # return redirect('accounts:login')
        else:
            errors = True
            context = {
                'errors': errors
            }
            return render(request, 'accounts/login.html', context)
    else:
        context = {
            'next_url': request.GET.get('next', 'accounts:login'),
        }
        return render(request, 'accounts/login.html', context)


# 로그아웃 뷰
@login_required
def logout(request):
    next_url = request.GET.get('next', 'accounts:login')
    if next_url == '/search/':
        next_url = '/'
    auth.logout(request)
    return redirect(next_url)


# 회원가입 뷰
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                form.cleaned_data['password'])
            new_user.alias = form.cleaned_data['alias']
            new_user.interest = form.cleaned_data['interest']
            new_user.save()
            user = authenticate(username=new_user.username, password=request.POST['verify_password'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('accounts:login')
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
@login_required
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
    form_class = PasswordResetForm
    success_url = reverse_lazy('accounts:reset_pw_done')
    email_template_name = 'accounts/password_reset_email.html'
    # html_email_template_name = 'accounts/password_reset_email.html'


# 비밀번호 초기화 완료 뷰 / 메일 발송 완료
class reset_pw_done(PasswordResetDoneView):
    template_name = "accounts/reset_pw_done.html"


# # 비밀번호 초기화 메일로 들어온 URL 처리
# # 새로운 비밀번호 설정 뷰
class reset_pw_confirm(PasswordResetConfirmView):
    template_name = 'accounts/reset_pw_confirm.html'
    success_url = reverse_lazy("accounts:login")
    form_class = SetPasswordForm

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user


# 새로운 비밀번호 설정 완료 뷰
class reset_pw_complete(PasswordChangeDoneView):
    template_name = "accounts/reset_pw_complete.html"
    success_url = reverse_lazy("accounts:login")


#
# 닉네임, 관심사에 대한 정보 변경 뷰
@login_required
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
@login_required
def check_comment(request):
    comments = Comments.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'comments': comments
    }

    return render(request, 'accounts/check_comment.html', context)


# 특정 댓글 삭제 뷰
@login_required
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comments, pk=comment_pk)

    # 요청을 보낸 사용자와 comment 작성자가 같은지 확인
    # 한번의 검증단계(굳이 필요없을 수도...)
    if comment.user.pk == request.user.pk:
        comment.delete()

    return redirect('accounts:check_comment')
