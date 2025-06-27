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
    responses={200: ProductSerializer},
)
class challenge_1_3_ViewSet(ViewSet):
    #########################################
    # Task: Retrieve the first product created by date
    # Return: All fields
    # Order-By: N/A
    #########################################

    def list(self, request):
        #############
        # Replace ... with your solution.
        #############
        product = Product.objects.first()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
