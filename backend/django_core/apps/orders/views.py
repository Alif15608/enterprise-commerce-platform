from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.services import get_or_create_active_cart
from apps.rbac.permissions import AllowAny, IsAdminOrManager

from . import services
from .models import Coupon
from .pricing import calculate_shipping, calculate_tax
from .serializers import (
    CheckoutSerializer,
    CouponSerializer,
    CouponValidateSerializer,
    OrderSerializer,
)


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

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminOrManager]

    def patch(self, request, order_number):
        new_status = request.data.get("status")
        try:
            order = services.update_order_status(
                order_number=order_number, new_status=new_status, is_staff=True,
            )
        except services.CheckoutError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(order).data)

class EstimateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        subtotal = Decimal(request.query_params.get("subtotal", "0"))
        tax = calculate_tax(subtotal)
        shipping = calculate_shipping(subtotal)
        return Response({"tax": tax, "shipping": shipping, "total": subtotal + tax + shipping})

class CouponValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            coupon, discount = services.validate_coupon(**serializer.validated_data)
        except services.CouponError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"code": coupon.code, "discount": discount})

class CouponListCreateView(APIView):
    permission_classes = [IsAdminOrManager]

    def get(self, request):
        coupons = Coupon.objects.all().order_by("-created_at")
        return Response(CouponSerializer(coupons, many=True).data)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = Coupon.objects.create(**serializer.validated_data)
        return Response(CouponSerializer(coupon).data, status=status.HTTP_201_CREATED)

class CouponDetailView(APIView):
    permission_classes = [IsAdminOrManager]

    def delete(self, request, pk):
        deleted_count, _ = Coupon.objects.filter(pk=pk).delete()
        if deleted_count == 0:
            return Response({"detail": "Coupon not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
