from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ProductNamePriceSerializer,
)

#################################
# Challenge Viewset
#################################


@extend_schema(
    tags=["_1_x Challenge Endpoint"],
    responses={200: ProductNamePriceSerializer(many=True)},
)
class challenge_1_2_ViewSet(ViewSet):
    #########################################
    # Task: Retrieve all products
    # Return: Only name and price fields as QuerySet
    # Order-By: Price, Descending Order
    #########################################

    def list(self, request):
        products = (
            #############
            # Replace ... with your solution.
            #############
            Product.objects.only("name", "price").order_by("-price")
        )

        serializer = ProductNamePriceSerializer(products, many=True)
        return Response(serializer.data)
