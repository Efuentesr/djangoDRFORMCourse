# views.py
from django.db import connection
from django.db.models import F
from drf_spectacular.utils import extend_schema
from inventory.models import Category, Product, StockManagement
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    CategoryProductSerializer,
    ProductPromotionSerializer,
    ProductSerializer,
    ProductStockSerializer,
    StockManagementSerializer,
)

####
#  Ex.1 Use of Inner Join for One-to-Many relationships.
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class ProductCategoryViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join for One-to-Many relationships.
    """

    def list(self, request):
        # Ex1 Return all data from both product and category
        # products = Product.objects.all()
        products = Product.objects.select_related("category")

        # Ex2 Return all products for all disabled categories
        # products = Product.objects.filter(category__is_active=False).select_related(
        #     "category"
        # )

        # Serialize data to return response
        products_data = ProductSerializer(products, many=True).data

        return Response(products_data)


####
#  Ex.2
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class ReturnWithValuesViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Values.
    """

    def list(self, request):
        # Ex1
        products = Product.objects.select_related("category").values(
            "id", "name", "category__name"
        )

        return Response(list(products))


####
#  Ex.3
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class ReturnWithOnlyViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Only
    """

    def list(self, request):
        # Ex1
        products = Product.objects.select_related("category").only(
            "id", "name", "category__name"
        )

        # Serialize data to return response
        products_data = ProductSerializer(products, many=True).data

        return Response(products_data)


####
#  Ex.4
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class AnnotateReturnWithValuesViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Values.
    """

    def list(self, request):
        # Ex1
        products = (
            Product.objects.select_related("category")
            .annotate(c_name=F("category__name"), p_name=F("name"))
            .values("id", "p_name", "c_name")
        )

        return Response(list(products))


####
#  Ex.5 Reverse Inner Join
####


@extend_schema(
    tags=["Module 7 - Reverse Inner Join"],
)
class RevProductCategoryViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join for One-to-Many relationships.
    """

    def list(self, request):
        # Ex1 Return all data from both product and category
        category = Category.objects.prefetch_related("products")

        # Serialize data to return response
        category_data = CategoryProductSerializer(category, many=True).data

        return Response(category_data)


####
#  Ex.6 Reverse Inner Join
####


@extend_schema(
    tags=["Module 7 - Reverse Inner Join"],
)
class RevValuesProductCategoryViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join for One-to-Many relationships and `.values()`.
    """

    def list(self, request):
        # Fetch all product data for categories, including category name and product name
        categories_data = (
            Category.objects.filter(is_active=True)
            .filter(products__isnull=False)
            .values(
                "id",
                "name",
                "slug",
                "products__id",
                "products__name",
                "products__price",
            )
        )

        # Return the data as response
        return Response(categories_data)


####
#  Ex.7 Use of Inner Join for One-to-One relationships.
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class StockManagementViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join for One-to-One relationships.
    """

    def list(self, request):
        # Ex1 Return all data from both stock management and products
        stock = StockManagement.objects.select_related("product")

        # Serialize data to return response
        stock_data = StockManagementSerializer(stock, many=True).data

        return Response(stock_data)


####
#  Ex.8 Use of Reverse Inner Join for One-to-One relationships.
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class RevStockManagementViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join for One-to-One relationships.
    """

    def list(self, request):
        # Ex1 Return all data from both stock management and products
        product = Product.objects.filter(stock__isnull=False).select_related("stock")

        # Serialize data to return response
        product_data = ProductStockSerializer(product, many=True).data

        return Response(product_data)


####
#  Ex.9
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class RawSQLProductCategoryViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join using Raw SQL.
    """

    def list(self, request):
        # Write a raw SQL query to simulate an INNER JOIN
        query = """
            SELECT p.id, p.name, c.name AS category_name
            FROM inventory_product p
            INNER JOIN inventory_category c ON p.category_id = c.id
            WHERE p.category_id IS NOT NULL
            LIMIT 5;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        # Format the results into a response
        products_data = [
            {"id": row[0], "name": row[1], "category_name": row[2]} for row in results
        ]

        return Response(products_data)


####
#  Ex.10
####


@extend_schema(
    tags=["Module 7 - Inner Join"],
)
class RawQuerySetProductCategoryViewSet(viewsets.ViewSet):
    """
    Demonstrates the use of Inner Join using Raw SQL.
    """

    def list(self, request):
        # Write a raw SQL query to simulate an INNER JOIN
        query = """
            SELECT p.id, p.name, c.name AS category_name
            FROM inventory_product p
            INNER JOIN inventory_category c ON p.category_id = c.id
            WHERE p.category_id IS NOT NULL
            LIMIT 5;
        """

        products = Product.objects.raw(query)  # Use Django's raw method

        # Serialize data to return response
        products_data = ProductSerializer(products, many=True).data
        return Response(products_data)


####
#  Ex.11 Inner Join Many-to-Many
####


@extend_schema(
    tags=["Module 7 - Reverse Inner Join"],
)
class ProductPromotionEventViewSet(viewsets.ViewSet):
    """
    Demonstrates INNER JOIN between Product and PromotionEvent.
    This view set returns a list of products with their related promotion events.
    """

    def list(self, request):
        # Perform an inner join between Product and PromotionEvent using prefetch_related
        products_with_promotions = Product.objects.prefetch_related(
            "productpromotionevent_set__promotion_event"
        ).filter(productpromotionevent__promotion_event__isnull=False)

        # # Serialize the product data with promotion events
        # products_data = []
        # for product in products_with_promotions:
        #     product_info = ProductPromotionSerializer(product).data
        #     products_data.append(product_info)

        # Serialize all products and their promotion events automatically
        products_data = ProductPromotionSerializer(
            products_with_promotions, many=True
        ).data

        return Response(products_data)
