from django import template
from datetime import date
from django.db.models import Count
from taggit.models import Tag

from ..models import Product

register = template.Library()

@register.simple_tag()
def date_now():
    current_date = date.today()
    return current_date.strftime("%d %B, %Y")

@register.simple_tag
def total_posts():
    return Product.objects.filter(draft=False).count()

@register.inclusion_tag('include/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Product.objects.filter(draft=False).order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=3):
    return Product.objects.annotate(total_comments=Count('comments')) .order_by('-total_comments')[:count]
