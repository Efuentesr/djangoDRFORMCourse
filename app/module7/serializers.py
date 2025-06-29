# serializers.py
from inventory.models import (
    Category,
    Product,
    ProductPromotionEvent,
    PromotionEvent,
    StockManagement,
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active", "level", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "is_active", "price", "category"]


class CategoryProductSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active", "level", "parent", "products"]


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "is_active", "price", "category"]


class StockManagementSerializer(serializers.ModelSerializer):
    product = StockProductSerializer()

    class Meta:
        model = StockManagement
        fields = ["quantity", "last_checked_at", "product"]


class ProductStockManagementSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManagement
        fields = ["quantity", "last_checked_at", "product"]


class ProductStockSerializer(serializers.ModelSerializer):
    stock = ProductStockManagementSerializerSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "is_active", "price", "stock"]


class PromotionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionEvent
        fields = ["id", "name", "start_date", "end_date", "price_reduction"]


class ProductPromotionEventSerializer(serializers.ModelSerializer):
    promotion_event = PromotionEventSerializer()

    class Meta:
        model = ProductPromotionEvent
        fields = ["product", "promotion_event"]


class ProductPromotionSerializer(serializers.ModelSerializer):
    # Serialize the related product promotion events
    promotion_events = ProductPromotionEventSerializer(
        source="productpromotionevent_set", many=True
    )

    class Meta:
        model = Product
        fields = ["id", "name", "price", "promotion_events"]
