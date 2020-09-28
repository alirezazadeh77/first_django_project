from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.urls import reverse


def save_dir(instance, filename):
    print(instance.id)
    print(filename)
    return f'./product/{instance.id}-{filename}'


class Store(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=("owner"), on_delete=models.CASCADE,
                              related_name='products')
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    phone_number = models.BigIntegerField(unique=True)
    address = models.TextField(blank=True)

    products = models.ManyToManyField('Product', related_name='stores')

    def __str__(self):
        return self.name


class Category(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="category")
    is_enable = models.BooleanField(default=True)
    properties = JSONField(default=dict)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.parent and self == self.parent.parent:
            raise ValidationError("you cant set this to chategury")


class DocumentManager(models.Manager):
    def is_enable(self):
        return self.filter(is_enable=True)
        # super().queryset().filter()


class Product(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rating = None

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=save_dir)
    is_enable = models.BooleanField(default=True)
    objects = DocumentManager()
    properties = JSONField(default=dict)
    categurise = models.ManyToManyField('Category', related_name="products")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_image = ''
        if self.image:
            old_image = self.image
            self.image = ''
            super().save(*args, **kwargs)
        self.image = old_image
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not "Mapsa" in self.name:
            raise ValidationError("Must include Mapsa")

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    def rating(self):
        if self._rating is None:
            self._rating = ProductRating.objects.filter(
                product=self
            ).aggregate(
                avg_rating=Coalesce(models.Avg('rate'), 0),
                rating_count=models.Count('id')
            )
        return self._rating

    def rating_avg(self):
        return self.rating()['avg_rating']

    def rating_count(self):
        return self.rating()['rating_count']


class ProductRating(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey('product', on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rates")

    class Meta:
        # unique_together = ['user', 'product']
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_product_user')
        ]

    def __str__(self):
        return f"user: {self.user} -> product{self.product}"

    def get_absolute_url(self):
        return reverse('products-list')


class ProductBookMark(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    like_status = models.BooleanField(default=True)

    class Meta:
        # unique_together = ['user', 'product']
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_product_user_bookmark')
        ]


class Screenes(models.Model):

    def product_search(self):
        return Product.objects

    def Category_search(self):
        return Category.objects



