from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Stores(models.Model):
    store_name = models.CharField(max_length=512)
    store_address = models.TextField()
    store_type = models.CharField(max_length=32)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')

    def __str__(self):
        return f"{self.store_name}"

class Products(models.Model):
    product_name = models.TextField()
    product_desc = models.TextField()
    product_qty = models.FloatField()
    product_unit = models.CharField(max_length=16)
    product_code = models.CharField(max_length=191, null=True, default="0000000000000")
    product_rate_per_unit = models.FloatField()
    product_ccy = models.CharField(max_length=3)
    product_is_extra = models.BooleanField(default=False)
    product_type = models.CharField(max_length=3, null=True)
    product_barcode = models.ImageField(upload_to="images/", null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
    
    def __str__(self):
        return f"{self.product_name} ({self.product_code})"

class Transactions(models.Model):
    txn_timestamp = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
    store = models.ForeignKey(Stores, on_delete=models.DO_NOTHING, related_name='store')
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, related_name='product')
    txn_dop = models.DateField(default=timezone.now)
    txn_qty = models.FloatField()
    txn_unit = models.CharField(max_length=16)
    txn_amount = models.FloatField()
    txn_ccy = models.CharField(max_length=3)
    txn_remarks = models.TextField(default="")

    def __str__(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.id, self.txn_timestamp, self.product, self.store, self.created_by, self.txn_dop, self.txn_qty, self.txn_unit, self.txn_amount, self.txn_ccy, self.txn_remarks)