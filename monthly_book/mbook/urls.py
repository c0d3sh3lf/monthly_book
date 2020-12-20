from django.contrib.auth.models import update_last_login
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('stores/', views.list_stores, name="stores"),
    path('add_store/', views.add_store, name="add_store"),
    path('update_store/<int:id>/', views.update_store, name="update_store"),
    path('delete_store/<int:id>/', views.delete_store, name="delete_store"),
    path('products/', views.list_products, name="products"),
    path('add_product/', views.add_product, name="add_product"),
    path('view_product/<int:id>/', views.view_product, name="view_product"),
    path('update_product/<int:id>/', views.update_product, name="update_product"),
    path('delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('list_transactions', views.list_transactions, name="list_transactions"),
    path('add_txn_pr/<int:id>', views.add_txn_pr, name="add_txn_pr"),
    path('add_txn/', views.add_txn_pr, name="add_txn"),
]
