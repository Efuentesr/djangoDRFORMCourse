from django.db.models import Q
from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ProductSerializer,
)


class CategoryListViewSet(ViewSet):
    # class CategoryListViewSet(viewsets.ViewSet):
    """
    Retrieves all categories with full model objects, demonstrating the use of logical operators.
    """

    @extend_schema(
        tags=["Module 6"],
    )
    def list(self, request):
        # Example 1: Using AND (Default behavior)
        # Find products that are active and belong to the category with ID=1
        # products_and = Product.objects.filter(is_active=True, category=1)
        # products_and = Product.objects.filter(is_active=True).filter(category=1)
        products_and = Product.objects.filter(Q(is_active=True) & Q(category=1))
        # products_or = Product.objects.filter(Q(is_active=True) | Q(category=1))
        # products_not = Product.objects.filter(~Q(is_active=True))

        # promotion_combined = Product.objects.filter(
        #     Q(is_active=True)
        #     & Q(category__id=1)
        #     & ~Q(productpromotionevent__isnull=False)
        # )

        # Serialize data to return response
        products_data = {
            # "promotion_combined": ProductSerializer(promotion_combined, many=True).data,
            # "products_not": ProductSerializer(products_not, many=True).data,
            "products_and": ProductSerializer(products_and, many=True).data,
            # "products_or": ProductSerializer(products_or, many=True).data,
        }

        return Response(products_data)
