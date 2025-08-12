from django.contrib import admin
from .import models


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Course, ProductAdmin)
