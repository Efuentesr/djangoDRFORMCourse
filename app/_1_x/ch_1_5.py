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
class challenge_1_5_ViewSet(ViewSet):
    #########################################
    # Task: Retrieve all products - excluding active products.
    # Return: All fields
    # Instruction: Do not use a filter()
    #########################################

    def list(self, request):
        products = Product.objects.exclude(is_active=True)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
