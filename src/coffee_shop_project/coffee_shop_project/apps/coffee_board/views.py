from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from taggit.models import Tag
from django.db.models import Count
# Create your views here.
from .models import Product, Comment
from .forms import CommentForm

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().order_by('name').annotate(count_tags=Count('taggit_taggeditem_items'))
        return context

class ProductView(TagMixin,ListView):
    model = Product
    queryset = Product.objects.filter(status='published').order_by('-publish')
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
class ProductDetailView(DetailView):
    login_required = True
    model = Product
    slug_field = 'slug'
    template_name = 'products/product_detail.html'

    def post(self, request, slug):
        form = CommentForm(request.POST)
        product = Product.objects.get(slug=slug)
        new_comment = None
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.name = self.request.user
            new_comment.email = self.request.user.email
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
