from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
import re
# Create your views here.
from .models import Product, Comment, Seller
from .forms import (
    CommentForm,
    RegistrationForm,
    SellerForm,
    ProductForm,
    AIFormSet,
    SearchForm,
)

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.order_by('name').annotate(
            count_tags=Count('taggit_taggeditem_items')
        )
        return context

class ProductView(TagMixin,ListView):
    model = Product
    queryset = Product.objects.filter(draft=False).order_by('-publish')
    template_name = 'products/product_list.html'
    paginate_by = 5
    context_object_name = 'my_products'

class TagIndexView(TagMixin,ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 5
    context_object_name = 'my_products'

    def get_queryset(self,tag_slug=None):
        return Product.objects.filter(tags__slug=self.kwargs.get('slug'))

class ProtectedView(TemplateView):
    template_name = 'products/product_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ProductDetailView(TagMixin,DetailView):
    login_required = True
    model = Product
    slug_field = 'slug'
    template_name = 'products/product_detail.html'

    def post(self, request, slug):
        form = CommentForm(request.POST)
        filter = Product.objects.filter(draft=False)
        product = get_object_or_404(filter, slug=slug)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.name = self.request.user
            new_comment.email = self.request.user.email
            new_comment.product = product
            new_comment.save()
        return redirect(product.get_absolute_url())

    def get(self, request, slug):
        form = CommentForm()
        filter = Product.objects.filter(draft=False)
        product = get_object_or_404(filter, slug=slug)
        return render(request, 'products/product_detail.html',
            {
            'form':form,
            'product':product,
            })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Product.objects.annotate(
            similarity=Greatest(
            TrigramSimilarity('title',query),
            TrigramSimilarity('description',query),
            )
        ).filter(similarity__gte=0.2).order_by('-similarity')
    return render(request, 'products/search.html',
            {'form': form,
            'query': query,
            'results': results,})

def aboutView(request):
    return render(request, 'products/about.html')

def contactView(request):
    return render(request, 'products/contact.html')

# def tagsView(request):
#     tags = Tag.objects.order_by('name').annotate(
#         count_tags=Count('taggit_taggeditem_items')
#     )
#     return render(request, 'products/tags.html', {'tags':tags})

@login_required
def user_products(request):
    product_list = Product.objects.filter(seller=request.user.sellers)
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
def update_profile(request):
    if request.method == 'POST':
        seller_form = SellerForm(request.POST, instance=request.user.sellers)
        seller_form.user = request.user
        if seller_form.is_valid():
            seller_form.save()
            return redirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        seller_form = SellerForm(instance=request.user.sellers)
    return render(request, 'account/update_profile.html', {
        'seller_form': seller_form,
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user.sellers
            product.slug = '_'.join(re.findall(r'\w+',product.title)).lower()
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
        product = get_object_or_404(
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
                    return redirect(product.get_absolute_url())
        else:
            product_form = ProductForm(instance=product)
            formset = AIFormSet(instance=product)
        return render(request, 'account/update_product.html', {
            'formset':formset,
            'product_form': product_form,
            'product': product,
        })

@login_required
def delete_product(request,slug=None):
    product = get_object_or_404(
        Product,
        slug=slug,
        seller=request.user.sellers
    )
    if request.method == 'POST':
        product.delete()
        Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0).delete()
        return redirect('/')

    return render(request, 'account/delete_product.html')
