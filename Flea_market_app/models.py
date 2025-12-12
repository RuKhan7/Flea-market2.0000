from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.name

# Профиль пользователя (Покупатель или Продавец)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_seller = models.BooleanField(default=False, verbose_name='Продавец')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    passport = models.CharField(max_length=50, verbose_name='Паспортные данные', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Товары
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    seller = models.ForeignKey(Profile, related_name='products', on_delete=models.CASCADE, verbose_name='Продавец')
    location = models.CharField(max_length=100, verbose_name='Местоположение товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # ДОБАВЬТЕ ПОЛЕ ДЛЯ ИЗОБРАЖЕНИЯ
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение товара')
    
    # ДОПОЛНИТЕЛЬНО: поле для URL изображения (если нужно)
    image_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение')
    
    categories = models.ManyToManyField(Category, through='ProductCategory', related_name='products', verbose_name='Категории')

    def __str__(self):
        return self.title

# Промежуточная таблица для связи "Товары-Категории"
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} - {self.category.name}'

# Комментарии
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments', verbose_name='Покупатель')
    text = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return f'Комментарий от {self.buyer.user.username} на товар {self.product.title}'

# Отзывы
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews', verbose_name='Покупатель')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'Отзыв на товар {self.product.title} от {self.buyer.user.username}'

# Комментарии к отзывам
class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comments', verbose_name='Отзыв')
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='review_comments', verbose_name='Покупатель')
    text = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return f'Комментарий к отзыву {self.review.id} от {self.buyer.user.username}'
    