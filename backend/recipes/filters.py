from django_filters.rest_framework import FilterSet, filters

from users.models import User

from .models import Recipe


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ["author"]
