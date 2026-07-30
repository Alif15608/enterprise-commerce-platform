from django.urls import include, path

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("rbac/", include("apps.rbac.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("cart/", include("apps.cart.urls")),
    path("orders/", include("apps.orders.urls")),
]
