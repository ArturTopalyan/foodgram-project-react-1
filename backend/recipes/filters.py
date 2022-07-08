import django_filters
from tags.models import Tag

from .models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = django_filters.NumberFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, queryset, name, value):
        match value:
            case 1:
                return queryset.filter(favorites__user=self.request.user)
            case 0:
                return queryset.exclude(favorites__user=self.request.user)
            # flake8 ругался, что функция ничего не возвращает и пришлось
            # в крайнем случае ничего не делать
            case _:
                pass
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        match value:
            case 1:
                return queryset.filter(carts__user=self.request.user)
            case 0:
                return queryset.exclude(carts__user=self.request.user)
            case _:
                pass
        return queryset


class IngredientFilter(django_filters.FilterSet):
    class Meta:
        fields = {
            'name': (
                'iexact',
                'istartswith',
                'icontains',
            ),
        }
        model = Ingredient
