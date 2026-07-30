from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("my-orders/", views.MyOrdersView.as_view(), name="my-orders"),
    path("all/", views.AllOrdersView.as_view(), name="all-orders"),
    path("<uuid:order_number>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<uuid:order_number>/status/", views.UpdateOrderStatusView.as_view(), name="order-status-update"),
    path("estimate/", views.EstimateView.as_view(), name="order-estimate"),
    path("coupons/validate/", views.CouponValidateView.as_view(), name="coupon-validate"),
    path("coupons/", views.CouponListCreateView.as_view(), name="coupon-list-create"),
    path("coupons/<int:pk>/", views.CouponDetailView.as_view(), name="coupon-detail"),
]