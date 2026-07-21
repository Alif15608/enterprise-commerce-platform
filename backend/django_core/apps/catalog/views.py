from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from apps.rbac.permissions import IsAdminOrManager
from . import services
from .models import Product
from .filters import ProductFilter
from .cache import make_product_list_cache_key, DEFAULT_CACHE_TTL
from .serializers import (
    CategorySerializer, ProductListSerializer,
    ProductDetailSerializer, ProductWriteSerializer,
)

from . import services


class CategoryTreeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        roots = services.get_category_tree()
        return Response(CategorySerializer(roots, many=True).data)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    queryset = services.get_product_queryset()
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "sku"]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        cache_key = make_product_list_cache_key(request.query_params.dict())
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=DEFAULT_CACHE_TTL)
        return response


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        product = services.get_product_detail_cached(slug)
        if product is None:
            return Response({"detail": "Not found."}, status=404)
        return Response(ProductDetailSerializer(product).data)

class ProductCreateView(APIView):
    permission_classes = [IsAdminOrManager]

    def post(self, request):
        serializer = ProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = services.create_product(**serializer.validated_data)
        return Response(ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductUpdateView(APIView):
    permission_classes = [IsAdminOrManager]

    def patch(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_deleted=False)
        serializer = ProductWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = services.update_product(product=product, **serializer.validated_data)
        return Response(ProductDetailSerializer(product).data)


class ProductDeleteView(APIView):
    permission_classes = [IsAdminOrManager]

    def delete(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_deleted=False)
        services.soft_delete_product(product=product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PopularProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = services.get_popular_products(limit=10)
        return Response(ProductListSerializer(products, many=True).data)