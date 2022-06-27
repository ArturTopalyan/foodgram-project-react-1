from django_filters import FilterSet
from django_filters import CharFilter

from .models import Ingredient


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
