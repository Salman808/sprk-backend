import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, RelatedProduct


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class RelatedProductType(DjangoObjectType):
    class Meta:
        model = RelatedProduct


class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.Int())
    products = graphene.List(ProductType)

    def resolve_product(self, info, id):
        return Product.objects.get(id=id)

    def resolve_products(self, info):
        return Product.objects.all()


schema = graphene.Schema(query=Query)
