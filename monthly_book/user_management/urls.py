from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('tnc/', views.tnc, name="tnc"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('list_users/', views.list_users, name="list_users"),
    path('view_user/<int:id>/', views.view_user, name="view_user"),
    path('update_user/<int:id>', views.update_user, name="update_user"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
]
