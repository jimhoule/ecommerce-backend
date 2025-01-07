from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
	wait_time = between(1, 5)

	@task(2)
	def view_products(self):
		collection_id = 1
		self.client.get(
			f'/store/products?collection_id={collection_id}', name='/store/products'
		)

	@task(4)
	def view_product(self):
		product_id = 1
		self.client.get(f'/store/products/{product_id}', name='/store/products/:id')

	@task(1)
	def add_to_cart(self):
		self.client.post(
			f'/store/carts/{self.cart_id}/items/',
			name='/store/carts/:id/items',
			json={'product_id': 1, 'quantity': 2},
		)

	# NOTE: Lifecycle hook
	def on_start(self):
		response = self.client.post('/store/carts/')
		cart = response.json()
		self.cart_id = cart['id']
