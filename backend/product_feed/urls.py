from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import ProductView, FeedUploadView, ProductDetailView
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [

    path('product/', ProductView.as_view(), name='products_list'),
    path('product/<str:code>', ProductDetailView.as_view(), name='products_detail'),

    path('feed/upload', FeedUploadView.as_view(), name='product_list_upload'),

    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

]
