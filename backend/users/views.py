from djoser.views import UserViewSet
from .pagination import UsersPagination
from .models import User


class CustomUserViewSet(UserViewSet):
    pagination_class = UsersPagination
    queryset = User.objects.all().order_by("id")
