from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import UserPasswordChangeForm, UserUpdateForm, UserSignUpForm

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


# No Login Required Decorator
def no_login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session["error"] = "You are authenticated. Please logout to access this."
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
@no_login_required
def tnc(request):
    return render(request, "tnc.html", {})


@no_login_required
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


@login_required
def user_logout(request):
    logout(request)
    return redirect('mbook:index')


@no_login_required
def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)     # create form object
        if form.is_valid():
            if 'TnCAgreement' in request.POST.keys() and request.POST['TnCAgreement'] :
                user = form.save()
                user.refresh_from_db()
                return redirect("mbook:index")
            else:
                request.session["error"] = "Please agree to our Terms and Conditions."
                return redirect("user_management:sign_up")
        else:
            request.session["error"] = ""
            for error_field in form.errors:
                request.session["error"] += f"{form.errors[error_field]}<br />"
            return redirect("user_management:sign_up")
    args = {}
    (request, args) = view_error_success(request, args)
    args['form'] = UserSignUpForm()
    return render(request, 'sign_up.html', args)


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


@login_required
@su_required
def view_user(request, id):
    user = User.objects.get(id=id)
    args={}
    (request, args) = view_error_success(request, args)
    args["user"] = user
    return render(request, "view_user.html", args)


@login_required
@su_required
@login_required
def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "GET":
        form_user = UserUpdateForm(initial={
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'is_active':user.is_active,
            'is_superuser':user.is_superuser,
            'is_staff':user.is_staff})
        args = {}
        (request, args) = view_error_success(request, args)
        args["form_user"] = form_user
        args["id"] = id
        return render(request, "update_user.html", args)
    elif request.method == "POST":
        form_user = UserUpdateForm(request.POST)
        if form_user.is_valid():
            if not user.email == form_user.cleaned_data.get('email'):
                user.email = form_user.cleaned_data.get('email')
            if not user.first_name == form_user.cleaned_data.get('first_name'):
                user.first_name = form_user.cleaned_data.get('first_name')
            if not user.last_name == form_user.cleaned_data.get('last_name'):
                user.last_name = form_user.cleaned_data.get('last_name')
            if not user.is_active == form_user.cleaned_data.get('is_active'):
                user.is_active = form_user.cleaned_data.get('is_active')
            if not user.is_superuser == form_user.cleaned_data.get('is_superuser'):
                user.is_superuser = form_user.cleaned_data.get('is_superuser')
            if not user.is_staff == form_user.cleaned_data.get('is_staff'):
                user.is_staff = form_user.cleaned_data.get('is_staff')
            user.save()
            request.session["success"] = "User Updated Successfully."
            return redirect("user_management:list_users")
        else:
            request.session["error"] = "Invalid data found."
            return redirect("user_management:list_users")
    else:
        request.session["error"] = "Requested Method Not Allowed"
        return redirect["user_management:list_users"]


@login_required
@su_required
def delete_user(request, id):
    if request.user.id != id:
        User.objects.filter(id=id).delete()
        request.session["success"] = "User deleted successfully!"
        return redirect("user_management:list_users")
    else:
        request.session["error"] = "You are an administrator. You cannot delete yourself."
        return redirect("user_management:list_users")