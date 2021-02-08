from django.db.models import fields
from rest_framework import serializers
from .models import Stores, Products, Transactions

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"