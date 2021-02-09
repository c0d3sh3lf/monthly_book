from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsSuperUser
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        if self.request.method == 'DELETE':
            self.permission_classes = (IsSuperUser, )

        return super(UserViewSet, self).get_permissions()