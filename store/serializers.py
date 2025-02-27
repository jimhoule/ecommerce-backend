from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

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
from .signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Collection
		fields = ['id', 'title', 'products_count']

	products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['id', 'image']

	def create(self, validated_data):
		product_id = self.context['product_id']
		return ProductImage.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True, read_only=True)

	class Meta:
		model = Product
		fields = [
			'id',
			'title',
			'description',
			'slug',
			'inventory',
			'unit_price',
			'price_with_tax',
			'collection',
			'images',
		]

	price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
	# NOTE: Returns the associated serialiazed Collection
	# # collection = CollectionSerializer()

	# NOTE: Returns an hyperlink to the associated Collection
	# collection = serializers.HyperlinkedRelatedField(
	#     queryset=Collection.objects.all(),
	#     view_name='collection-detail',
	# )

	def calculate_tax(self, product: Product):
		return product.unit_price * Decimal(1.1)


class SimpleProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'unit_price']


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ['id', 'name', 'description', 'date']

	def create(self, validated_data):
		product_id = self.context['product_id']

		return Review.objects.create(product_id=product_id, **validated_data)


class CartItemProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['id', 'product', 'quantity', 'total_price']

	product = CartItemProductSerializer()
	total_price = serializers.SerializerMethodField(method_name='get_total_price')

	def get_total_price(self, cart_item: CartItem):
		return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = ['id', 'items', 'total_price']

	id = serializers.UUIDField(read_only=True)
	items = CartItemSerializer(many=True, read_only=True)
	total_price = serializers.SerializerMethodField(method_name='get_total_price')

	def get_total_price(self, cart: Cart):
		return sum(
			[item.quantity * item.product.unit_price for item in cart.items.all()]
		)


class AddCartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['id', 'product_id', 'quantity']

	product_id = serializers.IntegerField()

	def validate_product_id(self, value):
		if not Product.objects.filter(pk=value).exists():
			raise serializers.ValidationError(f'Product with ID {value} does not exist')

		return value

	def save(self, **kwargs):
		cart_id = self.context['cart_id']
		product_id = self.validated_data['product_id']
		quantity = self.validated_data['quantity']

		try:
			# Updates a Cart Item
			cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
			cart_item.quantity += quantity
			cart_item.save()

			self.instance = cart_item
		except CartItem.DoesNotExist:
			# Creates a Cart Item
			self.instance = CartItem.objects.create(
				cart_id=cart_id, **self.validated_data
			)

		return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(read_only=True)

	class Meta:
		model = Customer
		fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
	product = SimpleProductSerializer()

	class Meta:
		model = OrderItem
		fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True)

	class Meta:
		model = Order
		fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
	cart_id = serializers.UUIDField()

	def validate_cart_id(self, cart_id):
		if not Cart.objects.filter(pk=cart_id).exists():
			raise serializers.ValidationError(
				f'Cart with ID of {cart_id} does not exist'
			)
		if Cart.objects.filter(pk=cart_id).count() == 0:
			raise serializers.ValidationError(f'Cart with ID of {cart_id} is empty')
		return cart_id

	def save(self, **kwargs):
		with transaction.atomic():
			cart_id = self.validated_data['cart_id']
			customer = Customer.objects.get(user_id=self.context['user_id'])
			order = Order.objects.create(customer=customer)
			cart_items = CartItem.objects.select_related('product').filter(
				cart_id=cart_id
			)
			order_items = [
				OrderItem(
					order=order,
					product=cart_item.product,
					unit_price=cart_item.product.unit_price,
					quantity=cart_item.quantity,
				)
				for cart_item in cart_items
			]
			OrderItem.objects.bulk_create(order_items)
			Cart.objects.filter(pk=cart_id).delete()
			# NOTE: Sends signal
			order_created.send_robust(self.__class__, order=order)
			return order
