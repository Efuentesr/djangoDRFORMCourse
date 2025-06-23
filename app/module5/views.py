from drf_spectacular.utils import OpenApiParameter, extend_schema
from inventory.models import Category
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    CategorySerializer,
)


@extend_schema(
    tags=["Module 5"],
)
class CategoryListViewSet(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryListValuesViewSet(ViewSet):
    def list(self, request):
        categories = Category.objects.values("name", "slug")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryListOnlyViewSet(ViewSet):
    def list(self, request):
        categories = Category.objects.only("name", "slug")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryFilterViewSet(ViewSet):
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
        categories = Category.objects.exclude(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
