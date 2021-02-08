from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from .serializers import StoreSerializer, ProductSerializer, TransactionSerializer
from .models import Stores, Products, Transactions
import jwt



def verify_jwt(token):
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return decoded_token

    
class StoreViewSet(viewsets.ModelViewSet):

    def list(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Stores.objects.filter(created_by=request.user)
            serializer = StoreSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def retrieve(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Stores.objects.filter(created_by=request.user)
            store = get_object_or_404(queryset, id=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def create(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            serializer = StoreSerializer(data=request.data)
            if serializer.is_valid():
                store = Stores.objects.create(**serializer.validated_data)
                serializer = StoreSerializer(store, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)
    

    def update(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Stores.objects.filter(created_by=request.user)
            store = get_object_or_404(queryset, id=pk)
            serializer = StoreSerializer(store, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Stores.objects.filter(created_by=request.user)
            store = get_object_or_404(queryset, id=pk)
            store.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)


class ProductViewSet(viewsets.ModelViewSet):

    def list(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Products.objects.filter(created_by=request.user)
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def retrieve(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Products.objects.filter(created_by=request.user)
            Product = get_object_or_404(queryset, id=pk)
            serializer = ProductSerializer(Product)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def create(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                Product = Products.objects.create(**serializer.validated_data)
                serializer = ProductSerializer(Product, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)
    

    def update(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Products.objects.filter(created_by=request.user)
            Product = get_object_or_404(queryset, id=pk)
            serializer = ProductSerializer(Product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Products.objects.filter(created_by=request.user)
            Product = get_object_or_404(queryset, id=pk)
            Product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)


class TransactionViewSet(viewsets.ModelViewSet):
    
    def list(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Transactions.objects.filter(created_by=request.user)
            serializer = TransactionSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def retrieve(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Transactions.objects.filter(created_by=request.user)
            Transaction = get_object_or_404(queryset, id=pk)
            serializer = TransactionSerializer(Transaction)
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

    
    def create(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                Transaction = Transactions.objects.create(**serializer.validated_data)
                serializer = TransactionSerializer(Transaction, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)
    

    def update(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Transactions.objects.filter(created_by=request.user)
            Transaction = get_object_or_404(queryset, id=pk)
            serializer = TransactionSerializer(Transaction, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk=None):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Transactions.objects.filter(created_by=request.user)
            Transaction = get_object_or_404(queryset, id=pk)
            Transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)