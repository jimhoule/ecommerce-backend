from django.urls import path, include
from .views import CartViewSet, CartItemViewSet, CustomerViewSet, CollectionViewSet, OrderViewSet, ProductViewSet, ReviewViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = [
   path('', include(router.urls)),
   path('', include(products_router.urls)),
   path('', include(carts_router.urls))
]