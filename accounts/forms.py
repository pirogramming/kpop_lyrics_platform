from allauth.account.forms import ResetPasswordForm as DefaultResetPasswordForm
from django import forms
from accounts.models import User
from django.utils.translation import gettext as _


class UserForm(forms.ModelForm):
    verify_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User

        fields = ['username', 'email', 'password', 'alias', 'interest']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '10자 이내로 입력 가능', 'autocomplete': 'off'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'username': '아이디',
            'email': '이메일',
            'password': '비밀번호',
            # 'verify_password': '비밀번호확인',
            'alias': '닉네임',
            'interest': '관심사',
        }
    field_order = ['username', 'email', 'password', 'verify_password', 'alias', 'interest']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 사용중입니다.')
        return username

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('닉네임이 이미 사용중입니다.')
        return alias

    def clean_verify_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('verify_password')
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 다릅니다.')
        return password2


class InfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['alias', 'interest']
        widgets = {
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '10자 이내로 입력 가능', 'autocomplete': 'off'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),

        }

    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('닉네임이 이미 사용중입니다.')
        return alias


class ResetPasswordForm(DefaultResetPasswordForm):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(attrs={
            "type": "email",
            "size": "30",
        })
    )



