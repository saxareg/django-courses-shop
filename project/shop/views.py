from .tasks import send_purchase_email  # ← добавить импорт
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Category, Purchase


def index(request):
    # Получаем параметры из URL
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'popular')
    category_name = request.GET.get('category', '')
    page_number = request.GET.get('page', 1)

    courses = Course.objects.all()

    if min_price:
        courses = courses.filter(price__gte=float(min_price))
    if max_price:
        courses = courses.filter(price__lte=float(max_price))

    if sort_by == 'new':
        courses = courses.order_by('-created_at')
    elif sort_by == 'reviews':
        courses = courses.order_by('-reviews_qty')
    else:
        courses = courses.order_by('-students_qty')

    if category_name:
        courses = courses.filter(category__title=category_name)

    # Пагинация
    paginator = Paginator(courses, 10)

    try:
        courses_page = paginator.page(page_number)
    except PageNotAnInteger:
        courses_page = paginator.page(1)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_pages)

    return render(request, 'shop/courses.html', {
        'courses': courses_page,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort_by,
        'current_category': category_name,
    })


def single_course(request, my_slug):
    course = get_object_or_404(Course, slug=my_slug)
    return render(request, 'shop/single_course.html', {'course': course})


def filter_courses(request):  # ← эта функция остается с таким именем!
    category = Category.objects.all()

    current_min_price = request.GET.get('min_price', '')
    current_max_price = request.GET.get('max_price', '')
    current_sort = request.GET.get('sort', 'popular')
    current_category = request.GET.get('category', '')

    return render(request, 'shop/filter.html', {
        'category': category,
        'current_min_price': current_min_price,
        'current_max_price': current_max_price,
        'current_sort': current_sort,
        'current_category': current_category,
    })


@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Проверяем не куплен ли уже курс
    if Purchase.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Вы уже приобрели этот курс!')
        return redirect('shop:single_course', my_slug=course.slug)

    # Создаем запись о покупке
    Purchase.objects.create(user=request.user, course=course)

    # Увеличиваем счетчик студентов
    course.students_qty += 1
    course.save()

    # Асинхронная отправка email
    send_purchase_email.delay(request.user.id, course.title)

    messages.success(
        request, f'Курс "{course.title}" успешно приобретен! Проверьте вашу почту.')
    return redirect('shop:my_courses')


@login_required
def my_courses(request):
    purchases = Purchase.objects.filter(
        user=request.user).select_related('course')
    return render(request, 'shop/my_courses.html', {'purchases': purchases})
