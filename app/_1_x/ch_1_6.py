from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ProductSerializer,
)

#################################
# Challenge Viewset
#################################


@extend_schema(
    tags=["_1_x Challenge Endpoint"],
    responses={200: ProductSerializer(many=True)},
)
class challenge_1_6_ViewSet(ViewSet):
    #########################################
    # Task: Filter products by price and category
    # Include: price of 19.99
    # Exclude: category 3
    # Return: All fields
    #########################################

    def list(self, request):
        products = Product.objects.filter(price=19.99).exclude(category=3)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
