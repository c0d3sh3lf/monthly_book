from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Stores(models.Model):
    store_name = models.TextField()
    store_address = models.TextField()
    store_type = models.CharField(max_length=32)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.store_name

class Products(models.Model):
    product_name = models.TextField()
    prodcut_desc = models.TextField()
    product_qty = models.FloatField()
    product_unit = models.CharField(max_length=16)
    product_code = models.CharField(max_length=191, unique=True)
    product_rate_per_unit = models.FloatField()
    product_ccy = models.CharField(max_length=3)
    product_is_extra = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return "{} - {}".format(self.product_name, self.product_code)

class Transactions(models.Model):
    txn_timestamp = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Stores, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    txn_dop = models.DateField(default=timezone.now)
    txn_qty = models.FloatField()
    txn_unit = models.CharField(max_length=16)
    txn_amount = models.FloatField()
    txn_ccy = models.CharField(max_length=3)

    def __str__(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.id, self.txn_timestamp, self.product, self.store, self.created_by, self.txn_dop, self.txn_qty, self.txn_unit, self.txn_amount, self.txn_ccy)