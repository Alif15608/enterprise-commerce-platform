from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """
    Base class for role-gated permissions. Subclass and set `required_role`.
    Not used directly — see IsAdmin, IsManager, etc. below.
    """
    required_role = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_roles.filter(role__name=self.required_role).exists()


class IsAdmin(HasRole):
    required_role = "admin"


class IsManager(HasRole):
    required_role = "manager"


class IsSeller(HasRole):
    required_role = "seller"


class IsCustomer(HasRole):
    required_role = "customer"


class IsAdminOrManager(BasePermission):
    """
    Composite permission for endpoints both Admins and Managers can access
    (e.g. inventory management in later phases) but Sellers/Customers cannot.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_roles.filter(role__name__in=["admin", "manager"]).exists()