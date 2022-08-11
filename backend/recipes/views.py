from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import RecipePagination
from .permissions import (IsAuthor, IsAuthorOrAdminOrIsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, ShortRecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-id")
    pagination_class = RecipePagination
    # permission_classes = [
    #     IsAuthorOrReadOnly or IsAdminUser or IsAuthenticatedOrReadOnly
    # ]
    # permission_classes = [
    #     (IsAuthor or IsAdminUser) and IsAuthenticatedOrReadOnly
    # ]
    permission_classes = [
        IsAuthorOrAdminOrIsAuthenticatedOrReadOnly,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        serializer = RecipeReadSerializer(
            instance=instance, context={"request": request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance = serializer.instance
        serializer = RecipeReadSerializer(
            instance=instance, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk=None):
        if request.method == "POST":
            user = request.user
            recipe = self.get_object()
            if Favorite.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                data = {"errors": "Рецепт уже добавлен в избранное"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(
                user=user,
                recipe=recipe,
            )
            serializer = ShortRecipeSerializer(
                recipe,
                context={"request": request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            user = request.user
            recipe = self.get_object()
            favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe,
            )
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            data = {"errors": "Рецепт уже удален из избранного"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            user = request.user
            recipe = self.get_object()
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                data = {"errors": "Рецепт уже добавлен в корзину"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe,
            )
            serializer = ShortRecipeSerializer(
                recipe,
                context={"request": request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            user = request.user
            recipe = self.get_object()
            favorite = ShoppingCart.objects.filter(
                user=user,
                recipe=recipe,
            )
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            data = {"errors": "Рецепт уже удален из корзины"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
