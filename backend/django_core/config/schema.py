import graphene

from apps.cart.schema import CartMutation, CartQuery
from apps.catalog.schema import CatalogQuery


class Query(CatalogQuery, CartQuery, graphene.ObjectType):
    pass


class Mutation(CartMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
