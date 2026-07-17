from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart-detail"),
    path("items/", views.CartAddItemView.as_view(), name="cart-add-item"),
    path("items/<int:item_id>/", views.CartUpdateItemView.as_view(), name="cart-update-item"),
    path("items/<int:item_id>/remove/", views.CartRemoveItemView.as_view(), name="cart-remove-item"),
    path("merge/", views.CartMergeView.as_view(), name="cart-merge"),
]