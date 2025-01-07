from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
	CreateModelMixin,
	DestroyModelMixin,
	RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import ProductFilter
from .models import (
	Cart,
	CartItem,
	Collection,
	Customer,
	Order,
	OrderItem,
	Product,
	ProductImage,
	Review,
)
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnlyPermission, ViewCustomerHistoryPermission
from .serializers import (
	AddCartItemSerializer,
	CartItemSerializer,
	CartSerializer,
	CollectionSerializer,
	CreateOrderSerializer,
	CustomerSerializer,
	OrderSerializer,
	ProductImageSerializer,
	ProductSerializer,
	ReviewSerializer,
	UpdateCartItemSerializer,
	UpdateOrderSerializer,
)


class CollectionViewSet(ModelViewSet):
	queryset = Collection.objects.annotate(products_count=Count('products')).all()
	serializer_class = CollectionSerializer
	permission_classes = [IsAdminOrReadOnlyPermission]

	def destroy(self, request: Request, *args, **kwargs):
		if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
			return Response(
				{'error': 'Collection still contains Products'},
				status=status.HTTP_405_METHOD_NOT_ALLOWED,
			)

		return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
	queryset = Product.objects.prefetch_related('images').all()
	serializer_class = ProductSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_class = ProductFilter
	pagination_class = DefaultPagination
	permission_classes = [IsAdminOrReadOnlyPermission]
	search_fields = ['title', 'description']
	ordering_fields = ['unit_price', 'last_update']

	# NOTE: Custom filtering logic for collection_id
	# def get_queryset(self):
	#     queryset = Product.objects.all()
	#     collection_id = self.request.query_params.get('collection_id')
	#     if collection_id is not None:
	#         queryset = queryset.filter(collection_id=collection_id)

	#     return queryset

	def get_serializer_context(self):
		return {'request': self.request}

	def destroy(self, request: Request, *args, **kwargs):
		if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
			return Response(
				{'error': 'Product is associated with an Order Item'},
				status=status.HTTP_405_METHOD_NOT_ALLOWED,
			)

		return super().destroy(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
	serializer_class = ProductImageSerializer

	def get_queryset(self):
		return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

	def get_serializer_context(self):
		return {'product_id': self.kwargs['product_pk']}


class ReviewViewSet(ModelViewSet):
	serializer_class = ReviewSerializer

	def get_queryset(self):
		return Review.objects.filter(product_id=self.kwargs['product_pk'])

	def get_serializer_context(self):
		return {'product_id': self.kwargs['product_pk']}


class CartViewSet(
	CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
	queryset = Cart.objects.prefetch_related('items__product').all()
	serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
	http_method_names = ['get', 'post', 'patch', 'delete']

	def get_queryset(self):
		return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related(
			'product'
		)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return AddCartItemSerializer

		if self.request.method == 'PATCH':
			return UpdateCartItemSerializer

		return CartItemSerializer

	def get_serializer_context(self):
		return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = [IsAdminOrReadOnlyPermission]

	# NOTE: If detail is True the action will be available on the detail view
	@action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
	def history(self, request, pk):
		return Response('Order API coming soon!')

	# NOTE: If detail is False the action will be available on the list view
	@action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
	def me(self, request):
		customer = Customer.objects.get(user_id=request.user.id)
		if request.method == 'GET':
			serializer = CustomerSerializer(customer)
			return Response(serializer.data)
		serializer = Customer(customer, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class OrderViewSet(ModelViewSet):
	http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Order.objects.all()
		customer_id = Customer.objects.only('id').get(user_id=user.id)
		return Order.objects.filter(customer_id=customer_id)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return CreateOrderSerializer
		if self.request.method == 'PATCH':
			return UpdateOrderSerializer
		return OrderSerializer

	def get_permissions(self):
		if self.request in ['PATCH', 'DELETE']:
			return [IsAdminOrReadOnlyPermission()]
		return [IsAuthenticated()]

	def create(self, request, *args, **kwargs):
		serializer = CreateOrderSerializer(
			data=request.data,
			context={'user_id': self.request.user.id},
		)
		serializer.is_valid(raise_exception=True)
		order = serializer.save()
		serializer = OrderSerializer(order)
		return Response(serializer.data)
