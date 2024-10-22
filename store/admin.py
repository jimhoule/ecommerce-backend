from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from .models import Collection, Product, Customer, Order, OrderItem


# Inlines
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    autocomplete_fields = ['product']
    extra = 0

# Filters classes
class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_10 = '<10'

    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (self.LESS_THAN_10, 'Low'),
        ]
    
    def queryset(self, request, queryset: QuerySet):
        match(self.value()):
            case self.LESS_THAN_10:
                return queryset.filter(inventory__lt=10)


# Admin classes
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = f'{reverse('admin:store_product_changelist')}?collection__id={str(collection.id)}'
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('products'),
        )


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display  = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    ordering = ['title']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    list_per_page = 10

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        
        return 'Ok'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.SUCCESS,
        )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]


# Registrations
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
