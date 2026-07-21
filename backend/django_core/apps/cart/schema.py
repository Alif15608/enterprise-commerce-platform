import graphene
from graphene_django import DjangoObjectType

from .models import Cart, CartItem
from . import services


class CartItemType(DjangoObjectType):
    line_total = graphene.Decimal()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

    def resolve_line_total(self, info):
        return self.line_total


class CartType(DjangoObjectType):
    subtotal = graphene.Decimal()

    class Meta:
        model = Cart
        fields = ["id", "status", "items"]

    def resolve_subtotal(self, info):
        return sum((item.line_total for item in self.items.all()), start=0)


def _resolve_cart_for_context(info):
    """Mirrors apps.cart.views._resolve_cart — same identity resolution
    logic, just adapted for GraphQL's info.context instead of DRF's request."""
    request = info.context
    if request.user and request.user.is_authenticated:
        return services.get_or_create_active_cart(user=request.user)
    token = request.headers.get("X-Guest-Token")
    return services.get_or_create_active_cart(session_token=token)


class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    cart = graphene.Field(CartType)
    error = graphene.String()

    def mutate(self, info, product_id, quantity):
        cart = _resolve_cart_for_context(info)
        try:
            services.add_item(cart=cart, product_id=product_id, quantity=quantity)
        except services.CartError as e:
            return AddToCart(cart=None, error=str(e))
        return AddToCart(cart=cart, error=None)


class UpdateCartItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    cart = graphene.Field(CartType)
    error = graphene.String()

    def mutate(self, info, item_id, quantity):
        cart = _resolve_cart_for_context(info)
        try:
            services.update_item_quantity(cart=cart, item_id=item_id, quantity=quantity)
        except services.CartError as e:
            return UpdateCartItem(cart=None, error=str(e))
        return UpdateCartItem(cart=cart, error=None)


class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    update_cart_item = UpdateCartItem.Field()


class CartQuery(graphene.ObjectType):
    cart = graphene.Field(CartType)

    def resolve_cart(self, info):
        return _resolve_cart_for_context(info)