from django.db.models import Q
from drf_spectacular.utils import extend_schema
from inventory.models import Product
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    ProductSerializer,
)


class ProductsInCategoryListViewSet(ViewSet):
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
        # products_and = Product.objects.filter(Q(is_active=True) & Q(category=1))
        # products_or = Product.objects.filter(Q(is_active=True) | Q(category=1))
        # products_not = Product.objects.filter(~Q(is_active=True))

        promotion_combined = Product.objects.filter(
            Q(is_active=True)
            & Q(category__id=10)
            # & Q(category=1)
            & ~Q(productpromotionevent__isnull=False)
            # & Q(productpromotionevent__isnull=True)
        )

        # Serialize data to return response
        products_data = {
            "promotion_combined": ProductSerializer(promotion_combined, many=True).data,
            # "products_not": ProductSerializer(products_not, many=True).data,
            # "products_and": ProductSerializer(products_and, many=True).data,
            # "products_or": ProductSerializer(products_or, many=True).data,
        }

        return Response(products_data)


@extend_schema(
    tags=["Module 6"],
)
class ComparisonOperatorViewSet(ViewSet):
    """
    Retrieves products using comparison operators, including equal to, not equal to, and negation (~).
    """

    def list(self, request):
        # Example 1: Greater Than (gt)
        # Find products with a price greater than 100
        products_gt = Product.objects.filter(price__gt=100)

        # Example 2: Less Than (lt)
        # Find products with a price less than 50
        products_lt = Product.objects.filter(price__lt=50)

        # Example 3: Greater Than or Equal to (gte)
        # Find products with a price greater than or equal to 30
        products_gte = Product.objects.filter(price__gte=30)

        # Example 4: Less Than or Equal to (lte)
        # Find products with a price less than or equal to 200
        products_lte = Product.objects.filter(price__lte=200)

        # Example 5: Exact Match (exact)
        # Find products whose name is exactly 'Product A'
        products_exact = Product.objects.filter(name__exact="Product A")

        # Example 6: Equal To (equal)
        # Find products whose name is 'Product B' (same as exact)
        products_equal = Product.objects.filter(name="Product B")

        # Example 7: Not Equal To (exclude)
        # Find products whose name is NOT 'Product A'
        products_not_equal = Product.objects.exclude(name="Product A")

        # Example 8: Using ~ (Negation)
        # Find products that do NOT belong to Category 1 (negating the condition)
        products_negation = Product.objects.filter(~Q(category__id=1))

        # Serialize data to return response
        products_data = {
            "products_gt": ProductSerializer(products_gt, many=True).data,
            "products_lt": ProductSerializer(products_lt, many=True).data,
            "products_gte": ProductSerializer(products_gte, many=True).data,
            "products_lte": ProductSerializer(products_lte, many=True).data,
            "products_exact": ProductSerializer(products_exact, many=True).data,
            "products_equal": ProductSerializer(products_equal, many=True).data,
            "products_not_equal": ProductSerializer(products_not_equal, many=True).data,
            "products_negation": ProductSerializer(products_negation, many=True).data,
        }

        return Response(products_data)

    ####


#  Ex.3 Using pattern matching methods.
####


@extend_schema(
    tags=["Module 6"],
)
class PatternMatchingViewSet(ViewSet):
    """
    Retrieves products using pattern matching methods: .contains() and .startswith().
    """

    def list(self, request):
        # Example 1: Using contains()
        # Find products whose name contains the substring 'shoe'
        products_contains = Product.objects.filter(name__icontains="Skirt")

        # Example 2: Using startswith()
        # Find products whose name starts with 'Super'
        products_startswith = Product.objects.filter(name__istartswith="Women")

        # Example 3: Combining contains() with other filters
        # Find products that are active and their name contains 'shirt'
        products_combined_contains = Product.objects.filter(
            is_active=True, name__icontains="Classic"
        )

        # Example 4: Combining startswith() with other filters
        # Find products in Category 2 that start with 'smart'
        products_combined_startswith = Product.objects.filter(
            category__id=11, name__istartswith="Mountain"
        )

        # Example 5: Case-insensitive contains (icontains)
        # Find products whose description contains 'eco' (case insensitive)
        products_description_contains = Product.objects.filter(
            description__icontains="Comfortable"
        )

        # Example 6: Using startswith() for filtering on 'slug'
        # Find products whose slug starts with 'new-arrival'
        products_slug_startswith = Product.objects.filter(
            slug__istartswith="bestselling"
        )

        # Serialize data to return response
        products_data = {
            "products_contains: skirt": ProductSerializer(
                products_contains, many=True
            ).data,
            "products_startswith": ProductSerializer(
                products_startswith, many=True
            ).data,
            "products_combined_contains": ProductSerializer(
                products_combined_contains, many=True
            ).data,
            "products_combined_startswith": ProductSerializer(
                products_combined_startswith, many=True
            ).data,
            "products_description_contains": ProductSerializer(
                products_description_contains, many=True
            ).data,
            "products_slug_startswith": ProductSerializer(
                products_slug_startswith, many=True
            ).data,
        }

        return Response(products_data)

    ####


#  Ex.4 Using list filtering methodss.
####


@extend_schema(
    tags=["Module 6"],
)
class ListFilteringViewSet(ViewSet):
    """
    Retrieves products using list filtering methods: `in_()` and `not_in()`.
    """

    def list(self, request):
        # Example 1: Using __in to filter products by a list of category IDs
        # Find products that belong to either Category 1, 2, or 3
        categories_list = [1, 2, 3]
        products_in = Product.objects.filter(category__in=categories_list)

        # Example 2: Using exclude() with __in to filter products not in a list of category IDs
        # Find products that are not in Category 1, 2, or 3
        products_not_in = Product.objects.exclude(category__in=categories_list)

        # Example 3: Using __in to filter products by a list of product IDs
        # Find products with specific IDs (e.g., 1, 2, and 3)
        product_ids = [1, 2, 3]
        specific_products = Product.objects.filter(id__in=product_ids)

        # Example 4: Using exclude() with __in to exclude products with specific IDs
        # Find products that are not 1, 2, or 3
        exclude_product_ids = [1, 2, 3]
        exclude_products = Product.objects.exclude(id__in=exclude_product_ids)

        # Example 5: Filtering products by multiple attributes with __in
        # Find products that belong to Category 1 or 2, and are active
        active_categories = [1, 2]
        active_products = Product.objects.filter(
            category__id__in=active_categories, is_active=True
        )

        # Example 6: Filtering products by multiple attributes with exclude() and __in
        # Find products that are not active and not in Category 1 or 2
        exclude_active_products = Product.objects.exclude(
            category__id__in=active_categories
        ).exclude(is_active=True)

        # Serialize data to return response
        products_data = {
            "products_in": ProductSerializer(products_in, many=True).data,
            "products_not_in": ProductSerializer(products_not_in, many=True).data,
            "specific_products": ProductSerializer(specific_products, many=True).data,
            "exclude_products": ProductSerializer(exclude_products, many=True).data,
            "active_products": ProductSerializer(active_products, many=True).data,
            "exclude_active_products": ProductSerializer(
                exclude_active_products, many=True
            ).data,
        }

        return Response(products_data)


####
#  Ex.5 Using Range.
####


@extend_schema(
    tags=["Module 6"],
)
class RangeFilteringViewSet(ViewSet):
    """
    Retrieves products using value range filtering: `range()`.
    """

    def list(self, request):
        # Example 1: Using __range to filter products by price range
        # Find products with a price between 100 and 500
        price_range = (100, 500)
        products_by_price = Product.objects.filter(price__range=price_range)

        # Example 2: Using __range to filter products by creation date range
        # Find products created between January 1, 2023, and December 31, 2023
        date_range = ("2023-01-01", "2026-12-31")
        products_by_date = Product.objects.filter(created_at__range=date_range)

        # Example 3: Using __range to filter products by ID range
        # Find products with IDs between 1 and 10
        id_range = (1, 10)
        products_by_id = Product.objects.filter(id__range=id_range)

        # Example 4: Filtering active products with price range
        # Find active products with a price between 50 and 200
        active_price_range = (50, 200)
        active_products_in_range = Product.objects.filter(
            is_active=True, price__range=active_price_range
        )

        # Example 5: Combining multiple ranges (price range and created date range)
        # Find products with a price between 100 and 500 created between January 1, 2023, and December 31, 2023
        combined_range = (100, 500)
        date_combined_range = ("2023-01-01", "2023-12-31")
        products_combined_range = Product.objects.filter(
            price__range=combined_range, created_at__range=date_combined_range
        )

        # Serialize data to return response
        products_data = {
            "products_by_price": ProductSerializer(products_by_price, many=True).data,
            "products_by_date": ProductSerializer(products_by_date, many=True).data,
            "products_by_id": ProductSerializer(products_by_id, many=True).data,
            "active_products_in_range": ProductSerializer(
                active_products_in_range, many=True
            ).data,
            "products_combined_range": ProductSerializer(
                products_combined_range, many=True
            ).data,
        }

        return Response(products_data)


###
#  Ex.6 List Slicing
####


@extend_schema(
    tags=["Module 6"],
)
class ListSlicingViewSet(ViewSet):
    """
    Retrieves products using List Slicing.
    """

    def list(self, request):
        # Example 1: Get the first 10 products
        first_10_products = Product.objects.all()[:10]
        # Example 2: Get products from 11th to 20th record
        next_10_products = Product.objects.all()[10:20]
        # Example 3: Using slicing with order_by
        first_last_products = Product.objects.order_by("-id")[:1]

        # Serialize data to return response
        products_data = {
            "first_10_products": ProductSerializer(first_10_products, many=True).data,
            "next_10_products": ProductSerializer(next_10_products, many=True).data,
            "first_last_products": ProductSerializer(
                first_last_products, many=True
            ).data,
        }

        return Response(products_data)
