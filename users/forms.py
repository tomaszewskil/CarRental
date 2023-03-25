from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', "password1", "password2"]
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Username'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Email'})}

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Repeat password'})


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'description']


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'placeholder': 'Old password'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'placeholder': 'New password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Repeat new password'})


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
