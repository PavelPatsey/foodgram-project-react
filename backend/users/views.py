from djoser.views import UserViewSet

from .models import User
from .pagination import UsersPagination


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all().order_by("id")
    pagination_class = UsersPagination
