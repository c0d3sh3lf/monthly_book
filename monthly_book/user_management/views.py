from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import UserPasswordChangeForm

def view_error_success(request, args):
    error = ""
    if 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        args["error"] = error
    success = ""
    if 'success' in request.session:
        success = request.session['success']
        del request.session['success']
        args["success"] = success
    return (request, args)


# Login Required Decorator
def login_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["error"] = "You are not authenticated. Please authenticate yourself here."
            return redirect("mbook:index")
        else:
            return function(request, *args, **kwargs)
    return wrapper


# Superadmin Decorator
def su_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            request.session["error"] = "You are not authorized to view this section. Please contact administrator."
            return redirect("mbook:index")
        else:
            return function(request, *args, **kwargs)
    return wrapper


# User views
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('mbook:index')
            else:
                request.session['error'] = "User is inactive!"
                return redirect("mbook:index")
        else:
            request.session['error'] = "Invalid Username / Password!"
            return redirect("mbook:index")
    else:
        return redirect("mbook:index")


def user_logout(request):
    logout(request)
    return redirect('mbook:index')


@login_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        form_password = UserPasswordChangeForm(user = user, data=request.POST)
        print(form_password.errors)
        if form_password.is_valid():
            form_password.save()
            request.session["success"] = "Password Changed Successfully."
            logout(request)
            return redirect("mbook:index")
        else:
            error = ""
            if 'old_password' in form_password.errors:
                error += form_password.errors['old_password'][0]
            if 'new_password1' in form_password.errors:
                error += form_password.errors['new_password1'][0]
            if 'new_password2' in form_password.errors:
                error += form_password.errors['new_password2'][0]
            request.session["error"] = error
            return redirect("user_management:change_password")
    else:
        form_password = UserPasswordChangeForm(user=user)
        args = {}
        args["form_password"] = form_password
        (request, args) = view_error_success(request, args)
        return render(request, "change_password.html", args)


# Admin views
@login_required
@su_required
def list_users(request):
    all_users = User.objects.all()
    args = {}
    (request, args) = view_error_success(request, args)
    args["all_users"] = all_users
    return render(request, "list_users.html", args)