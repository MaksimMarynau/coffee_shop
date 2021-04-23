from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='product_list'),
    path('about/', views.aboutView, name='about'),
    path('contact/', views.contactView, name='contact'),
    path("<slug:slug>/", views.ProductDetailView.as_view(),
        name='product_detail'
    ),
]
