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


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'someone@domain.com'
    }), label="Email")

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'John'
    }), label="First Name")

    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Doe'
    }), label="Last Name")

    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Active?')

    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Superuser?')

    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Staff?')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'someone@domain.com'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'John'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Doe'
    }))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }), help_text="<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>",
    label="Password")

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }), help_text="This should match the password in the Password field.",
    label="Confirm Password")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_superuser = False
        user.is_staff = False

        if commit:
            user.save()

        return user
