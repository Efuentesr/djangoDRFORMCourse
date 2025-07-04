from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # path("", include("module4.urls")),
    # path("", include("module5.urls")),
    # path("", include("module6.urls")),
    path("", include("module7.urls")),
    # path("", include("_1_x.urls")),
]
