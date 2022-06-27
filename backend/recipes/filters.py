from django_filters import (
    CharFilter,
    FilterSet,
    MultipleChoiceFilter,
    BooleanFilter,
)
from tags.models import Tag

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = MultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(
        method='get_favorited',
    )
    is_in_shopping_cart = BooleanFilter(
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


class IngredientFilter(FilterSet):
    name = CharFilter(
        filter_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        fields = (
            'name',
        )
        model = Ingredient
