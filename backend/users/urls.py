from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()

router.register("users", CustomUserViewSet)

urlpatterns = [
    # path("api/", include("djoser.urls")),
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
]
