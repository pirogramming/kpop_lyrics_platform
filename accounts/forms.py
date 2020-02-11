from django import forms

from accounts.models import User


class UserForm(forms.ModelForm):
    verify_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'verify_password', 'alias', 'interest']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter up to 15 characters', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter up to 10 characters', 'autocomplete': 'off'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'username': 'ID',
            'email': 'Email',
            'password': 'Password',
            'alias': 'Nickname',
            'interest': 'Favorite Group',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Same ID already in use')
        return username

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Same nickname already in use')
        return alias

    def clean_verify_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('verify_password')
        if password1 != password2:
            raise forms.ValidationError('Emails must match')
        return password2


class InfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['alias', 'interest']
        widgets = {
            'alias': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter up to 10 characters', 'autocomplete': 'off'}),
            'interest': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),

        }
        labels = {
            'alias': 'Nickname',
            'interest': 'Favorite Group',
        }

    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['alias'].widget.attrs['maxlength'] = 10

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if User.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Nickname already in use')
        return alias
