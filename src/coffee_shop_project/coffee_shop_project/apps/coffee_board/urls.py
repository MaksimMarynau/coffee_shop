from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='product_list'),
    path("<slug:slug>/", views.ProductDetailView.as_view(),
        name='product_detail'
    ),
]
