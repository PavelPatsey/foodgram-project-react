from djoser.views import UserViewSet
from .pagination import UsersPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = UsersPagination
