import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Category, Product, Brand
from .filters import ProductFilter
from . import services


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        interfaces = (graphene.relay.Node,)

    children = graphene.List(lambda: CategoryType)

    def resolve_children(self, info):
        return self.children.filter(is_active=True)


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]
        interfaces = (graphene.relay.Node,)


class ProductType(DjangoObjectType):
    is_in_stock = graphene.Boolean()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "sku", "description", "price", "stock_quantity", "category", "brand", "images"]
        interfaces = (graphene.relay.Node,)
        filterset_class = ProductFilter

    def resolve_is_in_stock(self, info):
        return self.stock_quantity > 0


class CatalogQuery(graphene.ObjectType):
    # Reuses the exact same cached, N+1-safe queryset REST uses.
    products = DjangoFilterConnectionField(ProductType)
    product = graphene.Field(ProductType, slug=graphene.String(required=True))
    categories = graphene.List(CategoryType)

    def resolve_products(self, info, **kwargs):
        return services.get_product_queryset()

    def resolve_product(self, info, slug):
        return services.get_product_queryset().filter(slug=slug).first()

    def resolve_categories(self, info):
        # Top-level roots only — 'children' field above handles nesting,
        # resolved lazily per-node rather than building the whole tree
        # eagerly like the REST CategoryTreeView does.
        return Category.objects.filter(parent__isnull=True, is_active=True)