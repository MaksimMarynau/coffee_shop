from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from taggit.managers import TaggableManager


class Seller(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        unique= True,
        related_name='sellers'
    )
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Seller.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.sellers.save()


class Product(models.Model):

    title = models.CharField('Product title', max_length=100, unique=True,)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/', blank=True,default='products/no-image.jpg')
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField("Available",default=True)
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='products'
    )
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug})

    class Meta:
        ordering = ('-publish',)


class ProductImages(models.Model):

    image = models.ImageField("Image", upload_to="products/additional/")
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


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
