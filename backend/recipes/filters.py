import django_filters
from tags.models import Tag

from .models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.MultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = django_filters.BooleanFilter(
        method='get_favorited',
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(followers__user=self.request.user)
        return Recipe.objects.all()

    def get_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return Recipe.objects.all()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        filter_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        fields = (
            'name',
        )
        model = Ingredient
