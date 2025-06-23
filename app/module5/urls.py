# module4/urls.py
from inspect import getmembers, isclass

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from . import views
from .views import DynamicCategoryURLFilterViewSet

router = DefaultRouter()

# Automatically find all ViewSets in views.py and register them
for name, cls in getmembers(views, isclass):
    if issubclass(cls, ViewSet) and cls.__module__ == views.__name__:
        if name != "DynamicCategoryURLFilterViewSet":
            router.register(
                rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
            )

urlpatterns = [
    path("api/mod5/", include(router.urls)),  # Register the routes under '/api/mod5/'
    path(
        "categories/active/<str:active_status>/",
        DynamicCategoryURLFilterViewSet.as_view({"get": "list"}),
    ),
]
