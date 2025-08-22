from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Course, Category


# def index(request):
#     courses = Course.objects.all()
#     return render(request, 'shop/courses.html', {'courses': courses})


# old method
# def index(request):
#     courses = Course.objects.all().order_by('-students_qty')
#     return render(request, 'shop/courses.html', {'courses': courses})

from django.shortcuts import render


def index(request):
    # Получаем параметры из URL
    # строка или None, если не передано
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'popular')  # по умолчанию 'popular'
    category_name = request.GET.get(
        'category', '')  # по умолчанию пустая строка

    courses = Course.objects.all()

    if min_price:
        courses = courses.filter(price__gte=float(
            min_price))  # цена >= min_price
    if max_price:
        courses = courses.filter(price__lte=float(
            max_price))  # цена <= max_price

    if sort_by == 'new':
        courses = courses.order_by('-created_at')  # новые сначала
    elif sort_by == 'reviews':
        courses = courses.order_by('-reviews_qty')  # по отзывам
    else:  # popular (по умолчанию)
        courses = courses.order_by('-students_qty')

    if category_name:
        # Используем title вместо id
        courses = courses.filter(category__title=category_name)

    return render(request, 'shop/courses.html', {
        'courses': courses,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort_by,
        'current_category': category_name,
    })


def single_course(request, my_slug):
    course = get_object_or_404(Course, slug=my_slug)
    return render(request, 'shop/single_course.html', {'course': course})


def filter_courses(request):
    category = Category.objects.all()
    return render(request, 'shop/filter.html', {'category': category})
