from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter_courses, name='filter'),
    path('<str:my_slug>', views.single_course, name='single_course'),
    path('buy/<int:course_id>/', views.buy_course, name='buy_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
