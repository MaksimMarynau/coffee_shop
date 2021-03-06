from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from .models import Product


class ProductView(ListView):
    model = Product
    queryset = Product.objects.filter(status='published').order_by('-publish')
    paginate_by = 3
    template_name = 'products/product_list.html'
    context_object_name = 'my_products'
