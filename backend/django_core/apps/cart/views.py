from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import services
from .models import Cart
from .serializers import CartSerializer, AddItemSerializer, UpdateItemSerializer


def _resolve_cart(request):
    """
    Shared helper: resolves the caller's cart based on whether they're
    authenticated (JWT) or a guest (X-Guest-Token header).
    """
    if request.user and request.user.is_authenticated:
        return services.get_or_create_active_cart(user=request.user)

    token = request.headers.get("X-Guest-Token")
    return services.get_or_create_active_cart(session_token=token)


class CartDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = _resolve_cart(request)
        return Response(CartSerializer(cart).data)


class CartAddItemView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = _resolve_cart(request)
        try:
            services.add_item(cart=cart, **serializer.validated_data)
        except services.CartError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartUpdateItemView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, item_id):
        serializer = UpdateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = _resolve_cart(request)
        try:
            services.update_item_quantity(cart=cart, item_id=item_id, **serializer.validated_data)
        except services.CartError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CartSerializer(cart).data)


class CartRemoveItemView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, item_id):
        cart = _resolve_cart(request)
        try:
            services.remove_item(cart=cart, item_id=item_id)
        except services.CartError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartMergeView(APIView):
    """
    Called by the frontend immediately after a successful login,
    with the guest's X-Guest-Token header still present.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.headers.get("X-Guest-Token")
        if not token:
            return Response({"detail": "No guest token provided."}, status=status.HTTP_400_BAD_REQUEST)

        cart = services.merge_guest_cart_into_user_cart(user=request.user, session_token=token)
        if cart is None:
            cart = services.get_or_create_active_cart(user=request.user)
        return Response(CartSerializer(cart).data)