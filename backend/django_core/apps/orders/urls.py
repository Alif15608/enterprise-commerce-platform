from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("my-orders/", views.MyOrdersView.as_view(), name="my-orders"),
    path("all/", views.AllOrdersView.as_view(), name="all-orders"),
    path("<uuid:order_number>/", views.OrderDetailView.as_view(), name="order-detail"),
]