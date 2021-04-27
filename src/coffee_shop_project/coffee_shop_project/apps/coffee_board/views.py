from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.paginator import Paginator

# Create your views here.
from .models import Product, Comment
from .forms import CommentForm


class ProductView(ListView):
    model = Product
    queryset = Product.objects.filter(status='published').order_by('-publish')
    template_name = 'products/product_list.html'
    paginate_by = 5
    context_object_name = 'my_products'


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'slug'
    template_name = 'products/product_detail.html'

    def post(self, request, slug):
        form = CommentForm(request.POST)
        product = Product.objects.get(slug=slug)
        new_comment = None
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.save()
        return redirect(product.get_absolute_url())

    def get(self, request, slug):
        form = CommentForm()
        product = Product.objects.get(slug=slug)
        return render(request, 'products/product_detail.html',
            {
            'form':form,
            'product':product,
            })

def aboutView(request):
    return render(request, 'products/about.html')

def contactView(request):
    return render(request, 'products/contact.html')
