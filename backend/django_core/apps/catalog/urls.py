from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryTreeView.as_view(), name="category-tree"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/popular/", views.PopularProductsView.as_view(), name="product-popular"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/<slug:slug>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("products/<slug:slug>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
    
]
