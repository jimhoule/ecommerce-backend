from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# Inlines
class TagInline(GenericStackedInline):
    model = TaggedItem
    autocomplete_fields = ['tag']


# Admins
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
