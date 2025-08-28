from django.contrib import admin
from .models import Category, Course, Purchase


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at', 'title')
    list_per_page = 10
    search_fields = ('title',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Purchase, PurchaseAdmin)
