from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
# Register your models here.
from .models import (
    Product,
    ProductDescription,
    Seller,
    Comment,
    ProductImages,
)

class DescriptionInline(admin.StackedInline):
    model = ProductDescription

class ProductImagesInline(admin.StackedInline):
	model = ProductImages
	extra = 1
	readonly_fields = ('get_image',)

	def get_image(self,obj):
		return mark_safe(f'<img src={obj.image.url} width="100" height="auto"')

	get_image.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ('title','tags','count','price','publish','status')
    list_filter = ('title', 'created','publish', 'seller')
    search_fields = ('title','seller')
    inlines = [DescriptionInline,ProductImagesInline]
    prepopulated_fields = {'slug':('title',)}
    # raw_id_fields = ('seller',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    save_on_top = True
    save_as = True


@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('product','country','image_tag')
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100", height=auto />'.format(obj.image.url))

    image_tag.short_description = 'Image'

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
	list_display = ('title','product','get_image')
	readonly_fields = ('get_image',)

	def get_image(self,obj):
		return mark_safe(f'<img src={obj.image.url} width="80" height="auto"')

	get_image.short_description = 'Images'


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user','phone','address')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','product','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.site_title = "Coffee shop"
admin.site.site_header = "Coffee shop"
