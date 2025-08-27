from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255, unique=True,
                            blank=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField()
    students_qty = models.IntegerField()
    reviews_qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255, unique=True,
                            blank=True, db_index=True)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='courses_files/',
                            blank=True, null=True, verbose_name='Файл курса')
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликован')

    class Meta:
        ordering = ['students_qty']
        indexes = [
            models.Index(fields=['students_qty'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс')
    purchased_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата покупки')

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
