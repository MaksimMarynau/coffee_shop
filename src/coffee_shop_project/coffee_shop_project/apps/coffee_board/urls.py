from django.urls import path


from . import views


urlpatterns = [
    path('', views.ProductView.as_view(), name='product_list'),
    path('tags/', views.tagsView, name='tags'),
    path('tag/<slug:slug>/', views.TagIndexView.as_view(), name='tagged'),
    path('search/', views.post_search, name='post_search'),
    path("<slug:slug>/", views.ProductDetailView.as_view(),
        name='product_detail'
    ),
]
