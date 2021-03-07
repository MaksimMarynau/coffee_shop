from django.db import models
from django.utils import timezone
from django.conf import settings
from phone_field import PhoneField
from django.urls import reverse

# Create your models here.
class Product(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField('Product title', max_length=100, unique=True,)
    count = models.IntegerField(default=0,)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )
    seller = models.ForeignKey(
        'Seller',
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})

    class Meta:
        ordering = ('-publish',)


class ProductDescription(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key = True,
        related_name='products_description',
    )
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.product.title

class Seller(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sellers'
    )
    nickname = models.CharField(max_length=100,unique=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nickname


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.product)
