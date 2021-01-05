from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Old Password'
    }), help_text="<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>",
    label="Old Password")

    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'New Password'
    }), help_text="This should be different from your previous password.",
    label="New  Password")

    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm Password'
    }), help_text="This should match the password in the Password field.",
    label="Confirm  Password")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def save(self, commit=True):
        user = super(UserPasswordChangeForm, self).save(commit=False)

        if commit:
            user.save()

        return user
