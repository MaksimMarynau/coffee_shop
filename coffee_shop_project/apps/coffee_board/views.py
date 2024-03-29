from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.db.models.functions import Greatest
from taggit.models import Tag
from django.db.models import Q
import re

from .models import Product, Comment, Seller
from .forms import (
    CommentForm,
    CommentFormAuthenticated,
    RegistrationForm,
    SellerForm,
    ProductForm,
    AIFormSet,
    SearchForm,
    UserUpdateForm,
)
from cart.forms import CartAddProductForm


class ProductView(ListView):
    model = Product
    queryset = Product.objects.filter(available=True).order_by('-publish')
    template_name = 'products/product_list.html'
    paginate_by = 5
    context_object_name = 'my_products'


class TagIndexView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 5
    context_object_name = 'my_products'

    def get_queryset(self,tag_slug=None):
        return Product.objects.filter(tags__slug=self.kwargs.get('slug'),available=True)


class ProtectedView(TemplateView):
    template_name = 'products/product_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(DetailView):
    login_required = True
    model = Product
    slug_field = 'slug'
    template_name = 'products/product_detail.html'

    def post(self, request, slug):
        form = CommentForm(request.POST)
        filter = Product.objects.filter(available=True)
        product = get_object_or_404(filter, slug=slug)
        if request.user.is_authenticated:
            form = CommentFormAuthenticated(request.POST)
            print(f'{request.user} is_authenticated')
            if form.is_valid():
                print(f'{request.user} form valid')
                new_comment = form.save(commit=False)
                new_comment.name = self.request.user
                new_comment.email = self.request.user.email
                new_comment.product = product
                new_comment.save()
        else:
            print(f'{request.user} else')
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.product = product
                new_comment.save()
        return redirect(product.get_absolute_url())

    def get(self, request, slug):
        form = CommentForm()
        cart_product_form = CartAddProductForm()
        filter = Product.objects.filter(available=True)
        product = get_object_or_404(filter, slug=slug)
        return render(request, 'products/product_detail.html',
            {
            'form':form,
            'product':product,
            'cart_product_form':cart_product_form,
            })


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        #Search for SQLite
        results = Product.objects.filter(
            Q(title__contains=query) | Q(seller__user__username__contains=query) | Q(description__contains=query))
        #Search for PostgreSQL only
        # results = Product.objects.annotate(
        #     similarity=Greatest(
        #     TrigramSimilarity('title',query),
        #     TrigramSimilarity('seller__user__username',query),
        #     TrigramSimilarity('description',query),
        #     )
        # ).filter(similarity__gte=0.2).order_by('-similarity')
    return render(request, 'products/search.html',
            {'form': form,
            'query': query,
            'results': results,})


def tagsView(request):
    tags = Tag.objects.order_by('name').annotate(
        count_tags=Count('taggit_taggeditem_items')
    )
    return render(request, 'products/tags.html', {'tags':tags})


@login_required
def user_products(request):
    if request.user.is_staff:
        product_list = Product.objects.filter(available=True).order_by('-available','title')
    else:
        product_list = Product.objects.filter(seller=request.user.sellers, available=True).order_by('-available','title')
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        'account/user_products.html',
        {'products':products}
    )


@login_required
def user_canceled_products(request):
    if request.user.is_staff:
        product_list = Product.objects.filter(available=False).order_by('title')
    else:
        product_list = Product.objects.filter(seller=request.user.sellers, available=False).order_by('title')
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        'account/user_canceled_products.html',
        {'products':products}
    )


@login_required
def update_profile(request):
    if request.method == 'POST':
        seller_form = SellerForm(request.POST, instance=request.user.sellers)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        seller_form.user = request.user
        if seller_form.is_valid() and user_form.is_valid():
            seller_form.save()
            user_form.save()
            return redirect('/')
    else:
        seller_form = SellerForm(instance=request.user.sellers)
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'account/update_profile.html', {
        'seller_form': seller_form,
        'user_form': user_form,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user.sellers
            product.slug = '_'.join(re.findall(r'\w+',product.title)).lower()
            product.available = True
            product.save()
            product_form.save_m2m()
            formset = AIFormSet(request.POST, request.FILES, instance=product)
            if formset.is_valid():
                formset.save()
                return redirect('/')
    else:
        product_form = ProductForm()
        formset = AIFormSet()
    return render(request, 'account/add_product.html', {
        'product_form': product_form,
        'formset': formset,
    })


@login_required
def update_product(request,slug=None):
        if request.user.is_staff:
            product = get_object_or_404(
                Product,
                slug=slug,
            )
        else:
            productproduct = get_object_or_404(
                Product,
                slug=slug,
                seller=request.user.sellers
            )
        if request.method == 'POST':
            product_form = ProductForm(
                request.POST,
                request.FILES,
                instance=product
            )
            if product_form.is_valid():
                product_form.save()
                formset = AIFormSet(request.POST, request.FILES, instance=product)
                if formset.is_valid():
                    formset.save()
                    return redirect('user_products')
        else:
            product_form = ProductForm(instance=product)
            formset = AIFormSet(instance=product)
        return render(request, 'account/update_product.html', {
            'formset':formset,
            'product_form': product_form,
            'product': product,
        })


@login_required
def cancel_product(request,slug=None):
    if request.user.is_staff:
        product = get_object_or_404(
            Product,
            slug=slug,
        )
    else:
        product = get_object_or_404(
            Product,
            slug=slug,
            seller=request.user.sellers
        )
    if request.method == 'POST':
        product.available = False
        for x in product.tags.all():
            product.tags.remove(x)
        product.save()
        tag = Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0)
        tag.delete()
        return redirect('user_products')

    return render(request, 'account/cancel_product.html', {'product':product})


@login_required
def delete_product(request,slug=None):
    if request.user.is_staff:
        product = get_object_or_404(
            Product,
            slug=slug,
        )
    else:
        product = get_object_or_404(
            Product,
            slug=slug,
            seller=request.user.sellers
        )
    if request.method == 'POST':
        product.delete()
        tag = Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0)
        tag.delete()
        return redirect('user_canceled_products')

    return render(request, 'account/delete_product.html', {'product':product})
