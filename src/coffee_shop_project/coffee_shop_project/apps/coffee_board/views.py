from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

# Create your views here.
from .models import Product, Comment
from .forms import CommentForm

class ProductView(ListView):
    model = Product
    queryset = Product.objects.filter(status='published').order_by('-publish')
    paginate_by = 3
    template_name = 'products/product_list.html'
    context_object_name = 'my_products'


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'slug'
    template_name = 'products/product_detail.html'
