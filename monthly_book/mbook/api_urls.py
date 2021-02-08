from django.urls import path, include
from .apis import ProductViewSet, StoreViewSet, TransactionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('stores', StoreViewSet, basename='stores')
router.register('products', ProductViewSet, basename='products')
router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls
