from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Ingredient, IngredientAmount, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "color",
            "slug",
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
        ]


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = IngredientAmount
        fields = [
            "id",
            "name",
            "measurement_unit",
            "amount",
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, obj):
        return True

    def get_is_in_shopping_cart(self, obj):
        return True


# {
#   "count": 123,
#   "next": "http://foodgram.example.org/api/recipes/?page=4",
#   "previous": "http://foodgram.example.org/api/recipes/?page=2",
#   "results": [
#     {
#       "id": 0,
#       "tags": [
#         {
#           "id": 0,
#           "name": "Завтрак",
#           "color": "#E26C2D",
#           "slug": "breakfast"
#         }
#       ],
#       "author": {
#         "email": "user@example.com",
#         "id": 0,
#         "username": "string",
#         "first_name": "Вася",
#         "last_name": "Пупкин",
#         "is_subscribed": false
#       },
#       "ingredients": [
#         {
#           "id": 0,
#           "name": "Картофель отварной",
#           "measurement_unit": "г",
#           "amount": 1
#         }
#       ],
#       "is_favorited": true,
#       "is_in_shopping_cart": true,
#       "name": "string",
#       "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
#       "text": "string",
#       "cooking_time": 1
#     }
#   ]
# }
