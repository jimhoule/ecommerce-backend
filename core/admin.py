from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline

from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import TaggedItem

from .models import User


# Inlines
class TagInline(GenericStackedInline):
	model = TaggedItem
	autocomplete_fields = ['tag']


# Admins
class UserAdmin(BaseUserAdmin):
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide'),
				'fields': (
					'username',
					'password1',
					'password2',
					'email',
					'first_name',
					'last_name',
				),
			},
		),
	)


admin.site.register(User, UserAdmin)


class CustomProductAdmin(ProductAdmin):
	inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
