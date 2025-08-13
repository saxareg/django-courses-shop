from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:my_slug>', views.single_course, name='single_course'),
]
