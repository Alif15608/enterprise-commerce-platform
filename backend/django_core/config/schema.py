import graphene

from apps.catalog.schema import CatalogQuery
from apps.cart.schema import CartQuery, CartMutation


class Query(CatalogQuery, CartQuery, graphene.ObjectType):
    pass


class Mutation(CartMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)