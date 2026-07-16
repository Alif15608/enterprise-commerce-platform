from django.urls import path
from . import views

urlpatterns = [
    path("roles/", views.RoleListView.as_view(), name="role-list"),
    path("roles/assign/", views.AssignRoleView.as_view(), name="role-assign"),
    path("roles/revoke/", views.RevokeRoleView.as_view(), name="role-revoke"),
]