import traceback

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ProductSerializer,
)


class challenge_1_1_ViewSet(ViewSet):
    #########################################
    # Task: Retrieve all active products only
    # Return: All fields
    # Order-By: Name (Decending)
    #########################################
    @extend_schema(
        tags=["_1_x Challenge Endpoint"],
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
