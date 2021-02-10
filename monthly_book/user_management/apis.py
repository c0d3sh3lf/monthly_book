from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from .permissions import IsSuperUser
from .serializers import UserSerializer
import jwt
from datetime import datetime


def verify_jwt(token):
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return decoded_token


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()

    
    def list(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id'] and request.user.id == int(pk):
            user = get_object_or_404(self.queryset, id=pk)
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer=serializer)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, pk):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id'] and request.user.id == int(pk):
            user = get_object_or_404(self.queryset, id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id'] and request.user.id == int(pk):
            user = get_object_or_404(self.queryset, id=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)



class SuperUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        self.permission_classes = (IsSuperUser,)

        return super(SuperUserViewSet, self).get_permissions()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            access_token = request.headers['Authorization'].split(" ")[1]
            decoded_token = verify_jwt(access_token)
            if request.user.id == decoded_token['user_id']:
                refresh_token = request.data["refresh_token"]
                rtoken = RefreshToken(refresh_token)
                rtoken.blacklist()

                return Response(status = status.HTTP_205_RESET_CONTENT)
            else:
                return Response(status = status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            