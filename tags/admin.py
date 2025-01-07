from django.contrib import admin

from .models import Tag


# Admins
class TagAdmin(admin.ModelAdmin):
	search_fields = ['lable']


admin.site.register(Tag, TagAdmin)
