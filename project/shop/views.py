from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Course, Category


# def index(request):
#     courses = Course.objects.all()
#     return render(request, 'shop/courses.html', {'courses': courses})

def index(request):
    courses = Course.objects.all().order_by('-students_qty')
    return render(request, 'shop/courses.html', {'courses': courses})


def single_course(request, my_slug):
    course = get_object_or_404(Course, slug=my_slug)
    return render(request, 'shop/single_course.html', {'course': course})


def filter_courses(request):
    return render(request, 'shop/filter.html')
