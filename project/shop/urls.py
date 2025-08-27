from django.urls import path, include
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_courses, name='filter'),
    path('<str:my_slug>', views.single_course, name='single_course'),
]
