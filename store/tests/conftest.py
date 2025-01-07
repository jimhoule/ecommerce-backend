from django.contrib.auth.models import User
from pytest import fixture
from rest_framework.test import APIClient


# NOTE: Available to all test modules in the tests folder
@fixture
def api_client():
	return APIClient()


@fixture
def authenticate(api_client: APIClient):
	def execute(is_staff=False):
		return api_client.force_authenticate(user=User(is_staff=is_staff))

	return execute
