from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.shortcuts import get_object_or_404
from .serializers import StoreSerializer, ProductSerializer, TransactionSerializer
from .models import Stores, Products, Transactions
import jwt
from datetime import datetime
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


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

    
    @action(methods=['get'], detail=False)
    def summary(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Stores.objects.filter(created_by=request.user)
            return Response({"item":"Stores", "count":len(queryset)}, status=status.HTTP_200_OK)
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
                Product = Products(**serializer.validated_data)
                Product.save()
                if Product.product_code and (Product.product_code != "0" or Product.product_code != '' or Product.product_code != '0000000000000'):
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(Product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    Product.product_barcode.save(f"{Product.product_code}.png", File(buffer), save=False)
                else:
                    Product.product_code = "0000000000000"
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(Product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    Product.product_barcode.save(f"{Product.product_code}.png", File(buffer), save=False)
                Product.save()
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
            if Product.product_code != request.data["product_code"]:
                if request.data["product_code"] and (request.data["product_code"] != "0" or request.data["product_code"] != '' or request.data["product_code"] != '0000000000000'):
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(request.data["product_code"], writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    Product.product_barcode.save(f"{request.data['product_code']}.png", File(buffer), save=False)
                else:
                    Product.product_code = "0000000000000"
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(Product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    Product.product_barcode.save(f"{Product.product_code}.png", File(buffer), save=False)
            Product.save()
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

    @action(methods=['get'], detail=False)
    def summary(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Products.objects.filter(created_by=request.user)
            return Response({"item":"Products", "count":len(queryset)}, status=status.HTTP_200_OK)
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

    @action(methods=['get'], detail=False)
    def summary(self, request):
        access_token = request.headers['Authorization'].split(" ")[1]
        decoded_token = verify_jwt(access_token)
        if request.user.id == decoded_token['user_id']:
            queryset = Transactions.objects.filter(created_by=request.user)
            current_month = datetime.now().month
            current_year = datetime.now().year
            current_month_transactions = queryset.filter(txn_dop__month=current_month, txn_dop__year=current_year)
            regular_amount_current_month = 0.0
            extra_amount_current_month = 0.0
            total_amount_current_month = 0.0
            for transaction in current_month_transactions:
                if transaction.product.product_is_extra:
                    extra_amount_current_month += transaction.txn_amount
                else:
                    regular_amount_current_month += transaction.txn_amount
            total_amount_current_month = regular_amount_current_month + extra_amount_current_month
            output_dict = {
                "item":"Transactions",
                "count":len(queryset),
                "current_month_count":len(current_month_transactions),
                "extra_amount_current_month":round(extra_amount_current_month, 2),
                "regular_amount_current_month":round(regular_amount_current_month, 2),
                "total_amount_current_month": round(total_amount_current_month, 2)
            }
            return Response(output_dict, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Unable to verify user"}, status = status.HTTP_401_UNAUTHORIZED)

