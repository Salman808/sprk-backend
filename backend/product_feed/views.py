# External apps
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Project app imports
from .models import Product
from .serializers import ProductSerializer, DataSerializer


class ProductView(generics.ListCreateAPIView):
    """
        This is the Product's Generic View for List and Create API

        list:
            List all of the products in the system.
                Args:
                    accepts only pagination params
                Returns:
                    returns the products listing with pagination
                Raises:
                     NotFound: If no more items found for the page or invalid page number provided.
        create:
            Create a new product
                Args:
                    Product (Object) : accepts an item object minimally must and for item code must be provide
                Returns:
                    Product (Object ): returns the newly created product Object
                Raises:
                     InvalidItem: If no item's code provided return invalid item error.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination


class ProductDetailView(generics.RetrieveAPIView):
    """
        This is the Product's Retrieval API which accept item's code and return the products matching item's code.
            retrieve:
                List the products in the system with provided item's code.
                    Args:
                        code (str) : Item's code is provided on the basis of which the products extracted.
                    Returns:
                        products (list : Product Object): returns the products listing with pagination with provided code

    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(item__code=kwargs.get("code")))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeedUploadView(APIView):
    """
            This endpoint created to upload or insert the data to system in the feed manner.
            You can upload the data as Json and as same format as provided in products.json file

            post:
                it accepts only the json file as input and insert the products to the database.
                Args:
                    json file (as formatted like products.json)
                Returns:
                    the inserted record to the databases.

        """

    allowed_methods = ['POST']

    def post(self, request, format=None):
        if request.data:
            prods = DataSerializer(data=request.data)
            if prods.is_valid():
                prods.save()
                return Response(prods.data, status=status.HTTP_201_CREATED)
            return Response(prods.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
