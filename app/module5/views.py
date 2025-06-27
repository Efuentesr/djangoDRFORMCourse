import traceback

from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from inventory.models import Category, Product
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, mixins

from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


@extend_schema(
    tags=["Module 5"],
)
# en este view use try solo a modo de ejemplo
class CategoryListViewSet(ViewSet):
    def list(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            )


class CategoryListValuesViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        categories = Category.objects.values("name", "slug")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryListOnlyViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        categories = Category.objects.only("name", "slug")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryFilterViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        categories = Category.objects.filter(is_active=False)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class DynamicCategoryQueryFilterViewSet(ViewSet):
    # retrive Categories based on query parameter
    @extend_schema(
        parameters=[OpenApiParameter("active", exclude=False)],
        tags=["Module 5"],
    )
    def list(self, request):
        active_param = request.query_params.get("active")
        categories = Category.objects.all()

        if active_param is not None:
            if active_param.lower() == "true":
                categories = categories.filter(is_active=True)
            elif active_param.lower() == "false":
                categories = categories.filter(is_active=False)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# categories/active/<str:active_status>/
class DynamicCategoryURLFilterViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request, active_status=None):
        # active_param = request.query_params.get("active")
        categories = Category.objects.all()

        if active_status is not None:
            if active_status.lower() == "true":
                categories = categories.filter(is_active=True)
            elif active_status.lower() == "false":
                categories = categories.filter(is_active=False)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class InactiveCategoryExcludeViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        # active_param = request.query_params.get("active")
        categories = Category.objects.exclude(is_active=True).exclude(
            slug="electronics"
        )
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SortedCategoryViewSet(ViewSet):
    @extend_schema(
        tags=["Module 5"],
        parameters=[
            OpenApiParameter(
                name="order",
                type=str,
                enum=["asc", "desc"],
                description="Sort order: 'asc' for ascending, 'desc' for descending",
                required=False,
            )
        ],
    )
    def list(self, request, order="asc"):
        order = request.GET.get("order")
        if order == "desc":
            categories = Category.objects.filter(is_active=True).order_by("-name")
        else:
            categories = Category.objects.filter(is_active=True).order_by("name")

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class PriceRangeProductViewSet(ViewSet):
    """
    Retrieves the most expensive and cheapest product based on price.
    """

    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        cheapest_product = Product.objects.order_by(
            "price"
        ).first()  # Get the cheapest product
        expensive_product = Product.objects.order_by(
            "-price"
        ).first()  # Get the most expensive product

        # Serialize data
        data = {
            "cheapest_product": ProductSerializer(cheapest_product).data,
            "most_expensive_product": ProductSerializer(expensive_product).data,
        }

        return Response(data)


####
# Ex.10 Retrieves a paginated list of products.
####


class ProductPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 50


@extend_schema(
    tags=["Module 5"],
)
class ProductListViewSet(GenericViewSet, mixins.ListModelMixin):
    """
    Retrieves a paginated list of products.
    """

    queryset = Product.objects.all().order_by("id")  # Ordered QuerySet
    serializer_class = ProductSerializer
    pagination_class = ProductPagination  # Enable Pagination


####
# Ex.11 Retrieves distinct categories that products are connected to.
####


class DistinctCategoryViewSet(ViewSet):
    """
    Retrieves distinct categories that products are connected to.
    """

    @extend_schema(
        tags=["Module 5"],
    )
    def list(self, request):
        # Get distinct category IDs that products are connected to
        distinct_categories = (
            Product.objects.values("category")
            .distinct()
            .order_by("category")
            .exclude(category__isnull=True)
        )

        # Return the distinct category IDs
        data = [category["category"] for category in distinct_categories]

        return Response(data)
