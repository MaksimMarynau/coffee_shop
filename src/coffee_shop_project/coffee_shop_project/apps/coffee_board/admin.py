from django.contrib import admin

# Register your models here.
from .models import Product, ProductDescription, Seller

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','count','price','publish','status')
    list_filter = ('title', 'created','publish', 'seller')
    search_fields = ('title','seller')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('seller',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('product','country')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','phone','address')
