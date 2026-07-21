from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.rbac.permissions import IsAdminOrManager
from apps.cart.services import get_or_create_active_cart
from . import services
from .serializers import OrderSerializer, CheckoutSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_active_cart(user=request.user)
        try:
            order = services.checkout(user=request.user, cart=cart, **serializer.validated_data)
        except services.CheckoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = services.get_orders_for_user(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        is_staff = request.user.user_roles.filter(role__name__in=["admin", "manager"]).exists()
        try:
            order = services.get_order_detail(
                user=request.user, order_number=order_number, is_staff=is_staff
            )
        except services.CheckoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order).data)


class AllOrdersView(APIView):
    """Admin/Manager view of every order in the system."""
    permission_classes = [IsAdminOrManager]

    def get(self, request):
        from .models import Order
        orders = Order.objects.prefetch_related("items").order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)