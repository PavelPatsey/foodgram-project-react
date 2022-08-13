from django_filters.rest_framework import FilterSet, filters

from users.models import User

from .models import Recipe


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = filters.NumberFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.NumberFilter(method="get_is_in_shopping_cart")

    def get_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )
