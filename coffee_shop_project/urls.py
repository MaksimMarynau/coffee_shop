"""coffee_shop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.flatpages import views as fp_views


from coffee_board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/update_profile', views.update_profile, name='update_profile' ),
    path('accounts/add_product', views.add_product, name='add_product' ),
    path('accounts/update_product/<slug:slug>/',
        views.update_product,
        name='update_product'
    ),
    path('accounts/cancel_product/<slug:slug>/',
        views.cancel_product,
        name='cancel_product'
    ),
    path('accounts/delete_product/<slug:slug>/',
        views.delete_product,
        name='delete_product'
    ),
    path('accounts/user_products', views.user_products, name='user_products'),
    path('accounts/user_canceled_products', views.user_canceled_products, name='user_canceled_products'),
    path('about/', fp_views.flatpage, {'url': '/about/'}, name='about'),
    path('contact/', fp_views.flatpage, {'url': '/contact/'}, name='contact'),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('coffee_board.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
