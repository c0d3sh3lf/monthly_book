from django.urls import path
from .apis import SuperUserViewSet, UserViewSet, LogoutView, TestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('su_users', SuperUserViewSet, basename='su_users')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),
    path('token/verify/', TokenVerifyView.as_view(), name="verify_token"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('test/', TestView.as_view(), name="test"),
] + router.urls
