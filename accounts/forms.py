from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm as DefaultPasswordResetForm, SetPasswordForm as DefaultSetPasswordForm
from accounts.models import User
from django.utils.translation import     gettext_lazy as _


class UserForm(forms.ModelForm):
    verify_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User

        fields = ['username', 'email', 'password', 'alias', 'interest']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Within 15 characters', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Within 10 characters', 'autocomplete': 'off'}),

            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'username': 'ID',
            'email': 'E-mail',
            'password': 'Password',
            'alias': 'Nickname',
            'interest': 'Favorite Group',

        }

    field_order = ['username', 'email', 'password', 'verify_password', 'alias', 'interest']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Id already exsists.')

        return username

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Nickname already exsists.')

        return alias

    def clean_verify_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('verify_password')
        if password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2


class InfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'alias', 'interest']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Within 10 characters', 'autocomplete': 'off'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),

        }
        labels = {
            'email': 'Email',
            'alias': 'Nickname',
            'interest': 'Favorite Group',
        }

    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Nickname already exsists.')
        return alias


class PasswordResetForm(DefaultPasswordResetForm):
    email = forms.EmailField(label="E-mail", max_length=254)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("The e-mail address is not assigned"
                                          " to any user account"))
        return self.cleaned_data["email"]

class SetPasswordForm(DefaultSetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput,
    )