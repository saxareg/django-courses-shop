from django.contrib import admin
from .import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'category', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at', 'title']
    list_per_page = 10
    search_fields = ['title']


# registration
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Course, ProductAdmin)
