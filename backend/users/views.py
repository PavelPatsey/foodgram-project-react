from djoser.views import UserViewSet

from .models import User
from .pagination import UsersPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = UsersPagination
    queryset = User.objects.all().order_by("id")
